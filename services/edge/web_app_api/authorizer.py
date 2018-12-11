import requests


def authorize(access_token):
    r = requests.post('http://user-service:5100/v1/users/authorize', data={'accessToken': access_token})

    if r.status_code == 200:
        return True
    elif r.status_code == 400:
        return False
