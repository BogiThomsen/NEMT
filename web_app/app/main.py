from flask import Flask, render_template, request, redirect, url_for, flash
import flask_login
import login_manager
import datetime
from urllib.parse import urlparse
from forms import RegisterForm, SignInForm
import requests
import rule_parser
import uuid

app = Flask(__name__)
app.secret_key = '&0n2%~pq0B=j8TS('
url = "http://172.31.91.114"

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
        r = requests.post(url+':4900/v1/users/authenticate', json={'username': username, 'password': password})
        json = r.json()
        if r.status_code == 200:
            id = json['_id']
            access_token = json['accessToken']
            user = login_manager.User()
            user.id = id + ';' + access_token
            flask_login.login_user(user)
            next = request.args.get('next')
            if not next or urlparse(next).netloc != '':
                next = url_for('dashboard')
            return redirect(next)
        elif r.status_code == 404 or r.status_code == 400:
            flash('An error occurred when trying to sign in.', 'danger')
            return render_template('auth/signin.html', form=form)

    return render_template('auth/signin.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not flask_login.current_user.is_anonymous:
        return redirect(url_for('index'))

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        r = requests.post(url+':4900/v1/users', json={'username': username, 'password': password})
        if r.status_code == 200:
            flash('Your user was successfully created.', 'success')
            return redirect(url_for('signin'))
        elif r.status_code == 400:
            flash('An error occurred when trying to register.', 'danger')
            return render_template('auth/register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            r = requests.post(url+':4900/v1/users', json={'username': username, 'password': password})
            if r.status_code == 200:
                flash('Your user was successfully created.', 'success')
                return redirect(url_for('signin'))
            elif r.status_code == 400:
                flash('An error occurred when trying to register.', 'danger')
                return render_template('auth/register.html', form=form)
        else:
            return render_template('auth/register.html', form=form, was_validated='was-validated')

    return render_template('auth/register.html', form=form)

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
    split_id_access_token = flask_login.current_user.id.split(';')
    user_id = split_id_access_token[0]
    access_token = split_id_access_token[1]
    ur = requests.get(url+":4900/v1/users/{}".format(user_id), json={"accessToken": access_token, "data":{}})
    u = ur.json()
    userDevices = []
    if ur.status_code == 200 and 'devices' in u:
        userDevices = requests.get(url+":4900/v1/users/{}/devices".format(user_id), json={'accessToken': access_token, 'data': {"deviceList": u['devices']}}).json()

    return render_template('pages/devices.html', userDevices=userDevices)

@app.route('/devices/<string:id>', methods=["GET", "POST"])
@flask_login.login_required
def devices_id(id):
    split_id_access_token = flask_login.current_user.id.split(';')
    user_id = split_id_access_token[0]
    access_token = split_id_access_token[1]

    ur = requests.get(url+":4900/v1/users/{}".format(user_id), json={"accessToken": access_token, "data":{}})
    u = ur.json()

    userDevices = []
    if ur.status_code == 200 and 'devices' in u:
        userDevices = requests.get(url+":4900/v1/users/{}/devices".format(user_id), json={'accessToken': access_token, 'data': {"deviceList": u['devices']}}).json()

    userActions = []
    userSensors = []
    userDevice = None
    if ur.status_code == 200 and 'devices' in u:
        userDevices = requests.get(url+":4900/v1/users/{}/devices".format(user_id), json={'accessToken': access_token, 'data': {"deviceList": u['devices']}}).json()
        for device in userDevices:
            if device["_id"] == id:
                userDevice = device
            if device["_id"] == id and 'actions' in device:
                actions = [action.split(":")[1] for action in device['actions']]
                userActions = requests.get(url+":4900/v1/users/{0}/devices/{1}/actions".format(user_id, device["_id"]), json={'accessToken': access_token, 'data': {"actionList": actions}}).json()
            if device["_id"] == id and 'sensors' in device:
                sensors = [sensor.split(":")[1] for sensor in device['sensors']]
                userSensors = requests.get(url+":4900/v1/users/{0}/devices/{1}/sensors".format(user_id, device["_id"]), json={'accessToken': access_token, 'data': {"sensorList": sensors}}).json()

    if request.method == 'POST':
        split_id_access_token = flask_login.current_user.id.split(';')
        user_id = split_id_access_token[0]
        access_token = split_id_access_token[1]
        form = request.form
        if 'prettyName' in form:
            pretty_name = request.form['prettyName']
            r = requests.patch(url+":4900/v1/users/" + user_id + "/devices/" + id, json={'accessToken': access_token, 'data': {'prettyName': pretty_name}})
            if r.status_code == 200:
                flash('Your device has been updated.', 'success')
                return redirect(url_for('devices_id', id=id))
            elif r.status_code == 400 or r.status_code == 404:
                flash('An error occurred when trying to update your device.', 'danger')
        elif 'actionId' in form:
            action_id = request.form['actionId']
            r = requests.get(url+':4900/v1/users/' + user_id + '/devices/' + id + '/actions/' + action_id + '/activate', json={'accessToken': access_token})

            if r.status_code == 200:
                flash('The action was succesfully triggered.', 'success')
            elif r.status_code == 400:
                flash('An error occurred when trying to trigger the action.', 'danger')

    return render_template('pages/device.html', userDevices=userDevices, device=userDevice, userSensors=userSensors, userActions=userActions)

@app.route('/devices/<string:id>/delete', methods=["POST"])
@flask_login.login_required
def devices_id_delete(id):
    split_id_access_token = flask_login.current_user.id.split(';')
    user_id = split_id_access_token[0]
    access_token = split_id_access_token[1]
    r = requests.delete(url+":4900/v1/users/" + user_id + "/devices/" + id, json={'accessToken': access_token})

    if r.status_code == 200:
        flash('Your device has been deleted.', 'success')
        return redirect(url_for('devices'))
    elif r.status_code == 400 or r.status_code == 404:
        flash('An error occurred while trying to delete your device.', 'danger')
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
    rule = rule_parser.parse_rule(rule)
    rule = rule_parser.prettify_rule(rule, testDevices, testSensors, testActions)

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

# Test data. Only used for usability testing.
testDevices = [
    {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Livingroom controller", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]},
    {"id": "002", "device_token": "002", "name": "Controller002", "prettyname": "Bedroom aircondition", "sensors": ["003", "004"], "actions": ["003", "004", "006"], "rules": []},
    {"id": "001", "device_token": "003", "name": "Controller003", "prettyname": "Coffee machine", "sensors": ["999"], "actions": [], "rules": []},
]

testSensors = [
    {"id": "001", "name": "Light001", "prettyname": "Livingroom light sensor", "value": "70", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "Temp001", "prettyname": "Livingroom temperature", "value": "21", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "Light002", "prettyname": "Bedroom light sensor", "value": "50", "timestamp": "11-12@12:31", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "Temp002", "prettyname": "Bedroom temperature", "value": "17", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "Temp999", "prettyname": "Coffee temperature", "value": "63", "timestamp": "11-12@09:11", "public": False, "access_tokens": ["1", "2"]}
]

testActions = [
    {"id": "001", "name": "LightOnLivingRoom", "prettyname": "Turn on livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "LightOffLivingRoom", "prettyname": "Turn off livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "LightOnBed", "prettyname": "Turn on bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "LightOffBed", "prettyname": "Turn off bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "HeatUpLivingRoom", "prettyname": "Increase livingroom temperature", "public": False, "access_tokens": ["1", "2"]},
    {"id": "006", "name": "CoolBed", "prettyname": "Cool off bedroom", "public": False, "access_tokens": ["1", "2"]},
    {"id": "007", "name": "TurnOnCoffee", "prettyname": "Turn on Coffee Machine", "public": False, "access_tokens": ["1", "2"]},
    {"id": "008", "name": "TurnOffCoffee", "prettyname": "Turn off Coffee Machine", "public": False, "access_tokens": ["1", "2"]}
]

testRules = [
    {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]},
    {"id": "002", "name": "Sunrise rule", "condition": "Controller001.Light003 > val.30", "invocations": ["Controller001.HeatUpLiv", "Controller002.LightOnBed"]},
]

testRule = {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]}

if __name__ == "__main__":
  app.run(host="0.0.0.0", port='5000', debug=True)