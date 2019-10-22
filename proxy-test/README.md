# Proxy Test

A simple demonstration of an Apache proxy with basic auth with the Apache 2.4 Alpine image.

The file `proxy/container_files/conf/extra/passwords` describes a single username/pass, both being `usertest`.

## Run the Test

* `docker-compose up --build -d`
* The local `proxy` and `secret` images will build and start
* `http://localhost` will show `Access Denied` served from the proxy
* `http://localhost/secret` will require basic auth to proceed, and then serve the secret image's webroot
* `http://localhost:81` to bypass the basic auth and see the secret image's webroot (here for demon purposes only!)

