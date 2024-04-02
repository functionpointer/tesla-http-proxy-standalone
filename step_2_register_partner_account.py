#! /usr/bin/env python3

import os
import logging
import requests

from const import (
    SCOPES,
    AUDIENCE,
    TESLA_AUTH_ENDPOINT,
    CLIENT_ID,
    CLIENT_SECRET,
    DOMAIN,
    REGION,
)

logging.basicConfig(format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
    level=logging.DEBUG, datefmt='%H:%M:%S')
logger = logging.getLogger('auth')

# generate partner authentication token
logger.info('Generating Partner Authentication Token')

req = requests.post(f"{TESLA_AUTH_ENDPOINT}/oauth2/v3/token",
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'},
    data={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES,
        'audience': AUDIENCE
    }
)
if req.status_code >= 400:
    logger.error("HTTP %s: %s", req.status_code, req.reason)
logger.debug(req.text)
try:
    tesla_api_token = req.json()['access_token']
except KeyError:
    logger.error("Response did not include access token: %s", req.text)
    raise SystemExit(1)

# register Tesla account to enable API access
logger.info('Registering Tesla account...')
req = requests.post(f'{AUDIENCE}/api/1/partner_accounts',
    headers={
        'Authorization': 'Bearer ' + tesla_api_token,
        'Content-Type': 'application/json'
    },
    data='{"domain": "%s"}' % DOMAIN
)
if req.status_code >= 400:
    logger.error("Error %s: %s", req.status_code, req.text)
    raise SystemExit(1)
logger.debug(req.text)
logger.info("Success")
