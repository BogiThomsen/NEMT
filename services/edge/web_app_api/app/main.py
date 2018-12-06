from flask import Flask, render_template, request
import requests
import sys
app = Flask(__name__)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
session = requests.Session()
session.trust_env = False

@app.route('/')
def index():
    r = session.get("http://user-service:5100/api/getUser", headers=headers)
    return render_template('index.html', text=r.json())

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    json = {}
    json["username"] = "drunar3"
    json["password"] = "mongo@meyer.service"
    json["access_token"] = "MongoMeyer"
    r = session.post("http://user-service:5100/api/addUser", json=json, headers=headers)
    return render_template('index.html', text=r)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')