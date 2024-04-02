#! /usr/bin/env python3
import const
from pathlib import Path

tls_cert_path = Path("./certs/tls-cert.pem")
with Path("./data/refresh_token").open() as f:
  refresh_token = f.read()

print("start the docker container: docker compose up -d")
print("configure hass integration with following details")
print(f"refresh token: {refresh_token}")
print(f"proxy url: https://localhost:4448")
print(f"proxy ssl cert: {tls_cert_path.absolute()}")
print(f"client id: {const.CLIENT_ID}")
