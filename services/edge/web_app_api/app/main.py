from flask import Flask, render_template, request, redirect, url_for
import flask_login
import login_manager
import datetime
from urllib.parse import urlparse
from forms import SignInForm
import requests
import sys

app = Flask(__name__)
app.secret_key = '&0n2%~pq0B=j8TS('

login_manager.login_manager.init_app(app)
login_manager.login_manager.login_view = 'signin'

users = {'burla': {'password': '1234'}}

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
        if form.password.data == users[username]['password']:
            user = login_manager.User()
            user.id = username
            flask_login.login_user(user)
            next = request.args.get('next')
            if not next or urlparse(next).netloc != '':
                next = url_for('dashboard')
            return redirect(next)

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
    return render_template('pages/dashboard.html')

@app.route('/devices')
@flask_login.login_required
def devices():
    webDevices = testDevices
    return render_template('pages/devices.html', webDevices=webDevices)

@app.route('/rules')
@flask_login.login_required
def rules():
    return render_template('pages/rules.html')

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)


## Testing variables
testDevices = [["test1", "1"],["test2", "2"],["test3", "3"],["test4", "4"],["test5", "5"],["test6", "6"],["test7", "7"],["test8", "8"],["test9", "9"],["test10", "10"],["test11", "11"],["test12", "12"],]