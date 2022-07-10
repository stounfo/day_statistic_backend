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
make deploy PROJECT_PATH=/opt/test/ DEPLOY_USER=ansible APP_IMAGE_URL=ghcr.io/stounfo/day_statistic_backend:master
```
PROJECT_PATH - path to directory where project will installed on the Managed node

DEPLOY_USER - username on the Managed node

APP_IMAGE_URL - url with application
