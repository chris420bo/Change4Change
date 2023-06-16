from flask import render_template, session
import wallet
import helpers
import bank


def get_dashboard(cur):
    connected = False

    if bank.check_connection(cur):
        connected = True

    if connected:
        # import any new transactions
        transactions = bank.import_transactions(cur)
        if transactions:
            wallet.store_transactions(cur, transactions)
        total = wallet.round_up(transactions)
        if total:
            successful = bank.charge_bank(cur, total)
            if successful:
                successful = wallet.deposit_change(cur, total)
                if successful:
                    wallet.update_last_donation(cur)

    # get name
    name = " ".join(helpers.get_name(cur))

    # get total donations
    total_donations = get_total_donations(cur)

    if not total_donations:
        total_donations = 0

    # get balance
    balance = wallet.get_total(cur)

    if not balance:
        balance = 0
    # get next milestone
    next_milestone = total_donations + (50 - (total_donations % 50))

    # get milestone_progress
    milestone_progress = round((total_donations / next_milestone) * 100, 1)

    # get transactions
    transactions = get_recent_transactions(cur)
    if transactions:
        transactions.reverse()

    return render_template("dashboard.html", name=name, total_donations=total_donations, balance=balance,
                           next_milestone=next_milestone, milestone_progress=milestone_progress,
                           transactions=transactions, connected=connected)


def get_total_donations(cur):
    try:
        wallet_id = wallet.get_wallet_id(cur)
        # Execute a SELECT query to get the total donations for a specific wallet_id
        query = "SELECT SUM(amount) FROM Donation WHERE source_wallet_id = %s"

        cur.execute(query, (wallet_id,))

        total_donations = cur.fetchone()[0]

        return total_donations
    except Exception as e:
        print("Error getting total donations:", e)
        return None


def get_recent_transactions(cur):
    try:
        uid = session.get("uid")
        sql = f"SELECT account_id FROM Bank WHERE user_id = '{uid}'"
        cur.execute(sql)  # access user banks
        account_id = cur.fetchone()[0]
        sql2 = f"SELECT account_number FROM CheckingAccount where account_id = '{account_id}'"
        cur.execute(sql2)  # access user checking_account
        account_number = cur.fetchone()[0]
        sql3 = f"SELECT * FROM Transactions WHERE source_account_number = '{account_number}' AND description <> " \
               f"'Change For Change Transaction' ORDER BY transaction_id"
        cur.execute(sql3)  # access all transactions for the specific checking account
        transactions = cur.fetchall()
        return withdraw_transactions(transactions)
    except Exception as e:
        print("Error getting transactions:", e)
        return None


def withdraw_transactions(transactions):
    target_transactions = []
    for transaction in transactions:
        if transaction[-1] == "W":
            target_transactions.append(transaction)
    return target_transactions
