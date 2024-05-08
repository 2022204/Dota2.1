from flask import Flask, render_template, session, url_for, redirect, request
from helper import checkuser, hashed_password, get_history, get_heroes, get_items
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
Session(app)
socketio = SocketIO(app)

users = [{"username":"hasan","password":"hasan", "value":123},
         {"username":"ali","password":"ali", "value":10},
         {"username":"farza","password":"farza","value":1234}]

duels = [
        {'username':'hasan','opponent': 'Murtaza', 'time': '12:00', 'result': 'Won', 'exchange':100},
        {'username':'hasan','opponent': 'farza', 'time': '12:30', 'result': 'Lost', 'exchange':-230},
        {'username':'hasan','opponent': 'Maryam', 'time': '13:00', 'result': 'Won', 'exchange': 102},
        {'username':'farza','opponent': 'Hasan', 'time': '12:30', 'result': 'Won', 'exchange': 230},
    ]

messages = []

@socketio.on('message')
def handleMsg(msg):
    print('Message: '+msg)
    send(msg, broadcast = True)
    messages.append(msg)


@app.route("/warrior")
def warriors():
    userid = session["user"]
    
    ## Select Warrior Ids from users inventory
    ## Select all items associate with the warriors
    ## Write them into details datatype
    details = []
    for hero in [h for h in my_heros if h["username"] == userid]:
        hero_details = {"heroname": hero["heroname"], "warrior_items": []}
        for warrior in [w for w in my_warriors if w["warriorid"] == hero["warriorid"]]:
            item = next(item for item in my_items if item["itemid"] == warrior["itemid"])
            hero_details["warrior_items"].append({"itemid": warrior["itemid"], "details": item})
        details.append(hero_details)

    return render_template("warriors.html", details = details)

@app.route('/trade', methods = ["GET","POST"])
def trade():
    return render_template('trade.html')
@app.route('/fight', methods = ["GET","POST"])
def fight():
    return render_template("fight.html", messages = messages)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

my_warriors = [
    {"warriorid": 1, "itemid": 1}, {"warriorid": 1, "itemid": 2},
    {"warriorid": 2, "itemid": 1}, {"warriorid": 2, "itemid": 3},
    {"warriorid": 3, "itemid": 2}, {"warriorid": 3, "itemid": 3}
]

items = [
    {"itemid": 1, "itemname":"item1","health": 200, "attack": 0, "damage": 0, "armor": 3,"price":20},
    {"itemid": 2, "itemname":"item2", "health": 0, "attack": 110, "damage": 230, "armor": 3,"price":2},
    {"itemid": 3, "itemname":"item3","health": 55, "attack": 55, "damage": 55, "armor": 5, "price":10}
]
@app.route('/sell', methods = ["GET","POST"])
def sell():
    ## Select Warrior Ids from users inventory
    ## Select all items associate with the warriors
    ## Write them into details datatype
    userid = session["user"]

    # warriors = SELECT warrior_id FROM Heros_owned Where user_id = userid ---> ALL Warriors owned
    # owned_items = SELECT items_id from Warriors where Warrior_id in warrior_id
    # items = SELECT * from items where item_id in owned_items;

    if request.method == "GET":
        return render_template("sell.html", items = items)
    else:
        item_id = int(request.form.get("item_id"))
        price = items[0]["price"]   #SELECT price from item where item_id = item_id    # find the price of item being sold.
        #Update user_money From users where user_id = user_id;           # add the money to user account 
        #Delete from warriors_owned where item_id = item_id;            # update the warriors_owned table
        # flash("SOLD SUCCESSFULLY")
        new_items = [item for item in items if item.get('itemid') != item_id]  
        print(new_items)
        return render_template("sell.html", items = new_items)


heroes = [
    {"heroid": 2, "health": 120, "attackspeed": 180, "Damage": 140, "armor": 7, "respawn time": 35, "price": 27},
    {"heroid": 3, "health": 90, "attackspeed": 220, "Damage": 160, "armor": 6, "respawn time": 25, "price": 30},
    {"heroid": 4, "health": 110, "attackspeed": 190, "Damage": 130, "armor": 8, "respawn time": 40, "price": 25},
    {"heroid": 5, "health": 100, "attackspeed": 210, "Damage": 170, "armor": 4, "respawn time": 28, "price": 33},
    {"heroid": 1, "health": 130, "attackspeed": 170, "Damage": 120, "armor": 9, "respawn time": 45, "price": 28}
]

items = [
    {"itemid": 1, "itemname":"item1","health": 200, "attack": 0, "damage": 0, "armor": 3,"price":20},
    {"itemid": 2, "itemname":"item2", "health": 0, "attack": 110, "damage": 230, "armor": 3,"price":2},
    {"itemid": 3, "itemname":"item3","health": 55, "attack": 55, "damage": 55, "armor": 5, "price":10}
]

@app.route('/buy_item',methods = ["POST","GET"])
def buy_item():
    user_id = session["user"]
    item_list = get_items(db.select_data(conn, f"SELECT * FROM items"))

    if request.method == "GET":
        return render_template("buy_item.html", items = item_list)
    else:
        item_id = int(request.form.get("item_id"))
        cost = db.select_data(conn, f"SELECT cost from items WHERE item_id = %s",(item_id, ))[0][0]
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
        if cash < cost:
            return render_template("Apology.html", messages = "NOT ENOUGH CASH!!!")
        
        cash -= cost

        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash, user_id))
        #insert into owned_warriors ('user_id','hero_id') VALUES (user_id, heroid)
        return redirect("\index")

@app.route('/buy_hero', methods = ["GET","POST"])
def buy_hero():
    user_id = session["user"]
    hero_list = get_heroes(db.select_data(conn, f"SELECT * FROM heroes"))

    if request.method == "GET":
        return render_template("buy_hero.html", heroes = hero_list)
    else:
        hero_id = int(request.form.get("hero_id"))
        cost = db.select_data(conn, f"SELECT cost from heroes WHERE hero_id = %s",(hero_id, ))[0][0]
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
        if cash < cost:
            return render_template("Apology.html", messages = "NOT ENOUGH CASH!!!")
        
        cash -= cost

        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash, user_id))
        #insert into owned_warriors ('user_id','hero_id') VALUES (user_id, heroid)
        return redirect("\index")



@app.route('/', methods = ["POST","GET"])
def main():
    if request.method == "GET":
        return render_template("homepage.html")
    else:
        return render_template("login.html")
    
@app.route('/login', methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        
        if not username:
            return render_template("Apology.html", message = "Must enter username")
        elif not password:
            return render_template("Apology.html", message = "Must enter Password")
        else:
            hash = hashed_password(password) 
            user_id = db.select_data(conn, f"SELECT user_id from users where username = %s AND password = %s", (username, hash))
            if len(user_id) == 0:
                return render_template("Apology.html", message = "Username/ Password doesn't match")
            else:
                session["user"] = user_id[0][0]
                history = get_history(db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (session["user"],)))

                return render_template("index.html", username = username, duels = history)
        

@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return render_template("Apology.html", message = "Must enter username")
        elif not password:
            return render_template("Apology.html", message = "Must enter Password")
        elif not confirmation:
            return render_template("Apology.html", message = "Must Enter confirmation password")
        elif password != confirmation:
            return render_template("Apology.html",message = "Passwords Don't match")
        else:
            hash = hashed_password(password)

            data = {
            "INSERT INTO users (username, password, gold) VALUES (%s, %s, %s)": [
                (username, hash, 1000)
            ]
        }
            table = "users"
            
            db.insert_data(conn, table, data)

            row = db.select_data(conn, f"SELECT user_id FROM users where username = %s AND password = %s",(username, password))
            session["user"] = row[0][0]
            
            return render_template("index.html", username = username, duels = [])


@app.route("/index")
def index():
    """First page"""
    if 'user' not in session or not session.get('user'):
        return redirect('/')
    
    user= session["user"]

    history = get_history(db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (session["user"],)))

    return render_template("index.html", username = user, duels = history)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



if __name__ == "__main__":
    socketio.run(app, host = '0.0.0.0', port = 5000, debug = True)