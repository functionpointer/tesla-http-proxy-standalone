# Start from the official Go image with version 1.20
FROM golang:alpine as builder

WORKDIR /build
ADD https://github.com/teslamotors/vehicle-command/archive/refs/heads/main.zip /build
RUN unzip main.zip
WORKDIR /build/vehicle-command-main

RUN go get ./...
RUN go build ./...
RUN go install ./...
RUN which tesla-http-proxy

FROM golang:alpine

COPY --from=builder /go/bin/tesla-http-proxy /usr/bin
COPY --from=builder /go/bin/tesla-keygen /usr/bin

RUN apk add --no-cache \
  gpg-agent \
  pass

RUN addgroup -g 1000 tesla && adduser -G tesla -u 1000 -h /home/tesla tesla -D
USER tesla

COPY keygen.sh /keygen.sh

# Run the tesla-http-proxy command by default when the container starts.
CMD ["tesla-http-proxy", "-keyring-debug", "-keyring-type", "pass", "-key-name", "myself", "-cert", "/certs/tls-cert.pem", "-tls-key", "/certs/tls-key.pem", "-port", "4448", "-key-file", "/certs/com.tesla.3p.public-key.pem", "-host", "0.0.0.0", "-verbose"]
