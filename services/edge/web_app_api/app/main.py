from flask import Flask, render_template, request, redirect, url_for
import flask_login
import login_manager
import requests
import sys

app = Flask(__name__)
app.secret_key = '&0n2%~pq0B=j8TS('

login_manager.login_manager.init_app(app)

users = {'burla': {'password': '1234'}}

@app.route('/signin', methods=['GET', 'POST'])
def login():
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

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/')
def index():
    #r = requests.get("http://172.19.0.1:8085/api/getUser")
    #return render_template('index.html', text=r.json())
    return 'Hello'

#@app.route('/addUser', methods=['GET', 'POST'])
#def addUser():
#    json = {}
#    json["username"] = "DRUNAR"
#    json["email"] = "e@mail.com"
#    r = requests.post("http://172.19.0.1:8085/api/addUser", json=json)
#    return render_template('index.html', text=r)


if __name__ == "__main__":
  app.run()