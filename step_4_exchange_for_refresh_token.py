#! /usr/bin/env python3

import const
from urllib.parse import urlparse, parse_qs
import random
import string
import sys
import requests

callback_url = input("enter callback_url from last step:")

print('Callback URL:', callback_url)
# sometimes I don't get a valid code, not sure why
try:
    parsed_url = urlparse(callback_url)
    query_params = parse_qs(parsed_url.query)
    code = query_params['code'][0]
    print('code:', code)
except KeyError:
    print('Invalid code!')
    sys.exit(1)

# Exchange code for refresh_token
req = requests.post(f"{const.TESLA_AUTH_ENDPOINT}/oauth2/v3/token",
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'},
    data={
        'grant_type': 'authorization_code',
        'client_id': const.CLIENT_ID,
        'client_secret': const.CLIENT_SECRET,
        'code': code,
        'audience': const.AUDIENCE,
        'redirect_uri': f"https://{const.DOMAIN}/callback"
    }
)
if req.status_code >= 400:
    print(f"HTTP {req.status_code}: {req.reason} {req.text}")
    sys.exit(1)

response = req.json()
refresh_token = response['refresh_token']

with open('./data/refresh_token', 'w') as f:
    f.write(response['refresh_token'])
with open('./data/access_token', 'w') as f:
    f.write(response['access_token'])

print("success")
print(f"refresh token: {refresh_token}")
print("stored in ./data")
