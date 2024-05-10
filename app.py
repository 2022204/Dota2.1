from flask import Flask, render_template, session, url_for, redirect, request
from helper import checkuser, hashed_password, get_history, get_heroes, get_items, get_items_by_ids
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


messages = []

@socketio.on('message')
def handleMsg(msg):
    print('Message: '+msg)
    send(msg, broadcast = True)
    messages.append(msg)


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

@app.route('/sell', methods = ["GET","POST"])
def sell():
    user_id = session["user"]

    item_list = db.select_data(conn, f"SELECT item_id from UserItems WHERE user_id = %s", (user_id,))

    query, itemlist = get_items_by_ids(item_list)
    if query == None or itemlist == []:
        items = []
    else:
        items = get_items(db.select_data(conn, query, itemlist))
    cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
    if request.method == "GET":
        return render_template("sell.html", items = items, gold = cash)
    else:
        item_id = int(request.form.get("item_id"))
        price = db.select_data(conn, f"SELECT cost FROM items WHERE item_id = %s", (item_id, ))[0][0]
        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash + price, user_id))
        db.delete_data(conn,f"DELETE FROM UserItems where user_id = %s AND item_id = %s", (user_id, item_id))

        return redirect('/index')

@app.route('/buy_item',methods = ["POST","GET"])
def buy_item():
    user_id = session["user"]
    item_list = get_items(db.select_data(conn, f"SELECT * FROM items"))
    if request.method == "GET":
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
        return render_template("buy_item.html", items = item_list, gold = cash)
    else:
        item_id = int(request.form.get("item_id"))
        cost = db.select_data(conn, f"SELECT cost from items WHERE item_id = %s",(item_id, ))[0][0]
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
        if cash < cost:
            return render_template("Apology.html", messages = "NOT ENOUGH CASH!!!")
        
        cash -= cost

        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash, user_id))
        data = {
            "INSERT INTO UserItems (user_id, item_id) VALUES (%s, %s)": [
                (user_id, item_id)
            ]
        }
        table = "UserItems"
        db.insert_data(conn, table, data)

        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash, user_id))

        return redirect("/index")

@app.route('/buy_hero', methods = ["GET","POST"])
def buy_hero():
    user_id = session["user"]
    hero_list = get_heroes(db.select_data(conn, f"SELECT * FROM heroes"))

    if request.method == "GET":
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]      
        return render_template("buy_hero.html", heroes = hero_list, gold = cash)
    else:
        hero_id = int(request.form.get("hero_id"))
        cost = db.select_data(conn, f"SELECT cost from heroes WHERE hero_id = %s",(hero_id, ))[0][0]
        cash =  db.select_data(conn , f"SELECT gold from users where user_id = %s", (user_id, ))[0][0]
        if cash < cost:
            return render_template("Apology.html", messages = "NOT ENOUGH CASH!!!")
        
        cash -= cost

        db.update_data(conn, f"Update users SET gold = %s where user_id = %s",(cash, user_id))
        data = {
            "INSERT INTO UserHeroes (user_id, hero_id) VALUES (%s, %s)": [
                (user_id, hero_id)
            ]
        }
        table = "Userheroes"
            
        db.insert_data(conn, table, data)
        
        return redirect("/index")



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
            if user_id == None:
                return render_template("Apology.html", message = "Username/ Password doesn't match")
            else:
                session["user"] = user_id[0][0]
                history = get_history(db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (session["user"],)))

                return redirect("/index")
        

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
        return redirect('/login')
    
    user_id = session["user"]
    print("USER_ID: ",user_id)

    history = get_history(db.select_data(conn, f"SELECT * from history WHERE user_id = %s", (user_id,)))
    print(history)
    cash =  db.select_data(conn , "SELECT gold from users where user_id = %s", (user_id, ))
    print(cash)

    username = db.select_data(conn, "SELECT username FROM users where user_id = %s",(user_id,))
    print(username)
    return render_template("index.html", username = username[0][0], duels = history, gold = cash[0][0])


@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    return redirect("/login")



if __name__ == "__main__":
    socketio.run(app, host = '0.0.0.0', port = 5000, debug = True)