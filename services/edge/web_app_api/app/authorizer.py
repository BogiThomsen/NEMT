import requests

def authorize(access_token):
    r = requests.post('http://user-service:5100/v1/users/authorize', data={'accessToken': access_token})

    if r.status_code == 200:
        return ''
    elif r.status_code == 401:
        return r.get_json().error
