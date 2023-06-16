from flask import session
import wallet


def choose_charities(cur, selected_charities):
    try:
        uid = session.get("uid")
        charities_dict = {"meals": False, "red": False, "heart": False, "nyc": False, "ny": False}
        for charity in selected_charities:
            charities_dict[charity] = True
        sql = f"UPDATE UsersCharities SET meals = {charities_dict['meals']}, red = {charities_dict['red']}, " \
              f"heart = {charities_dict['heart']}, nyc = {charities_dict['nyc']}, ny = {charities_dict['ny']} " \
              f"WHERE user_id = {uid}"
        cur.execute(sql)
    except Exception as e:
        print("Error when choosing charities:", e)


def chosen_charities(cur):  # get chosen charities - use for splitting automated donations
    try:
        uid = session.get("uid")
        chosen = []
        charities_dict = {1: "Meals On Wheels", 2: "American Red Cross", 3: "American Heart Association", \
                          4: "NYC Department of Homeless Services", 5: "NY Blood Center"}
        sql = f"SELECT * FROM UsersCharities WHERE user_id = {uid}"
        cur.execute(sql)
        result = cur.fetchone()
        for ndx in range(len(result)):
            if result[ndx] and ndx != 0:
                chosen.append(charities_dict[ndx])
        return chosen
    except Exception as e:
        print("Error when getting chosen charities:", e)


def change_charities(cur, selected_charities):  # reset and then re-choose
    try:
        reset_charities(cur)
        choose_charities(cur, selected_charities)
    except Exception as e:
        print("Error when changing charities:", e)


def reset_charities(cur):  # set everything to false
    try:
        uid = session.get("uid")
        sql = f"UPDATE UsersCharities SET meals = {False}, red = {False}, " \
              f"heart = {False}, nyc = {False}, ny = {False} " \
              f"WHERE user_id = {uid}"
        cur.execute(sql)
    except Exception as e:
        print("Error when resetting charities:", e)


def get_donations(cur):  # use for wallet page now....
    try:
        wallet_id = wallet.get_wallet_id(cur)
        donations = []
        sql = f"SELECT * FROM Donation WHERE source_wallet_id = {wallet_id}"
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            donation_id = result[-3]
            cur.execute(f"SELECT name FROM Charity WHERE user_id = {donation_id}")
            name = cur.fetchone()[0]
            donations.append((name, result[-2], result[-1]))
        donations.reverse()
        return donations
    except Exception as e:
        print("Error when getting donations:", e)
