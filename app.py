from flask import Flask, render_template, session, url_for, redirect, request
from helper import checkuser, hashed_password
app = Flask(__name__)

app.secret_key = "dota2.1"

users = [{"username":"hasan","password":"qwe", "value":123},
         {"username":"ali","password":"123123", "value":10}]

@app.route('/', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)

        if not username:
            return render_template("Apology.html", message = "Must enter username")
        elif not password:
            return render_template("Apology.html", message = "Must enter Password")
        else:
            hash = hashed_password(password) 
            message, value = checkuser(users, username, hash)
            if message != None:
                return render_template("Apology.html", message= message)
            else:
                session["user"] = username   #replace with user_id later
                return render_template("index.html", username = username, password = hash, value = value)
        
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
            users.append({"username":username, "password":hash, "value":0})
            session["user"] = username  #replace with user_id later
            return render_template("index.html", username = username, password = hash, value = 0)

        

@app.route("/index.html",methods = ["GET","POST"])
def index():
    """First page"""
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)