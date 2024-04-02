#! /bin/bash

# prepare password-store
gpg --batch --passphrase '' --quick-gen-key myself default default
gpg --list-keys
pass init myself

tesla-keygen -f -keyring-type pass -key-name myself create > /certs/com.tesla.3p.public-key.pem
