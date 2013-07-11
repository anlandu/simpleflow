import json
import requests


def get(api_endpoint, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token %s' % token
    }

    r = requests.get(api_endpoint, headers=headers)
    return r.json()


def post(api_endpoint, token, data):
    headers = {
        'content-Type': 'application/json',
        'Authorization': 'Token %s' % token
    }
    r = requests.post(api_endpoint, data=json.dumps(data), headers=headers)
    return r.json()


def patch(api_endpoint, token, data):
    headers = {
        'content-Type': 'application/json',
        'Authorization': 'Token %s' % token
    }
    r = requests.patch(api_endpoint, data=json.dumps(data), headers=headers)
    return r.json()