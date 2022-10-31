# day_statistic_backend

## First start

Download the project dependencies:

* [python 3.11](https://www.python.org/downloads/)
* [poetry 1.2.1](https://python-poetry.org/docs/)
* [docker and docker-compose](https://docs.docker.com/engine/install/ubuntu/)


Run the development server:

```bash
make install
make start
```

Show another magic of make.

```bash
make help
```


## Deploy from a local system to a server

Add your public ssh key to the server in ```~/.ssh/authorized_keys```.

Run deploy.

**Attention! The script below deletes all unused docker data on the managed node.**

```bash
make deploy DEPLOY_HOST=206.188.197.52 DEPLOY_USER=ansible DEPLOY_PROJECT_PATH=/opt/test APP_IMAGE_URL=ghcr.io/stounfo/day_statistic_backend:latest
```
DEPLOY_HOST - host of the server

DEPLOY_PROJECT_PATH - path where the project will be installed on the server

DEPLOY_USER - username on the server

APP_IMAGE_URL - URL with a application

## Deploy from a fork cd

Work in progress.

## Contributing

Contributing [cheatsheet](https://gist.github.com/MarcDiethelm/7303312).