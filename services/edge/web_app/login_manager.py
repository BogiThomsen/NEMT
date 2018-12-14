import flask_login
import requests

login_manager = flask_login.LoginManager()

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(id_access_token):
    split_id_access_token = id_access_token.split(';')
    id = split_id_access_token[0]
    access_token = split_id_access_token[1]

    #r = requests.get('127.0.0.1:5000/v1/users/' + id, data={'accessToken': access_token})

    status_code = 200

    if status_code == 200:
        user = User()
        user.id = id + ';' + access_token
        return user
    elif status_code == 404:
        return None

'''
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
'''
