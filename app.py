from flask import Flask

#create an instance of flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"