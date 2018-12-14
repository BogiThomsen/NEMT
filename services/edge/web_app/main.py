from flask import Flask, render_template, request, redirect, url_for, flash
import flask_login
import login_manager
import datetime
from urllib.parse import urlparse
from forms import SignInForm
import requests

app = Flask(__name__)
app.secret_key = '&0n2%~pq0B=j8TS('

login_manager.login_manager.init_app(app)
login_manager.login_manager.login_view = 'signin'

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if not flask_login.current_user.is_anonymous:
        return redirect(url_for('index'))

    form = SignInForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #r = requests.post('127.0.0.1:5000/v1/users/authenticate', data={'username': username, 'password': password})
        status_code = 200
        json = {'id': '3', 'accessToken': 'ABC123'}

        if status_code == 200:
            id = json['id']
            access_token = json['accessToken']
            user = login_manager.User()
            user.id = id + ';' + access_token
            flask_login.login_user(user)
            next = request.args.get('next')
            if not next or urlparse(next).netloc != '':
                next = url_for('dashboard')
            return redirect(next)
        elif status_code == 400:
            pass

    return render_template('auth/signin.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    #register a user

    return render_template('auth/register.html')

@app.route('/signout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template('auth/logout.html')

@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    userSensors = testSensors
    userActions = testActions
    return render_template('pages/dashboard.html', userSensors=userSensors, userActions=userActions)

@app.route('/devices')
@flask_login.login_required
def devices():
    # UI links all devices to their sensors and actions
    # Needed fields for Device: ["name"], ["prettyname"], ["sensors"], ["actions"]
    # Needed fields for Actions ["id"], ["prettyname"], ["public"]
    # Needed fields for Sensors ["id"], ["prettyname"], ["value"], ["public"]

    # Expected: all devices to a given user
    userDevices = testDevices
    # Expected: all sensors to a given user
    userSensors = testSensors
    # Expected: all actions to a given user
    userActions = testActions
    return render_template('pages/devices.html', userDevices=userDevices, userSensors=userSensors, userActions=userActions)

@app.route('/rules')
@flask_login.login_required
def rules():
    return render_template('pages/rules.html')

@app.route('/rules/new')
def createrule():
    userSensors = testSensors
    userActions = testActions
    return render_template('pages/createrule.html', userSensors=userSensors, userActions=userActions)

@app.route('/')
def index():
    if flask_login.current_user.is_anonymous:
        return redirect(url_for('signin'))
    else:
        return redirect(url_for('dashboard'))

# "/devices" testing variables. May be deleted when "/devices" has been correctly implemented
testDevices = [
    {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Living Room", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]},
    {"id": "002", "device_token": "002", "name": "Controller002", "prettyname": "Bed Room", "sensors": ["003", "004"], "actions": ["003", "004", "006"], "rules": []},
    {"id": "001", "device_token": "003", "name": "Controller003", "prettyname": "Weather Station", "sensors": ["999"], "actions": [], "rules": []},

]

testSensors = [
    {"id": "001", "name": "Light001", "prettyname": "Livingroom light sensor", "value": "70", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "Temp001", "prettyname": "Livingroom Temperature", "value": "21", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "Light002", "prettyname": "Bedroom light sensor", "value": "50", "timestamp": "11-12@12:31", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "Temp002", "prettyname": "Bedroom Temperature", "value": "17", "timestamp": "11-12@13:30", "public": True, "access_tokens": ["1", "2"]},
    {"id": "999", "name": "Temp999", "prettyname": "Aalborg Temperature", "value": "25", "timestamp": "11-12@09:11", "public": True, "access_tokens": ["1", "2"]}
]

testActions = [
    {"id": "001", "name": "LightOnLiv", "prettyname": "turn on livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "LightOffLiv", "prettyname": "turn off livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "LightOnBed", "prettyname": "turn on bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "LightOffBed", "prettyname": "turn off bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "HeatUpLiv", "prettyname": "increase livingroom temperature", "public": False, "access_tokens": ["1", "2"]},
    {"id": "006", "name": "CoolBed", "prettyname": "cool off bedroom", "public": False, "access_tokens": ["1", "2"]}
]


if __name__ == "__main__":
  app.run(debug=True)