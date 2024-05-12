from flask import Flask, render_template, session, url_for, redirect, request
from helper import (
    checkuser,
    hashed_password,
    get_history,
    get_heroes,
    get_items,
    get_items_by_ids,
    get_tradeOffers,
    get_users,
    get_challenges,
    merge_items_by_challenge,
)
from flask_session import Session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import database_updated_file as db
import os
from dotenv import load_dotenv

load_dotenv(".env.local")
conn = db.establish_connection(os.getenv("uri"))
app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"]
Session(app)
socketio = SocketIO(app)
messages = []


@socketio.on("message")
def handleMsg(msg):
    print("Message: " + msg)
    send(msg, broadcast=True)
    messages.append(msg)


@app.route("/trade", methods=["GET", "POST"])
def handle_trade():
    user_id = session["user"]
    if request.method == "POST":
        action = request.form.get("action")

        if action == "offer_trade":
            offered_to_user_id = request.form.get("user_id")
            hero_id = request.form.get("hero_id")
            gold = int(request.form.get("gold"))
            data = {
                "INSERT INTO tradeOffers (user_id, hero_id, offered_to, gold, status) VALUES (%s, %s, %s,%s,%s)": [
                    (user_id, hero_id, offered_to_user_id, gold, "pending")
                ]
            }
            table = "tradeOffers"
            db.insert_data(conn, table, data)

        elif action == "accept_trade":
            offerer_user_id = request.form.get("user_id")
            hero_id = request.form.get("hero_id")
            cost = int(request.form.get("gold"))
            not_sold = db.select_data(
                conn,
                f"""SELECT EXISTS(
                SELECT 1 FROM Userheroes
                WHERE user_id = %s AND hero_id = %s
                )""",
                (offerer_user_id, hero_id),
            )
            if not not_sold:
                db.update_data(
                    conn,
                    f"UPDATE tradeOffers SET status = 'accepted' WHERE user_id = %s AND hero_id = %s AND offered_to = %s AND status = 'pending'",
                    (offerer_user_id, hero_id, user_id),
                )
                return render_template(
                    "Apology.html", message="Sorry. This hero is NO longer available."
                )
            have_hero = db.select_data(
                conn,
                f"""SELECT EXISTS (
                SELECT 1
                FROM userheroes
                WHERE user_id = %s AND hero_id = %s
                )""",
                (user_id, hero_id),
            )[0][0]
            print(have_hero)
            if have_hero:
                return render_template(
                    "Apology.html",
                    message="You already have this hero. Can't buy multiple heros",
                )

            cash = db.select_data(
                conn, f"SELECT gold from users where user_id = %s", (user_id,)
            )[0][0]
            if cash < cost:
                return render_template("Apology.html", messages="NOT ENOUGH CASH!!!")

            db.update_data(
                conn,
                f"Update users SET gold = %s where user_id = %s",
                ((cash - cost), user_id),
            )
            db.update_data(
                conn,
                f"Update users SET gold = %s where user_id = %s",
                ((cash + cost), offerer_user_id),
            )

            data = {
                "INSERT INTO UserHeroes (user_id, hero_id) VALUES (%s, %s)": [
                    (user_id, hero_id)
                ]
            }
            table = "Userheroes"

            db.insert_data(conn, table, data)
            db.delete_data(
                conn,
                f"DELETE FROM UserHeroes WHERE user_id = %s AND hero_id = %s",
                (offerer_user_id, hero_id),
            )
            db.update_data(
                conn,
                f"UPDATE tradeOffers SET status = 'accepted' WHERE user_id = %s AND hero_id = %s AND offered_to = %s AND status = 'pending'",
                (offerer_user_id, hero_id, user_id),
            )
            db.update_data(
                conn,
                f"UPDATE tradeOffers SET status = 'sold' WHERE user_id = %s AND hero_id = %s AND offered_to != %s AND status != 'accepted'",
                (offerer_user_id, hero_id, user_id),
            )

        elif action == "reject_trade":
            user_id_offer = request.form.get("user_id")
            hero_id = request.form.get("hero_id")
            gold = int(request.form.get("gold"))
            db.update_data(
                conn,
                f"UPDATE tradeOffers SET status = 'rejected' WHERE user_id = %s AND hero_id = %s AND offered_to = %s AND status = 'pending'",
                (user_id_offer, hero_id, user_id),
            )

        return redirect("/index")

    elif request.method == "GET":
        offers = get_tradeOffers(
            db.select_data(
                conn,
                f"""SELECT 
  t.user_id, t.hero_id,
  u1.username AS offerer_username, 
  h.name as hero_name, 
  t.gold, t.status, u2.username
FROM 
  tradeOffers as t
  JOIN users as u1 ON t.user_id = u1.user_id 
  JOIN heroes as h ON t.hero_id = h.hero_id
  JOIN users as u2 on t.offered_to = u2.user_id
  WHERE t.offered_to = %s and t.status = 'pending'""",
                (user_id,),
            )
        )
        cash = db.select_data(
            conn, f"SELECT gold from users where user_id = %s", (user_id,)
        )[0][0]

        heros = get_heroes(
            db.select_data(
                conn,
                f"SELECT * FROM heroes WHERE hero_id IN (SELECT hero_id FROM Userheroes WHERE user_id = %s)",
                (user_id,),
            )
        )
        users = get_users(
            db.select_data(conn, f"SELECT * FROM users WHERE user_id != %s", (user_id,))
        )
        finalized_offers = get_tradeOffers(
            db.select_data(
                conn,
                f"""SELECT 
  t.user_id, t.hero_id,
  u1.username AS offerer_username, 
  h.name as hero_name, 
  t.gold, t.status, u2.username
FROM 
  tradeOffers as t
  JOIN users as u1 ON t.user_id = u1.user_id 
  JOIN heroes as h ON t.hero_id = h.hero_id
  JOIN users as u2 on t.offered_to = u2.user_id
  WHERE (t.offered_to = %s OR t.user_id = %s) and t.status != 'pending'""",
                (user_id, user_id),
            )
        )
        return render_template(
            "trade.html",
            trade_offers=offers,
            gold=cash,
            users=users,
            heros=heros,
            other_offers=finalized_offers,
        )


@app.route("/fight", methods=["POST", "GET"])
def fight():
    user_id = session["user"]
    cash = db.select_data(
        conn, f"SELECT gold from users where user_id = %s", (user_id,)
    )[0][0]

    if request.method == "POST":
        action = request.form["action"]

        if action == "accept_challenge":
            challenge_id = request.form["challenge_id"]
            challenger_id = request.form["challenger_id"]
            opponent_hero_id = request.form["opponent_hero_id"]
            gold = request.form["gold"]
            items = [
                request.form["item1"],
                request.form["item2"],
                request.form["item3"],
            ]
            print(challenger_id, opponent_hero_id, items)
            challenger_cash = db.select_data(
                conn, f"SELECT gold FROM users WHERE user_id = %s", (challenger_id,)
            )[0][0]

            if challenger_cash < gold:
                db.delete_data(
                    conn,
                    f"DELETE FROM challenge_items WHERE challenge_id = %s",
                    (challenge_id,),
                )
                db.delete_data(
                    conn,
                    f"DELETE FROM challenges WHERE challenge_id = %s",
                    (challenge_id,),
                )
                return render_template(
                    "Apology.html",
                    message="Challenge no longer available. Request declined",
                )


        elif action == "challenge":
            hero_id = request.form["hero"]
            items = request.form.getlist("items[]")
            defender_id = request.form["user"]
            gold = int(request.form["gold"])

            if gold > cash:
                return render_template(
                    "Apology.html", message="You don't have enough gold"
                )

            if len(items) > 3:
                return render_template(
                    "Apology.html", message="Only up to 3 items are allowed"
                )

            data = {
                "INSERT INTO challenges (challenger_id, hero_id, defender_id, gold, status) VALUES (%s, %s, %s,%s,%s)": [
                    (user_id, hero_id, defender_id, gold, "pending")
                ]
            }
            table = "challenges"
            db.insert_data(conn, table, data)

            challenge_id = db.select_data(
                conn,
                f"SELECT challenge_id FROM challenges WHERE challenger_id = %s AND hero_id = %s AND defender_id = %s AND status = 'pending'",
                (user_id, hero_id, defender_id),
            )[0][0]

            for item in items:
                data = {
                    "INSERT INTO challenge_items (challenge_id, user_id, item_id) VALUES (%s, %s, %s)": [
                        (challenge_id, user_id, int(item)),
                    ]
                }
                table = "challenge_items"
                db.insert_data(conn, table, data)

        return redirect("/index")
    else:
        my_heroes = get_heroes(
            db.select_data(
                conn,
                f"SELECT * FROM heroes WHERE hero_id IN (SELECT hero_id FROM Userheroes WHERE user_id = %s)",
                (user_id,),
            )
        )
        my_items = get_items(
            db.select_data(
                conn,
                f"SELECT * from items WHERE item_id in (SELECT item_id FROM UserItems Where user_id = %s)",
                (user_id,),
            )
        )
        users = get_users(
            db.select_data(
                conn,
                f"SELECT * FROM users where user_id IN (SELECT user_id from users where user_id != %s)",
                (user_id,),
            )
        )
        my_challenges = merge_items_by_challenge(
            get_challenges(
                db.select_data(
                    conn,
                    f"""SELECT 
    u1.username, 
    h1.name AS hero_name, 
    c.hero_id, 
    c.gold, 
    c.challenger_id, 
    c.challenge_id,
    I.name AS item_name, 
    ci.item_id 
FROM 
    challenges AS c
JOIN 
    users AS u1 ON u1.user_id = c.challenger_id 
JOIN 
    heroes AS h1 ON h1.hero_id = c.hero_id
JOIN 
    challenge_items AS ci ON c.challenge_id = ci.challenge_id
JOIN 
    items AS I ON ci.item_id = I.item_id
WHERE 
    c.defender_id = %s""",
                    (user_id,),
                )
            )
        )

        return render_template(
            "fight.html",
            users=users,
            heroes=my_heroes,
            items=my_items,
            challenges=my_challenges,
            gold=cash,
        )


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/sell", methods=["GET", "POST"])
def sell():
    user_id = session["user"]

    items = get_items(
        db.select_data(
            conn,
            "SELECT * FROM items WHERE item_id IN (SELECT item_id FROM UserItems WHERE user_id = %s)",
            (user_id,),
        )
    )

    cash = db.select_data(
        conn, f"SELECT gold from users where user_id = %s", (user_id,)
    )[0][0]
    if request.method == "GET":
        return render_template("sell.html", items=items, gold=cash)
    else:
        item_id = int(request.form.get("item_id"))

        price = db.select_data(
            conn, f"SELECT cost FROM items WHERE item_id = %s", (item_id,)
        )[0][0]
        db.update_data(
            conn,
            f"Update users SET gold = %s WHERE user_id = %s",
            ((cash + price), user_id),
        )
        db.delete_data(
            conn,
            f"DELETE FROM UserItems WHERE user_id = %s AND item_id = %s",
            (user_id, item_id),
        )
        return redirect("/index")


@app.route("/buy_item", methods=["POST", "GET"])
def buy_item():
    user_id = session["user"]
    item_list = get_items(
        db.select_data(
            conn,
            f"SELECT * FROM items WHERE item_id NOT IN (SELECT item_id FROM UserItems WHERE user_id = %s)",
            (user_id,),
        )
    )
    if request.method == "GET":
        cash = db.select_data(
            conn, f"SELECT gold from users where user_id = %s", (user_id,)
        )[0][0]
        return render_template("buy_item.html", items=item_list, gold=cash)
    else:
        item_id = int(request.form.get("item_id"))
        cost = db.select_data(
            conn, f"SELECT cost from items WHERE item_id = %s", (item_id,)
        )[0][0]
        cash = db.select_data(
            conn, f"SELECT gold from users where user_id = %s", (user_id,)
        )[0][0]
        if cash < cost:
            return render_template("Apology.html", messages="NOT ENOUGH CASH!!!")

        cash -= cost

        db.update_data(
            conn, f"Update users SET gold = %s where user_id = %s", (cash, user_id)
        )
        data = {
            "INSERT INTO UserItems (user_id, item_id) VALUES (%s, %s)": [
                (user_id, item_id)
            ]
        }
        table = "UserItems"
        db.insert_data(conn, table, data)

        db.update_data(
            conn, f"Update users SET gold = %s where user_id = %s", (cash, user_id)
        )

        return redirect("/index")


@app.route("/buy_hero", methods=["GET", "POST"])
def buy_hero():
    user_id = session["user"]
    hero_list = get_heroes(
        db.select_data(
            conn,
            f"SELECT * FROM heroes WHERE hero_id NOT IN (SELECT hero_id FROM UserHeroes WHERE user_id = %s)",
            (user_id,),
        )
    )

    if request.method == "GET":
        cash = db.select_data(
            conn, f"SELECT gold from users where user_id = %s", (user_id,)
        )[0][0]
        return render_template("buy_hero.html", heroes=hero_list, gold=cash)
    else:
        hero_id = int(request.form.get("hero_id"))
        cost = db.select_data(
            conn, f"SELECT cost from heroes WHERE hero_id = %s", (hero_id,)
        )[0][0]
        cash = db.select_data(
            conn, f"SELECT gold from users where user_id = %s", (user_id,)
        )[0][0]
        if cash < cost:
            return render_template("Apology.html", messages="NOT ENOUGH CASH!!!")

        cash -= cost

        db.update_data(
            conn, f"Update users SET gold = %s where user_id = %s", (cash, user_id)
        )
        data = {
            "INSERT INTO UserHeroes (user_id, hero_id) VALUES (%s, %s)": [
                (user_id, hero_id)
            ]
        }
        table = "Userheroes"

        db.insert_data(conn, table, data)

        return redirect("/index")


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "GET":
        return render_template("homepage.html")
    else:
        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("Apology.html", message="Must enter username")
        elif not password:
            return render_template("Apology.html", message="Must enter Password")
        else:
            hash = hashed_password(password)
            user_id = db.select_data(
                conn,
                f"SELECT user_id from users where username = %s AND password = %s",
                (username, hash),
            )
            if user_id == None:
                return render_template(
                    "Apology.html", message="Username/ Password doesn't match"
                )
            else:
                session["user"] = user_id[0][0]
                history = get_history(
                    db.select_data(
                        conn,
                        f"SELECT * from history WHERE user_id = %s",
                        (session["user"],),
                    )
                )

                return redirect("/index")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return render_template("Apology.html", message="Must enter username")
        elif not password:
            return render_template("Apology.html", message="Must enter Password")
        elif not confirmation:
            return render_template(
                "Apology.html", message="Must Enter confirmation password"
            )
        elif password != confirmation:
            return render_template("Apology.html", message="Passwords Don't match")
        else:
            hash = hashed_password(password)

            exists = db.select_data(
                conn,
                f"""SELECT EXISTS (
                SELECT 1
                FROM users
                WHERE username = %s
                )""",
                (username,),
            )[0][0]
            if exists:
                return render_template(
                    "Apology.html", message="This username already exists"
                )

            data = {
                "INSERT INTO users (username, password, gold) VALUES (%s, %s, %s)": [
                    (username, hash, 1000)
                ]
            }
            table = "users"

            db.insert_data(conn, table, data)

            row = db.select_data(
                conn,
                f"SELECT user_id FROM users where username = %s AND password = %s",
                (username, password),
            )
            session["user"] = row[0][0]

            return render_template("index.html", username=username, duels=[])


@app.route("/index")
def index():
    """First page"""
    if "user" not in session or not session.get("user"):
        return redirect("/login")

    user_id = session["user"]

    history = get_history(
        db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (user_id,))
    )
    cash = db.select_data(
        conn, "SELECT gold from users where user_id = %s", (user_id,)
    )[0][0]

    username = db.select_data(
        conn, "SELECT username FROM users where user_id = %s", (user_id,)
    )[0][0]

    return render_template("index.html", username=username, duels=history, gold=cash)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
