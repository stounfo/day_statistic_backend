# day_statistic_backend

## Getting Started

The project uses [poetry](https://python-poetry.org/docs/). Make sure you install it. Also project uses [docker and docker-compose](https://docs.docker.com/engine/install/ubuntu/).

Run the development server:

```bash
make install
make start
```

Deploy project from local. The project uses [ansible](https://docs.ansible.com/ansible/latest/getting_started/index.html) for deploy. Make sure you added authorized_keys on the managed node.

**Attention! This script delete all unused docker data on the managed node.**

```bash
make deploy DEPLOY_HOST=206.188.197.52 DEPLOY_USER=ansible DEPLOY_PROJECT_PATH=/opt/test APP_IMAGE_URL=ghcr.io/stounfo/day_statistic_backend:latest
```
DEPLOY_HOST - host of the Managed node

DEPLOY_PROJECT_PATH - path to directory where project will installed on the Managed node

DEPLOY_USER - username on the Managed node

APP_IMAGE_URL - url with application
