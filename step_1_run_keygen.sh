#! /bin/bash

docker build -t tesla build-context
docker run -it --rm --mount type=bind,source="$(pwd)"/certs,target=/certs --mount type=bind,source="$(pwd)"/password-store,target=/home/tesla/.password-store --mount type=bind,source="$(pwd)"/gnupg,target=/home/tesla/.gnupg tesla /keygen.sh
openssl req -x509 -nodes -newkey ec \
      -pkeyopt ec_paramgen_curve:secp521r1 \
      -pkeyopt ec_param_enc:named_curve  \
      -subj "/CN=localhost" \
      -keyout certs/tls-key.pem -out certs/tls-cert.pem -sha256 -days 3650 \
      -addext "extendedKeyUsage = serverAuth" \
      -addext "keyUsage = digitalSignature, keyCertSign, keyAgreement"
