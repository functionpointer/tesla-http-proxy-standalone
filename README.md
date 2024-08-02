Tesla HTTP Proxy Standalone
===========================

Using [HomeAssistant Tesla Custom integraton](https://github.com/alandtse/tesla) now requires Tesla's Fleet Api Proxy.
Setting it up is some work. There is a ready-made [HomeAssistant Add-On](https://github.com/llamafilm/tesla-http-proxy-addon).
That's great, but doesn't work for [Home Assistant Core](https://www.home-assistant.io/installation/#advanced-installation-methods).

This repo is the solution. A simple docker container with the proxy, and some set-up scripts for the required certificates.
The code is mostly taken from the Add-On.

What you will need
==================

- Docker
- NGINX
- Your own domain


Installation
============

1. Choose a subdomain. I will use `tesla.<your domain>.com` in this documentation
2. clone this repo
3. copy `client_secrets.py.template` to `client_secrets.py`
4. in `client_secrets.py`, edit `REGION` to reflect your region, edit `DOMAIN` to reflect your domain
5. run `step_1_run_keygen.py`
6. Request application at `developer.tesla.com`. See [here](https://github.com/llamafilm/tesla-http-proxy-addon/blob/main/tesla_http_proxy/DOCS.md#how-to-use) for more info.
   Do not choose the Open Source plan, as you will need the client secret.
   Choose `https://tesla.<your domain>.com` as allowed origin, and `https://tesla.<your domain>.com/callback` as redirect URI.
   Choose all scopes.
7. You will get a Client ID and Client Secret. Copy them into `client_secrets.py`.
8. add this to your nginx:
```
server {
  listen [::]:443 ssl;
  listen 443 ssl;
  http2 on;

  server_name tesla.<your domain>.com;
  proxy_buffering off;

  location / {
    return 404;
  }

  location /.well-known/appspecific/com.tesla.3p.public-key.pem {
    root <path to this repo>/certs;
    try_files /com.tesla.3p.public-key.pem =404;
  }

  location = /favicon.ico {
    log_not_found off;
  }

  location = /robots.txt {
    log_not_found off;
  }

}
```
9. run the other `step_*_.py` scripts in order. follow the instructions.
10. Eventually you will need to start the container: `docker compose up -d`
11. Finally, set up the [HomeAssistant Tesla Custom integraton](https://github.com/alandtse/tesla). If you already have it configured, you will have to delete the integration and set it up again. Don't worry, HA doesn't delete your history.

What it does
============

Tesla's Proxy needs two sets of certificates:
1. The 3p certificate, used to communicate with Tesla's Servers
2. The snakeoil certificate, used to communicate with clients of the proxy (i.e. between HA and the proxy)

`step_1_run_keygen.py` generates both certs. The 3p one needs to be publically available, so nginx is configured to serve it pubically.
The snakeoil certificate is not published.
Certificates are stored in the `certs/` folder.
The 3p key unfortunately can't be, as Tesla's code _needs_ to have it in a keyring.
We use the `passkey` keyring to store it, and so the key ends up in the `password-store/` and `gnupg/` folders.

The following steps mostly interact with Tesla.
First, a partner account is created. That one represents our "third-party company".
Then, your personal Tesla account grants that partner account access using OAuth. This creates an `access_token` and `refresh_token`, both stored under `data/`.
These are used for your actual application, i.e. the HA integration.

Updating
========

Run `tesla-update.sh`

