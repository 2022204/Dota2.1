from flask import Flask, render_template, session, url_for, redirect, request
from helper import checkuser, hashed_password
app = Flask(__name__)

users = [{"username":"hasan","password":"qwe"},
         {"username":"ali","password":"123123"}]

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
            message = checkuser(users, username, hash)
            if message != None:
                return render_template("Apology.html", message= message)
            else:
                return render_template("index.html")
        
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
            users.append({"username":username, "password":hash})
            return render_template("index.html")
        

@app.route("/index.html",methods = ["GET","POST"])
def index():
    """First page"""
    return render_template("index.html", message = "LOGGED IN SUCCESSFULLY")
if __name__ == "__main__":
    app.run(debug = True)