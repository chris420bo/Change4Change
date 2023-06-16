import datetime
from flask import render_template, session
import math
import bank
import charity


def get_total(cur):
    try:
        uid = session.get('uid')
        sql = f"SELECT balance FROM Wallet WHERE user_id = {uid}"
        cur.execute(sql)
        res = cur.fetchone()
        return res[0]
    except Exception as e:
        print("Error when accessing wallet: ", e)
        return None


def get_wallet(cur):
    charity_connected = False
    selected_charities = charity.chosen_charities(cur)
    if selected_charities:
        charity_connected = True
        selected_charities = ', '.join(selected_charities)
    balance = get_total(cur)
    # print("Wallet balance when doing /wallet", balance)
    if not balance:
        balance = 0
    else:
        if balance >= 50:  # Donate to the specific charities....
            balance = automated_donation(cur, balance)
    donations = charity.get_donations(cur)
    wallet_transactions = None
    if bank.check_connection(cur):
        wallet_transactions = recent_wallet_transactions(cur)
    return render_template("wallet.html", balance=balance, charity_connected=charity_connected,
                           selected_charities=selected_charities, donations=donations,
                           wallet_transactions=wallet_transactions)


def recent_wallet_transactions(cur):
    try:
        # update transactions in our db
        transactions = bank.import_transactions(cur)
        if transactions:
            store_transactions(cur, transactions)

        bank_cur = bank.connect()

        username, password, last_4 = bank.get_credentials(cur)
        account_number = bank.get_checking_account(bank_cur, cur, username, password, last_4)

        bank_cur.close()

        sql = f"SELECT description, " \
              f"CASE " \
              f"WHEN type = 'W' THEN amount " \
              f"WHEN type = 'D' THEN -amount " \
              f"END as amount, " \
              f"date " \
              f"FROM transactions " \
              f"WHERE destination_account_number = '99999999999' " \
              f"AND source_account_number LIKE '%{account_number}' " \
              f"ORDER BY transaction_id DESC " \
              f"LIMIT 5"

        cur.execute(sql)
        res = cur.fetchall()
        return res
    except Exception as e:
        print("Error getting wallet transactions:", e)


def automated_donation(cur, balance):  # each charity gets equal donations
    try:
        wallet_id = get_wallet_id(cur)
        amount = balance - (balance % 50)
        # distributed across the charities (add to their balance), insert in the donations table
        chosen_charities = charity.chosen_charities(cur)
        if not chosen_charities:
            chosen_charities = ["Meals On Wheels"]
        divisor = len(chosen_charities)
        donation = round(amount / divisor, 2)
        for i in range(divisor):
            current_charity = chosen_charities[i]
            # get destination_id from Charity table and add to charity balance
            cur.execute(f"SELECT user_id FROM Charity WHERE name = '{current_charity}'")
            destination_id = cur.fetchone()[0]
            cur.execute(f"UPDATE Charity SET balance = balance + {donation} WHERE user_id = {destination_id}")
            # store in Donations table
            cur.execute(f"INSERT INTO Donation (source_wallet_id, destination_charity_id, amount, created_on) VALUES\
                        ({wallet_id}, {destination_id}, {donation}, '{datetime.date.today()}')")
        bank.charge_bank(cur, amount, "D")
        balance = balance % 50
        update_wallet(cur, balance)
        return balance
    except Exception as e:
        print("Error automatically donating:", e)


def get_wallet_id(cur):
    try:
        uid = session.get("uid")
        query = f"SELECT wallet_id FROM Wallet WHERE user_id = {uid}"
        cur.execute(query)
        wallet_id = cur.fetchone()[0]
        return wallet_id
    except Exception as e:
        print("Error when getting wallet id: ", e)
        return None


def clean_transactions(transactions):
    cleaned_transactions = []
    for transaction in transactions:
        new_transaction = (transaction[0], transaction[1], transaction[2],
                           float(transaction[3]), str(transaction[4]), transaction[5])
        cleaned_transactions.append(new_transaction)
    return cleaned_transactions


def store_transactions(cur, transactions):
    cleaned_transactions = clean_transactions(transactions)
    # print(len(cleaned_transactions))
    for transaction in cleaned_transactions:
        try:
            query = f"INSERT INTO Transactions " \
                    f"(source_account_number, destination_account_number, description, amount, date, type) " \
                    f"VALUES {transaction}"
            cur.execute(query)

        except Exception as e:
            print("Error when getting storing transactions: ", e)


def wallet_transaction(cur, resulting_balance, account_id, last_4, change, deposit):
    try:
        type = "W"
        original = change
        if not deposit:
            change = -change
            type = "D"
        uid = session.get("uid")
        # add money to wallet
        balance = get_total(cur) + change
        bank.charge_bank(cur, original, type)
        update_wallet(cur, balance)
        # update BankAPI Database as well
        bank_cur = bank.connect()
        if 1 <= uid <= 6:
            sql5 = f"UPDATE CheckingAccount SET balance = '{resulting_balance}' WHERE account_id = '{account_id}' "
        else:
            sql5 = f"UPDATE CheckingAccount SET balance = '{resulting_balance}' WHERE account_id = '{account_id}' " \
                   f"AND RIGHT(account_number,4) = '{last_4}'"
        bank_cur.execute(sql5)
        bank_cur.close()
        return balance
    except Exception as e:
        print("Error when depositing/withdrawing in wallet page:", e)


def round_up(transactions):
    # source_account_number, destination_account_number, description, amount, date, type)

    total = 0
    for transaction in transactions:
        # only round withdrawals
        if transaction[5] == "W" and transaction[2] != "Change For Change Transaction":
            amount = transaction[3]

            total += math.ceil(amount) - amount

    return total


def deposit_change(cur, amount):
    balance = get_total(cur)
    print("Current:", balance)
    try:
        print("Added:", amount)
        total = balance + amount
        update_wallet(cur, total)
        return True
    except Exception as e:
        print("Error when depositing change:", e)
        return False


def update_last_donation(cur):
    try:
        bank_cur = bank.connect()

        username, password, last_4 = bank.get_credentials(cur)
        account_number = bank.get_checking_account(bank_cur, cur, username, password, last_4)

        bank_cur.close()
        sql = f"UPDATE CheckingAccount " \
              f"SET last_donation = '{datetime.date.today()}' " \
              f"WHERE account_number LIKE '%{account_number}'"
        cur.execute(sql)
        return True
    except Exception as e:
        print("Error when depositing change:", e)
        return False


def update_wallet(cur, amount):
    try:
        wallet_id = get_wallet_id(cur)
        sql = f"UPDATE Wallet " \
              f"SET balance = {amount} " \
              f"WHERE wallet_id = {wallet_id}"
        print("Final:", amount)
        cur.execute(sql)
    except Exception as e:
        print("Error updating wallet:", e)
