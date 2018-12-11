from flask import Flask, render_template, request, json
import requests
import sys
import urllib

app = Flask(__name__)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
session = requests.Session()
session.trust_env = False

@app.route('/', methods=['GET', 'DELETE'])
def index():
    username = "bogiergud"
    user_id = session.get("http://user-service:5100/api/users/getId/{}".format(username), headers=headers).text
    # Please find en bedre måde at fjerne quotes og html encodet newline(%0A)
    user_id = user_id.replace('\"', '').rstrip()
    user = session.get("http://user-service:5100/api/users/{}".format(user_id), headers=headers)

    return render_template('index.html', user=user.json(), id=user_id, delete="no")

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    json = {}
    json["username"] = "bogiergud"
    json["password"] = "bogi@er.nice"
    json["access_token"] = "sudo giv mig adgang"
    r = session.post("http://user-service:5100/api/users", json=json, headers=headers)
    return render_template('index.html', text=r)

@app.route('/patchUser', methods=['GET', 'POST', 'PATCH'])
def patchUser():
    user_id = session.get("http://user-service:5100/api/users/{}".format(username), headers=headers).text
    # Please find en bedre måde at fjerne quotes og html encodet newline(%0A)
    user_id = user_id.replace('\"', '').rstrip()

    json = {}
    json["userId"] = user_id
    json["operation"] = False
    json["username"] = "guderbogi"
    json["password"] = "nytpassword"
    json["device"] = "pissefeddeviceid!"
    json["rule"] = "DetErIkkeMigDerLaverReglerne"



    user = session.get("http://user-service:5100/api/users/{}".format(user_id), headers=headers)
    return render_template('index.html', text=user.json())


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')