from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import hashlib
import helpers
from migrations import migrate
import profile
import dashboard
import psycopg2
import wallet
import datetime
import bank
import decimal
import displayCharities
from bank_db import migrate as migrate_bank
import charity

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = psycopg2.connect(
    host="localhost",
    database="ChangeForChange",
    user="postgres",
    password="abc123")

# database cursor
conn.autocommit = True
cur = conn.cursor()  # TODO: close cursor when finished


# index page
@app.route("/")
def root():
    # if there is a session, replace login with logout
    if not session.get("uid"):
        logged_in = False
    else:
        logged_in = True
    return render_template("index.html", logged_in=logged_in)


@app.route("/charity", methods=['GET', 'POST'])
def display_charity():
    # if there is a session, replace login with logout
    if not session.get("uid"):
        logged_in = False
    else:
        logged_in = True

    org_name, description = displayCharities.get_org_info(cur)
    return render_template("displayCharities.html", logged_in=logged_in, org_name=org_name, description=description)


@app.route("/about")
def rootA():
    # if there is a session, replace login with logout
    if not session.get("uid"):
        logged_in = False
    else:
        logged_in = True
    return render_template("about.html", logged_in=logged_in)


@app.route("/dashboard")
def home_dashboard():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return dashboard.get_dashboard(cur)


@app.route("/migrate")
def run_migrations():
    migrate.run(cur)
    return render_template("migrate.html")


@app.route("/migrate_bank")
def run_bank_migrations():
    migrate_bank.run()
    return render_template("migrate.html")


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# Route for handling the login page logic
@app.route('/login_action', methods=['GET', 'POST'])
def login_action():
    error = None
    if request.method == 'POST':
        un, pw = request.form['username'].strip(), request.form['password']
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
        result = helpers.find_account(cur, un, hashed_pw)
        if result:
            session["uid"] = helpers.get_uid(cur, un)[0]
            return redirect(url_for('home_dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = None
    if request.method == 'POST':
        un = request.form['username'].strip()
        pw = request.form['password']
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()  # hashes password, log into database
        fName = request.form['first_name']
        lName = request.form['last_name']
        bday_str = request.form['birthday']
        birthday = datetime.datetime.strptime(bday_str, '%Y-%m-%d').date()
        street_addr = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        email = request.form['email']

        if helpers.check_existing(cur, un, email):
            msg = 'Account already exists'
        elif not helpers.valid_email(email):
            msg = 'Invalid email address'
        elif not helpers.valid_username(un):
            msg = 'Invalid username. Must fit criteria'
        elif not helpers.valid_password(pw):
            msg = 'Invalid password. Must fit criteria'
        else:
            current_date = datetime.date.today()
            cur.execute(
                'INSERT INTO Users (username, password, first_name, last_name, birthday, street_address, city, state, '
                'zipcode, created_on, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (un, hashed_pw, fName, lName, birthday, street_addr, city, state, zipcode, current_date, email))
            conn.commit()
            msg = 'Registration Successful'
    return render_template('registrationPage.html', msg=msg)


@app.route("/logout")
def logout():
    session["uid"] = None
    return redirect("/")


@app.route("/profile")
def get_profile():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return profile.get_profile(cur)


@app.route("/edit_profile")
def edit_profile():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return profile.get_edit_profile()


@app.route("/change_username", methods=['GET', 'POST'])
def change_username():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return profile.change_username(cur, request.form, session.get("uid"))


@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return profile.change_password(cur, request.form, session.get("uid"))


@app.route("/change_address", methods=['GET', 'POST'])
def change_address():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return profile.change_address(cur, request.form, session.get("uid"))


@app.route('/bank', methods=['GET', 'POST'])
def bank_connect():
    msg = None
    uid = session.get("uid")
    connected = False
    if bank.check_connection(cur):
        connected = True
    elif request.method == 'POST':
        bank_name = request.form['bank_name']
        un = request.form['username'].strip()
        pw = request.form['password']
        last_4 = request.form['last_4']
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
        if bank.check_bank_account(cur, bank_name, un):
            msg = 'Account already exists'
        else:
            # insert into checking account table, bank table, and wallet table for user
            cur.execute(
                'INSERT INTO Bank (bank_name, username, password, connection_status, withdrawal_status, user_id,'
                'account_number) VALUES (%s, %s, %s, %s, %s, %s, %s)', (bank_name, un, hashed_pw, True, True, uid,
                                                                        last_4))
            account_id = bank.get_account_id(cur)
            cur.execute('INSERT INTO CheckingAccount (account_number, account_id, balance, last_donation) VALUES (%s,'
                        '%s, %s, %s)', (last_4.zfill(11), account_id, 1000, datetime.date.today()))
            cur.execute('INSERT INTO Wallet (balance, user_id) VALUES (%s, %s)', (0, uid))
            cur.execute('INSERT INTO UsersCharities (user_id, meals, red, heart, nyc, ny) '
                        'VALUES (%s, %s, %s, %s, %s, %s)', (uid, False, False, False, False, False))

            # insert into checking account table for bankAPI
            bank_cur = bank.connect()
            bank_cur.execute(
                'INSERT INTO CheckingAccount (account_number, account_id, balance, username, password) VALUES (%s, '
                '%s, %s, %s, %s)', (last_4.zfill(11), account_id, 1000, un, hashed_pw))
            bank_cur.close()
            msg = 'Connection Successful'
            connected = True
    return render_template('bank.html', msg=msg, connected=connected)


@app.route('/disconnect_bank', methods=['GET', 'POST'])
def disconnect_bank():
    uid = session.get("uid")
    account_id = bank.get_account_id(cur)
    wallet_id = wallet.get_wallet_id(cur)

    helpers.delete_transactions(cur, account_id)

    cur.execute('DELETE FROM CheckingAccount WHERE account_id = %s', (account_id,))
    cur.execute('DELETE FROM Bank WHERE user_id = %s', (uid,))
    cur.execute('DELETE FROM UsersCharities WHERE user_id = %s', (uid,))

    if not (1 <= uid <= 6):
        cur.execute('DELETE FROM Donation WHERE source_wallet_id = %s', (wallet_id,))
        cur.execute('DELETE FROM Wallet WHERE user_id = %s', (uid,))
        bank_cur = bank.connect()
        helpers.delete_transactions(bank_cur, account_id)
        bank_cur.execute('DELETE FROM CheckingAccount WHERE account_id = %s', (account_id,))
        bank_cur.close()
    return redirect(url_for('bank_connect'))


@app.route('/test', methods=['GET', 'POST'])
def test():
    transactions = bank.import_transactions(cur)
    if not transactions:
        return render_template("test.html", error="no transactions detected")
    wallet.store_transactions(cur, transactions)
    total = wallet.round_up(transactions)
    successful = bank.charge_bank(cur, total)
    if successful:
        successful = wallet.deposit_change(cur, total)
        if successful:
            wallet.update_last_donation(cur)
            return render_template("test.html")
        else:
            return render_template("test.html", error="unsuccessful")
    else:
        return render_template("test.html", error="unsuccessful")


@app.route('/wallet', methods=['GET', 'POST'])
def wallet_display():
    if not session.get("uid"):
        # if not there in the session then redirect to the login page
        return redirect(url_for('login'))
    return wallet.get_wallet(cur)


@app.route('/add_transaction1', methods=['GET', 'POST'])
# for new user with last 4 digits: 1111
def add_transaction1():
    bank_cur = bank.connect()
    sql = f"INSERT INTO Transactions (source_account_number, destination_account_number, description, amount, " \
          f"date, type) " \
          f"VALUES ('00000001111', '19999999999', 'NBA', " \
          f"{20.6}, '{datetime.date.today()}', 'W')"
    bank_cur.execute(sql)
    bank_cur.close()
    return redirect(url_for('home_dashboard'))


@app.route('/add_transaction', methods=['GET', 'POST'])
# for user1
def add_transaction():
    bank_cur = bank.connect()
    sql = f"INSERT INTO Transactions (source_account_number, destination_account_number, description, amount, " \
          f"date, type) " \
          f"VALUES ('00000000005', '19999999999', 'NBA', " \
          f"{20.6}, '{datetime.date.today()}', 'W')"
    bank_cur.execute(sql)
    bank_cur.close()
    return redirect(url_for('home_dashboard'))


@app.route('/presentation', methods=['GET', 'POST'])
# use to show that requirements are working
# make sure to run only after bank has been connected
def presentation():
    bank_cur = bank.connect()
    username, password, account_number = bank.get_credentials(cur)
    checking_account = bank.get_checking_account(bank_cur, cur, username, password, account_number)
    bank.delete_last_transaction(bank_cur, checking_account)
    # reset wallet transactions and delete the extra ones caused by running /add_transaction
    bank_cur.execute("DELETE FROM Transactions WHERE description = 'Change For Change Transaction'")
    bank_cur.execute("DELETE FROM Transactions WHERE description = 'NBA'")
    # assure that checking account has funds
    account_id = bank.get_account_id(cur)
    sql0 = f"UPDATE CheckingAccount SET balance = {10000} WHERE account_id = '{account_id}' "
    bank_cur.execute(sql0)
    bank_cur.close()
    # delete local transactions to see if they get imported properly from Bank API
    sql1 = f"DELETE FROM Transactions;"
    cur.execute(sql1)
    # reset wallet balance
    wallet.update_wallet(cur, 0)
    # reset donations
    wallet_id = wallet.get_wallet_id(cur)
    sql2 = f"DELETE FROM Donation WHERE source_wallet_id = {wallet_id}"
    cur.execute(sql2)
    # everything ready to go
    msg = "Requirements ready to be tested. Please proceed to dashboard to test!"
    return render_template('test.html', msg=msg)


@app.route('/wallet_deposit', methods=['GET', 'POST'])
def wallet_deposit():
    charity_connected = False
    selected_charities = charity.chosen_charities(cur)
    if selected_charities:
        charity_connected = True
        selected_charities = ', '.join(selected_charities)
    msg = None
    balance = wallet.get_total(cur)
    if request.method == 'POST':
        last_4 = bank.get_last_four(cur)
        deposit = decimal.Decimal(request.form['deposit-amount'])
        account_id = bank.get_account_id(cur)
        # find checking account
        target = helpers.find_specific_account(last_4, account_id)
        if not target:
            msg = "Account cannot be found"

        else:
            resulting_balance = target[2] - deposit  # output error if negative
            if resulting_balance < 0:
                msg = "Insufficient funds found in checking account"
            # take money from checking account
            else:
                balance = wallet.wallet_transaction(cur, resulting_balance, account_id, last_4, deposit, True)
                if balance >= 50:  # Donate to the specific charities....
                    balance = wallet.automated_donation(cur, balance)
    donations = charity.get_donations(cur)
    wallet_transactions = wallet.recent_wallet_transactions(cur)
    return render_template('wallet.html', msg=msg, balance=balance, charity_connected=charity_connected,
                           selected_charities=selected_charities, donations=donations,
                           wallet_transactions=wallet_transactions)


@app.route('/wallet_withdraw', methods=['GET', 'POST'])
def wallet_withdraw():
    charity_connected = False
    selected_charities = charity.chosen_charities(cur)
    if selected_charities:
        charity_connected = True
        selected_charities = ', '.join(selected_charities)
    msg = None
    balance = wallet.get_total(cur)
    if request.method == 'POST':
        last_4 = bank.get_last_four(cur)
        withdraw = decimal.Decimal(request.form['withdraw-amount'])
        if withdraw > wallet.get_total(cur):
            msg = "Insufficient wallet funds"
        else:
            account_id = bank.get_account_id(cur)
            # find checking account
            target = helpers.find_specific_account(last_4, account_id)
            if not target:
                msg = "Account cannot be found"
            else:
                resulting_balance = target[2] + withdraw
                balance = wallet.wallet_transaction(cur, resulting_balance, account_id, last_4, withdraw, False)
    donations = charity.get_donations(cur)
    wallet_transactions = wallet.recent_wallet_transactions(cur)
    return render_template('wallet.html', msg=msg, balance=balance, charity_connected=charity_connected,
                           selected_charities=selected_charities, donations=donations,
                           wallet_transactions=wallet_transactions)


@app.route('/select_charities', methods=['GET', 'POST'])
def select_charities():
    return render_template("charity-select.html")


@app.route('/chosen_charities', methods=['GET', 'POST'])
def chosen_charities():
    msg = None
    balance = wallet.get_total(cur)
    charity_connected = False
    selected_charities = None
    if request.method == 'POST':
        selected_charities = request.form.getlist('charity[]')
        if not selected_charities:
            charity.reset_charities(cur)
            msg = "You have not chosen any charities. Default: Meals On Wheels"
        else:
            charity.change_charities(cur, selected_charities)
            charity_connected = True  # pass as a parameter to wallet.html
            selected_charities = ', '.join(charity.chosen_charities(cur))
    donations = charity.get_donations(cur)
    wallet_transactions = wallet.recent_wallet_transactions(cur)
    return render_template("wallet.html", balance=balance, charity_connected=charity_connected,
                           selected_charities=selected_charities, msg=msg, donations=donations,
                           wallet_transactions=wallet_transactions)


@app.route('/test2', methods=['GET', 'POST'])
def test2():
    wallet.recent_wallet_transactions(cur)
    return render_template('test.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
    cur.close()
