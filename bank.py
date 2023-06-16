import psycopg2
from flask import session
import datetime
import helpers


def check_connection(cur):
    try:
        uid = session.get("uid")
        cur.execute("SELECT * FROM Bank WHERE user_id = %s", (uid,))
        return cur.fetchone()
    except Exception as e:
        print("Error when checking bank connection:", e)


def check_bank_account(cur, bank_name, un):
    try:
        cur.execute("SELECT * FROM Bank WHERE bank_name = %s AND username = %s", (bank_name, un))
        return cur.fetchone()
    except Exception as e:
        print("Error when finding account:", e)


def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="BankAPI",
        user="postgres",
        password="abc123")

    conn.autocommit = True
    bank_cur = conn.cursor()
    return bank_cur


def get_credentials(cur):
    try:
        uid = session.get("uid")
        sql = f"SELECT username, password, account_number FROM Bank WHERE user_id = {uid}"
        cur.execute(sql)
        res = cur.fetchone()
        return res
    except Exception as e:
        print('Error when getting bank credentials: ', e)
        return None


def get_checking_account(bank_cur, cur, username, password, account_number):
    try:
        uid = session.get("uid")
        if 1 <= uid <= 6:
            account_id = get_account_id(cur)
            return helpers.find_specific_account(account_number, account_id)[0]
        sql = f"SELECT account_number " \
              f"FROM CheckingAccount " \
              f"WHERE username = '{username}' " \
              f"AND password = '{password}' " \
              f"AND account_number LIKE '%{account_number}'"
        bank_cur.execute(sql)
        res = bank_cur.fetchone()
        return res[0]
    except Exception as e:
        print('Error when getting bank details: ', e)
        return None


def get_last_donation(bank_cur, checking_account):
    try:
        sql = f"SELECT transaction_id FROM Transactions WHERE description = 'Last Donation' and " \
              f"source_account_number = '{checking_account}'"
        bank_cur.execute(sql)
        res = bank_cur.fetchone()
        if res:
            return res[0]
        return 0
    except Exception as e:
        print('Error when getting last donation: ', e)
        return None


def import_transactions(cur):
    # connect to bank api
    bank_cur = connect()
    username, password, account_number = get_credentials(cur)
    checking_account = get_checking_account(bank_cur, cur, username, password, account_number)
    # get last donation id
    last_donation = get_last_donation(bank_cur, checking_account)
    # import all transactions since last donation
    try:
        sql1 = f"SELECT source_account_number, destination_account_number, description, amount, date, type " \
               f"FROM Transactions " \
               f"WHERE (source_account_number = '{checking_account}' OR destination_account_number = '{checking_account}') " \
               f"AND transaction_id > {last_donation} " \
               f"ORDER BY transaction_id"
        bank_cur.execute(sql1)
        res = bank_cur.fetchall()
        delete_last_transaction(bank_cur, checking_account)
        add_last_transaction(bank_cur, checking_account)
        bank_cur.close()
    except Exception as e:
        print('Error when getting new set of transactions: ', e)
        return None

    bank_cur.close()
    return res


def add_last_transaction(bank_cur, checking_account):
    try:
        sql = f"INSERT INTO Transactions (source_account_number, destination_account_number, description, amount, " \
              f"date, type) " \
              f"VALUES ('{checking_account}', '99999999999', 'Last Donation', " \
              f"{0}, '{datetime.date.today()}', 'D')"
        bank_cur.execute(sql)
    except Exception as e:
        print('Error when adding last transaction: ', e)


def delete_last_transaction(bank_cur, checking_account):
    try:
        exists = get_last_donation(bank_cur, checking_account)
        if exists:
            sql = f"DELETE FROM Transactions WHERE source_account_number = '{checking_account}' AND description = 'Last " \
                f"Donation'"
            bank_cur.execute(sql)
    except Exception as e:
        print('Error when deleting last transaction: ', e)


def charge_bank(cur, amount, type="W"):
    bank_cur = connect()
    username, password, account_number = get_credentials(cur)
    checking_account = get_checking_account(bank_cur, cur, username, password, account_number)
    try:
        sql = f"INSERT INTO Transactions (source_account_number, destination_account_number, description, amount, " \
              f"date, type) " \
              f"VALUES ('{checking_account}', '99999999999', 'Change For Change Transaction', " \
              f"{amount}, '{datetime.date.today()}', '{type}')"
        bank_cur.execute(sql)
        bank_cur.close()
        return True
    except Exception as e:
        print('Error when charging bank: ', e)
        return False


def get_account_id(cur):
    try:
        uid = session.get("uid")
        sql = f'SELECT account_id FROM Bank WHERE user_id = {uid}'
        cur.execute(sql)
        return cur.fetchone()[0]
    except Exception as e:
        print("Error getting account_id:", e)


def get_last_four(cur):
    try:
        uid = session.get("uid")
        sql = f'SELECT account_number FROM Bank WHERE user_id = {uid}'
        cur.execute(sql)
        return cur.fetchone()[0]
    except Exception as e:
        print("Error getting account_id:", e)
