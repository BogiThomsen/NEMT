import requests

def authorize(access_token, userid):
    response = requests.post('http://user-service:5100/v1/users/authorize/{}'.format(userid), json={'accessToken': access_token})

    if response.status_code == 200:
        return ""
    else:
        return "error"
