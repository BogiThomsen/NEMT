from flask import Flask, render_template, request, redirect, url_for
import flask_login
import login_manager
import datetime
import requests
import sys

app = Flask(__name__)
app.secret_key = '&0n2%~pq0B=j8TS('

login_manager.login_manager.init_app(app)

users = {'burla': {'password': '1234'}}

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    #if request.method == 'GET':
    #    return '''
    #           <form action='login' method='POST'>
    #            <input type='text' name='username' id='username' placeholder='username'/>
    #            <input type='password' name='password' id='password' placeholder='password'/>
    #            <input type='submit' name='submit'/>
    #           </form>
    #           '''

    if request.method == 'POST':
        username = request.form['username']
        if request.form['password'] == users[username]['password']:
            user = login_manager.User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('protected'))

    return render_template('auth/signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #register a user

    return render_template('auth/register.html')

@app.route('/signout')
def logout():
    flask_login.logout_user()
    return render_template('auth/logout.html')

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)
