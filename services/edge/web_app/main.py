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

    return render_template('pages/devices.html', userDevices=userDevices)

@app.route('/devices/<string:id>', methods=["GET", "POST"])
@flask_login.login_required
def devices_id(id):
    if request.method == "GET":
        device = testDevice
        userSensors = testSensors
        # Expected: all actions to a given user
        userActions = testActions

        return render_template('pages/device.html', device=testDevice, userSensors=userSensors, userActions=userActions)

    else:

        #r = requests.patch("http://web-app:5000/users/" + flask_login.current_user.id + "/devices/" + id, data={'accessToken': flask_login.current_user.access_token, 'data': {'prettyname': request.data.prettyName}})

#      if r.status_code == 200:
        flash('Your device has been updated.')
        return redirect(url_for('devices_id', id=id))

@app.route('/devices/<string:id>/delete', methods=["POST"])
@flask_login.login_required
def devices_id_delete(id):
    #r = requests.delete("http://web-app:5000/users/" + flask_login.current_user.id + "/devices/" + id, data={'accessToken': flask_login.current_user.access_token, 'data': {'userid':flask_login.current_user.id, 'deviceid':id}})

    #if r.status_code == 200:
    flash('Your device has been deleted.')
    return redirect(url_for('devices'))

@app.route('/rules')
@flask_login.login_required
def rules():

    userRules = testRules

    return render_template('pages/rules.html', userRules=userRules)

@app.route('/rules/<string:id>')
@flask_login.login_required
def rules_id(id):

    rule = testRule

    return render_template('pages/rule.html', rule=rule)

@app.route('/rules/new')
def rules_new():
    userSensors = testSensors
    userActions = testActions
    return render_template('pages/createrule.html', userSensors=userSensors, userActions=userActions)

@app.route('/')
def index():
    if flask_login.current_user.is_anonymous:
        return redirect(url_for('signin'))
    else:
        return redirect(url_for('dashboard'))

# "/devices" testing variables. May be deleted when web_app has been correctly integrated
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

testRules = [
    {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]},
    {"id": "002", "name": "Sunrise rule", "condition": "Controller001.Light003 > val.30", "invocations": ["Controller001.HeatUpLiv", "Controller002.LightOnBed"]},

]

testDevice = {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Living Room", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]}

testRule = {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]}



if __name__ == "__main__":
  app.run(debug=True)