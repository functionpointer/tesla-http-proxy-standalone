#! /usr/bin/env python3

import random
import const
import string
import urllib.parse

scopes_encoded = urllib.parse.quote_plus(const.SCOPES)

randomstate = ''.join(random.choices(string.hexdigits.lower(), k=10))
randomnonce = ''.join(random.choices(string.hexdigits.lower(), k=10))
url = f"{const.TESLA_AUTH_ENDPOINT}/oauth2/v3/authorize?&client_id={const.CLIENT_ID}&prompt=login&redirect_uri=https://{const.DOMAIN}/callback&response_type=code&scope={scopes_encoded}&state={randomstate}&nonce={randomnonce}"

print("open this in webbrowser:")
print(url)

print("copy the url of the 404 afterwards")
