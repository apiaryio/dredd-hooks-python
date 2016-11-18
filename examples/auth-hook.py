# Example how to roll your own Authorization in the dredd hooks.
# It uses a non-standard requests package (http://python-requests.org/)

import json
import dredd_hooks as hooks
import requests

stash = {}
api_username = "XXX"
api_password = "XXX"
api_uri = "XXX"


@hooks.before_each
def add_token(transaction):
    if 'token' in stash:
        print('adding a token')
    else:
        stash['token'] = obtain_token()

    transaction['request']['headers']['Authorization'] = "Bearer " + stash['token']


def obtain_token():
    data = {
               "api_login_form": {
                   "username": api_username,
                   "password": api_password
               }
           }
    url = api_uri
    response = requests.post(url, json=data)
    response.raise_for_status()
    parsed_body = response.json()
    token = parsed_body["token"]
    return token
