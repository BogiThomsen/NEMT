from flask import Flask, render_template, request
import requests
import sys
app = Flask(__name__)

@app.route('/')
def index():
    r = requests.get("http://172.20.0.2:5100/api/getUser")
    return render_template('index.html', text=r.text)

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    json = {}
    json["username"] = "drunar"
    json["password"] = "mongo@meyer.service"
    json["access_token"] = "MongoMeyer"
    r = requests.post("http://172.20.0.2:5100/api/addUser", json=json)
    return render_template('index.html', text=r.raise_for_status())


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')