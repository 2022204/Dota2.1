from flask import Flask , request

app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return "Hello WOrld!"
    else:
        


if __name__ == "__main__":
    app.run()