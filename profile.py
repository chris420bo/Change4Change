from flask import render_template, session, request
import helpers
import hashlib
# from datetime import date
import charity


def get_profile(cur):
    uid = session.get("uid")

    # get name
    name = helpers.get_name(cur)

    # get member initiation date
    initiation_date = get_initiation_date(cur, uid)

    # get favorite charities
    favorite_charities = get_favorite_charities(cur, uid)

    if not favorite_charities:
        favorite_charities = ["Meals On Wheels"]

    # get top 5 donations
    top_donations = get_top_donations(cur, uid)

    # get last donation
    last_donation = get_last_donation(cur, uid)

    return render_template("profile.html", name=name, initiation_date=initiation_date,
                           favorite_charities=favorite_charities, top_donations=top_donations,
                           last_donation=last_donation)


def get_edit_profile():
    uid = session.get("uid")
    return render_template("edit_profile.html")


def get_initiation_date(cur, uid):
    try:
        sql = f"SELECT created_on FROM Users WHERE user_id = '{uid}'"
        cur.execute(sql)
        res = cur.fetchall()[0][0]
        return res.strftime('%B %d, %Y')
    except Exception as e:
        print("Error getting the initiation date:", e)
        return None


def get_favorite_charities(cur, uid):
    try:
        res = charity.chosen_charities(cur)
        return res
    except Exception as e:
        print("Error getting favorite charities:", e)
        return None


def get_top_donations(cur, uid):
    try:
        sql = f"SELECT Charity.name, Donation.amount " \
              f"FROM ((Donation JOIN Wallet ON Donation.source_wallet_id = Wallet.wallet_id) " \
              f" JOIN Charity ON Donation.destination_charity_id = Charity.user_id) " \
              f"WHERE Wallet.user_id = '{uid}' " \
              f"ORDER BY Donation.amount DESC " \
              f"LIMIT 5"
        cur.execute(sql)
        res = cur.fetchall()
        return res
    except Exception as e:
        print("Error getting top donations:", e)
        return None


def get_last_donation(cur, uid):
    try:
        sql = f"SELECT Donation.created_on, Charity.name, Donation.amount " \
              f"FROM ((Donation JOIN Wallet ON Donation.source_wallet_id = Wallet.wallet_id) " \
              f"JOIN Charity ON Donation.destination_charity_id = Charity.user_id) " \
              f"WHERE Wallet.user_id = {uid} " \
              f"ORDER BY Donation.created_on DESC " \
              f"LIMIT 1"
        cur.execute(sql)
        res = cur.fetchall()[0]
        return res
    except Exception as e:
        print("Error getting top donations:", e)
        return None


def change_username(cur, form, uid):
    old_username = form["old_username"].strip()
    new_username = form["new_username"].strip()

    # check if they are the same
    if old_username == new_username:
        return render_template("edit_profile.html", error="Usernames are the same")

    # check if valid
    if len(new_username) > 10 or len(new_username) < 2:
        return render_template("edit_profile.html", error="New username must be more than 1 character and under "
                                                          "10 characters")
    if not new_username.isalnum():
        return render_template("edit_profile.html", error="New username can only contain letters and numbers")

    # check if old username is correct
    try:
        # change username
        sql = f"SELECT username FROM Users WHERE user_id = {uid}"
        cur.execute(sql)
        res = cur.fetchall()[0]
        if not res or res[0] != old_username:
            return render_template("edit_profile.html", error="Old username is incorrect")
    except Exception as e:
        return render_template("edit_profile.html", error="Old username is incorrect")

    try:
        # change username
        sql = f"UPDATE Users " \
              f"SET username = '{new_username}' " \
              f"WHERE user_id = {uid} AND username = '{old_username}'; "
        cur.execute(sql)
        return render_template("edit_profile.html", success=f"Username successfully changed to {new_username}!")
    except Exception as e:
        print(e)
        return render_template("edit_profile.html", error="Error changing username")


def change_password(cur, form, uid):
    old_password = form["old_password"].strip()
    new_password = form["new_password"].strip()
    retype_password = form["retype_password"].strip()

    # check if they are the same
    if old_password == new_password:
        return render_template("edit_profile.html", error="Old and new passwords are the same")

    # check if valid
    if new_password != retype_password:
        return render_template("edit_profile.html", error="Passwords are not the same")

    if not helpers.valid_password(new_password):
        return render_template("edit_profile.html",
                               error="Passwords is not valid. Must contain: ")  # TODO: add what password must contian

    # check if old password is correct
    try:
        # change username
        sql = f"SELECT password FROM Users WHERE user_id={uid}"
        cur.execute(sql)
        res = cur.fetchall()[0][0]
    except Exception as e:
        print(e)
        return render_template("edit_profile.html", error="Error fetching old password")

    hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()

    if hashed_old_password != res:
        return render_template("edit_profile.html", error="Old password is incorrect")

    hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

    try:
        # change username
        sql = f"UPDATE Users " \
              f"SET password = '{hashed_new_password}' " \
              f"WHERE user_id = {uid} AND password = '{hashed_old_password}'; "
        cur.execute(sql)
        return render_template("edit_profile.html", success=f"Password successfully changed!")
    except Exception as e:
        print(e)
        return render_template("edit_profile.html", error="Error changing password")


def change_address(cur, form, uid):
    street_address = form["street_address"].strip()
    city = form["city"].strip()
    state = form["state"].strip()
    zipcode = form["zipcode"].strip()

    try:
        # change username
        sql = f"UPDATE Users " \
              f"SET street_address = '{street_address}', " \
              f"city = '{city}', " \
              f"state = '{state}', " \
              f"zipcode = '{zipcode}' " \
              f"WHERE user_id = {uid}; "
        cur.execute(sql)
        return render_template("edit_profile.html", success=f"Address successfully changed!")
    except Exception as e:
        print(e)
        return render_template("edit_profile.html", error="Error changing address")
