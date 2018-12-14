from flask import Flask, render_template, request
import requests
import sys
app = Flask(__name__)

@app.route('/')
def index():
    r = requests.get("http://172.19.0.1:8085/api/getUser")
    return render_template('index.html', text=r.json())

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    json = {}
    json["username"] = "DRUNAR"
    json["email"] = "e@mail.com"
    r = requests.post("http://172.19.0.1:8085/api/addUser", json=json)
    return render_template('index.html', text=r)


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')