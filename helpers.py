from flask import session
import re
import bank


def find_account(cur, un, pw):  # used for login
    """
    un = username, pw = password
    returns the row with the specified username and password,
    if it doesn't exist then it returns None
    """
    try:
        cur.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (un, pw))
        return cur.fetchone()
    except Exception as e:
        print("Error when finding account:", e)


def check_existing(cur, un, email):  # used for registration
    try:
        cur.execute("SELECT * FROM Users WHERE username = %s OR email = %s", (un, email))
        return cur.fetchone()
    except Exception as e:
        print("Error when finding account:", e)


def valid_email(email):
    # checks if email already in database or is valid --> if yes, return true; otherwise, return false
    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    except Exception as e:
        print("Error when checking email:", e)


def valid_username(un):
    validity = True
    if len(un) == 0 or len(un) > 8:
        validity = False
    elif re.search('[0-9]', un) is None:
        validity = False
    elif re.search('[A-Z]', un) or re.search('[a-z]', un) is None:
        validity = False
    return validity


def valid_password(pw):
    # checks if password is valid --> if yes, return true; otherwise, return false
    validity = True
    if len(pw) < 8 or len(pw) > 15:
        validity = False
    elif re.search('[0-9]', pw) is None:
        validity = False
    elif re.search('[A-Z]', pw) is None:
        validity = False
    elif re.search('[a-z]', pw) is None:
        validity = False
    elif (re.search('[!-/]', pw) or re.search('[:-@]', pw)) is None:
        validity = False
    return validity

# gets user id of the user
def get_uid(cur, un):
    try:
        sql = f"SELECT user_id FROM Users WHERE username = '{un}'"
        cur.execute(sql)
        res = cur.fetchall()
        return res[0]
    except Exception as e:
        print("Error when getting user id:", e)


def get_name(cur):
    try:
        uid = session.get("uid")
        sql = f"SELECT first_name, last_name FROM Users WHERE user_id = '{uid}'"
        cur.execute(sql)
        res = cur.fetchall()[0]
        return res
    except Exception as e:
        print("Error getting the name:", e)
        return None


def find_specific_account(last_4, account_id):
    try:
        uid = session.get("uid")
        bank_cur = bank.connect()
        if 1 <= uid <= 6:
            sql = f"SELECT * FROM CheckingAccount WHERE account_id = '{account_id}'"
        else:
            sql = f"SELECT * FROM CheckingAccount WHERE account_id = '{account_id}' " \
                  f"AND RIGHT(account_number,4) = '{last_4}'"
        bank_cur.execute(sql)
        target = bank_cur.fetchone()
        bank_cur.close()
        return target
    except Exception as e:
        print("Error finding account based on last 4-digits:", e)


def delete_transactions(cur, account_id):
    try:
        # start with bank then checkingAccount then Transactions
        sql1 = f"SELECT account_number FROM CheckingAccount WHERE account_id = {account_id}"
        cur.execute(sql1)
        account_number = cur.fetchone()[0]
        sql2 = f"DELETE FROM Transactions where source_account_number = '{account_number}'"
        cur.execute(sql2)
        print("deleting....")
    except Exception as e:
        print("Error deleting Transactions for user:", e)
