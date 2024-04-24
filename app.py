from flask import Flask, render_template, session, url_for, redirect, request
from helper import checkuser, hashed_password
from flask_session import Session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
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
        {'username':'hasan','opponent': 'Farza', 'time': '12:30', 'result': 'Lost', 'exchange':-230},
        {'username':'hasan','opponent': 'Maryam', 'time': '13:00', 'result': 'Won', 'exchange': 102},
        {'username':'Farza','opponent': 'Hasan', 'time': '12:30', 'result': 'Won', 'exchange': 230},

    ]

messages = []

@socketio.on('message')
def handleMsg(msg):
    print('Message: '+msg)
    send(msg, broadcast = True)
    messages.append(msg)




@app.route('/fight')
def fight():
    return render_template("fight.html", messages = messages)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


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
        password = hashed_password(request.form.get("password"))

        
        if not username:
            return render_template("Apology.html", message = "Must enter username")
        elif not password:
            return render_template("Apology.html", message = "Must enter Password")
        else:
            hash = hashed_password(password) 
            # users = db.execute("SELECT * FROM users")
            message, value = checkuser(users, username, hash)
            if message != None:
                return render_template("Apology.html", message= message)
            else:
                session["user"] = username   #replace with user_id later
                my_duels = [duel for duel in duels if duel.get('username') == username]
                return render_template("index.html", username = username, duels = my_duels)
        
@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        if not username:
            return render_template("Apology.html", message = "Must enter username")
        elif not password:
            return render_template("Apology.html", message = "Must enter Password")
        elif not email:
            return render_template("Apology.html", message = "Must enter email")
        elif not confirmation:
            return render_template("Apology.html", message = "Must Enter confirmation password")
        elif password != confirmation:
            return render_template("Apology.html",message = "Passwords Don't match")
        else:
            hash = hashed_password(password)
            users.append({"username":username, "password":hash, "value":0})
            
            session["user"] = username  #replace with user_id later
            my_duels = [duel for duel in duels if duel.get('username') == username]
            return render_template("index.html", username = username, duels = my_duels)

@app.route("/index")
def index():
    """First page"""
    if 'user' not in session or not session.get('user'):
        return redirect('/')
    
    user= session["user"]
    my_duels = [duel for duel in duels if duel.get('username') == user]
    return render_template("index.html", username = user, duels = my_duels)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    socketio.run(app, host = '0.0.0.0', port = 5000, debug = True)