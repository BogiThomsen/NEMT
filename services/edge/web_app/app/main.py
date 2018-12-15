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
        r = requests.post('http://web-app-api:5000/v1/users/authenticate', json={'username': username, 'password': password})
        #status_code = 200
        #json = {'id': '3', 'accessToken': 'ABC123'}
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
        r = requests.post('http://web-app-api:5000/v1/users', json={'username': username, 'password': password})
        status_code = 200
        if r.status_code == 200:
            livroomDevice = requests.post('http://device-access:5500/v1/users/' + r.json()['_id'] + '/devices', json={'name': livingroomDevice['name'], 'accessToken': uuid.uuid4().hex})
            bedDevice = requests.post('http://device-app:5500/v1/users/' + r.json()['_id'] + '/devices', json={'name': bedroomDevice['name'], 'accessToken': uuid.uuid4().hex})
            cofmacDevice = requests.post('http://device-access:5500/v1/users/' + r.json()['_id'] + '/devices', json={'name': coffeeMachineDevice['name'], 'accessToken': uuid.uuid4().hex})

            #livingroomSensors
            livroomSensors = []
            livroomSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': livingroomSensors[1]['name'], 'public': False}.json()))
            livroomSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': livingroomSensors[2]['name'], 'public': False}.json()))
            #livingroomActions
            livroomActions = []
            livroomActions.append = requests.post('http://action-access:5700/v1/actions', json={'name': livingroomActions[1]['name'], 'public': False}.json())
            livroomActions.append = requests.post('http://action-access:5700/v1/actions', json={'name': livingroomActions[2]['name'], 'public': False}.json())
            livroomActions.append = requests.post('http://action-access:5700/v1/actions', json={'name': livingroomActions[3]['name'], 'public': False}.json())
            # bedroomSensors
            bedSensors = []
            bedSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': bedroomSensors[1]['name'], 'public': False}.json()))
            bedSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': bedroomSensors[2]['name'], 'public': False}.json()))
            bedSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': bedroomSensors[3]['name'], 'public': False}.json()))
            # bedroomActions
            bedActions = []

            # coffeeSensors
            cofmacSensors = []
            cofmacSensors.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': coffeeSensors[1]['name'], 'public': False}.json()))
            # coffeeActions
            cofmacActions = []
            cofmacActions.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': coffeeActions[1]['name'], 'public': False}.json()))
            cofmacActions.append(requests.post('http://sensor-access:5600/v1/sensors', json={'name': coffeeActions[2]['name'], 'public': False}.json()))


            d1_request = requests.patch('http://device-access:5500/v1/' + livroomDevice['_id'], json={'_id':livroomDevice['_id'], 'deviceInfo':{'operation': 'add', 'sensor': livroomSensors, 'action': livroomSensors}}.json())
            d2_request = requests.patch('http://device-access:5500/v1/' + bedDevice['_id'], json={'_id':bedDevice['_id'], 'deviceInfo':{'operation': 'add', 'sensor': bedSensors, 'action': bedActions}}.json())
            d3_request = requests.patch('http://device-access:5500/v1/' + cofmacDevice['_id'], json={'_id':cofmacDevice['_id'], 'deviceInfo':{'operation': 'add', 'sensor': cofmacSensors, 'action': cofmacActions}}.json())

            user_patching = requests.patch('http://user-service:5200/v1/users/' + r['_id'], json={'operation':'add', 'device':[livroomDevice, bedDevice, cofmacDevice]})

            flash('Your user was successfully created.', 'success')
            return redirect(url_for('signin'))
        elif r.status_code == 400:
            print(r.json()["error"])
            flash('An error occurred when trying to register.', 'danger')
            return render_template('auth/register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            r = requests.post('http://web-app-api:5000/v1/users', json={'username': username, 'password': password})
            status_code = 200
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
    ur = requests.get("http://web-app-api:5000/v1/users/{}".format(user_id), json={"accessToken": access_token})
    u = ur.json()
    userDevices = []
    if ur.status_code == 200 and 'devices' in u:
        for device in u["devices"]:
            device_resp = requests.get("http://web-app-api:5000/v1/users/{0}/devices/{1}".format(user_id, device), json={"accessToken": access_token})
            userDevice = device_resp.json()
            userDevices.append(userDevice)



    # UI links all devices to their sensors and actions
    # Needed fields for Device: ["name"], ["prettyname"], ["sensors"], ["actions"]
    # Needed fields for Actions ["id"], ["prettyname"], ["public"]
    # Needed fields for Sensors ["id"], ["prettyname"], ["value"], ["public"]

    # Expected: all devices to a given user
    # Expected: all sensors to a given user

    return render_template('pages/devices.html', userDevices=userDevices)

@app.route('/devices/<string:id>', methods=["GET", "POST"])
@flask_login.login_required
def devices_id(id):
    split_id_access_token = flask_login.current_user.id.split(';')
    user_id = split_id_access_token[0]
    access_token = split_id_access_token[1]
    ur = requests.get("http://web-app-api:5000/v1/users/{}".format(user_id), json={"accessToken": access_token})
    u = ur.json()
    userDevices = []
    userActions = []
    userSensors = []

    if ur.status_code == 200 and 'devices' in u:
        for device in u["devices"]:
            device_resp = requests.get("http://web-app-api:5000/v1/users/{0}/devices/{1}".format(user_id, device),
                                       json={"accessToken": access_token})
            userDevice = device_resp.json()
            userDevices.append(userDevice)
            if userDevice["_id"] == id and 'actions' in userDevice:
                for action in userDevice["actions"]:
                    action = action.split(":")[1]
                    user_action = requests.get("http://web-app-api:5000/v1/users/{0}/devices/{1}/actions/{2}".format(user_id, id, action), json={"accessToken": access_token}).json()

                    userActions.append(user_action)
            if userDevice["_id"] == id and 'sensors' in userDevice:
                for sensor in userDevice["sensors"]:
                    sensor = sensor.split(":")[1]
                    user_sensor = requests.get("http://web-app-api:5000/v1/users/{0}/devices/{1}/sensors/{2}".format(user_id, id, sensor), json={"accessToken": access_token}).json()
                    userSensors.append(user_sensor)
    if request.method == 'POST':
        split_id_access_token = flask_login.current_user.id.split(';')
        user_id = split_id_access_token[0]
        access_token = split_id_access_token[1]
        form = request.form
        if 'prettyName' in form:
            pretty_name = request.form['prettyName']
            r = requests.patch("http://web-app:5000/users/" + user_id + "/devices/" + id, data={'accessToken': access_token, 'data': {'prettyname': pretty_name}})

        if r.status_code == 200:
            flash('Your device has been updated.', 'success')
            return redirect(url_for('devices_id', id=id))
        elif 'actionId' in form:
            action_id = request.form['actionId']
            r = requests.get('http://web-app-api:5000/v1/users/' + user_id + '/devices/' + id + '/actions/' + action_id + '/activate', data={'accessToken': access_token})
            status_code = 200

            if r.status_code == 200:
                flash('The action was succesfully triggered.', 'success')
            elif r.status_code == 400:
                flash('An error occurred when trying to trigger the action.', 'danger')


    device = testDevice
    # Expected: all actions to a given user

    return render_template('pages/device.html', userDevices=userDevices, device=device, userSensors=userSensors, userActions=userActions)

@app.route('/devices/<string:id>/delete', methods=["POST"])
@flask_login.login_required
def devices_id_delete(id):
    split_id_access_token = flask_login.current_user.id.split(';')
    user_id = split_id_access_token[0]
    access_token = split_id_access_token[1]
    r = requests.delete("http://web-app-api:5000/v1/users/" + user_id + "/devices/" + id, data={'accessToken': access_token})

    if r.status_code == 200:
        flash('Your device has been deleted.', 'success')
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

# "/devices" testing variables. May be deleted when web_app has been correctly integrated
testDevices = [
    {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Livingroom controller", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]},
    {"id": "002", "device_token": "002", "name": "Controller002", "prettyname": "Bedroom Aircondition", "sensors": ["003", "004"], "actions": ["003", "004", "006"], "rules": []},
    {"id": "001", "device_token": "003", "name": "Controller003", "prettyname": "Coffee Machine", "sensors": ["999"], "actions": [], "rules": []},
]

livingroomDevice = {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Livingroom controller", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]}

bedroomDevice = {"id": "002", "device_token": "002", "name": "Controller002", "prettyname": "Bedroom Aircondition", "sensors": ["003", "004"], "actions": ["003", "004", "006"], "rules": []}

coffeeMachineDevice = {"id": "001", "device_token": "003", "name": "Controller003", "prettyname": "Coffee Machine", "sensors": ["999"], "actions": [], "rules": []}

testSensors = [
    {"id": "001", "name": "Light001", "prettyname": "Livingroom light sensor", "value": "70", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "Temp001", "prettyname": "Livingroom Temperature", "value": "21", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "Light002", "prettyname": "Bedroom light sensor", "value": "50", "timestamp": "11-12@12:31", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "Temp002", "prettyname": "Bedroom Temperature", "value": "17", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "Temp999", "prettyname": "Coffe Temperature", "value": "63", "timestamp": "11-12@09:11", "public": False, "access_tokens": ["1", "2"]}
]

livingroomSensors = [
    {"id": "001", "name": "Light001", "prettyname": "Livingroom light sensor", "value": "70", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "Temp001", "prettyname": "Livingroom Temperature", "value": "21", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]}
]
bedroomSensors = [
    {"id": "003", "name": "Light002", "prettyname": "Bedroom light sensor", "value": "50", "timestamp": "11-12@12:31", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "Temp002", "prettyname": "Bedroom Temperature", "value": "17", "timestamp": "11-12@13:30", "public": False, "access_tokens": ["1", "2"]}
]
coffeeSensors = [
    {"id": "005", "name": "Temp999", "prettyname": "Coffe Temperature", "value": "63", "timestamp": "11-12@09:11", "public": False, "access_tokens": ["1", "2"]}
]

testActions = [
    {"id": "001", "name": "LightOnLivingRoom", "prettyname": "turn on livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "LightOffLivingRoom", "prettyname": "turn off livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "003", "name": "LightOnBed", "prettyname": "turn on bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "LightOffBed", "prettyname": "turn off bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "HeatUpLivingRoom", "prettyname": "increase livingroom temperature", "public": False, "access_tokens": ["1", "2"]},
    {"id": "006", "name": "CoolBed", "prettyname": "cool off bedroom", "public": False, "access_tokens": ["1", "2"]},
    {"id": "007", "name": "TurnOnCoffee", "prettyname": "Turn on Coffee Machine", "public": False, "access_tokens": ["1", "2"]},
    {"id": "008", "name": "TurnOffCoffee", "prettyname": "Turn off Coffee Machine", "public": False, "access_tokens": ["1", "2"]}
]

livingroomActions = [
    {"id": "001", "name": "LightOnLivingRoom", "prettyname": "turn on livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "002", "name": "LightOffLivingRoom", "prettyname": "turn off livingroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "005", "name": "HeatUpLivingRoom", "prettyname": "increase livingroom temperature", "public": False, "access_tokens": ["1", "2"]}
]
bedroomActions = [
    {"id": "003", "name": "LightOnBed", "prettyname": "turn on bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "004", "name": "LightOffBed", "prettyname": "turn off bedroom lights", "public": False, "access_tokens": ["1", "2"]},
    {"id": "006", "name": "CoolBed", "prettyname": "cool off bedroom", "public": False, "access_tokens": ["1", "2"]},
]
coffeeActions = [
    {"id": "007", "name": "TurnOnCoffee", "prettyname": "Turn on Coffee Machine", "public": False, "access_tokens": ["1", "2"]},
    {"id": "008", "name": "TurnOffCoffee", "prettyname": "Turn off Coffee Machine", "public": False, "access_tokens": ["1", "2"]}
]

testRules = [
    {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]},
    {"id": "002", "name": "Sunrise rule", "condition": "Controller001.Light003 > val.30", "invocations": ["Controller001.HeatUpLiv", "Controller002.LightOnBed"]},

]

testDevice = {"id": "001", "device_token": "001", "name": "Controller001", "prettyname": "Living Room", "sensors": ["001", "002"], "actions":["001", "002", "005"], "rules":[]}

testRule = {"id": "001", "name": "Sunset rule", "condition": "Controller002.Light002 < val.15", "invocations": ["Controller002.CoolBed", "Controller001.LightOnLiv"]}



if __name__ == "__main__":
  app.run(host="0.0.0.0", port='5000', debug=True)