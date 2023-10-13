# simpler_ecom

BY: Håvard Furdal Seim, Erik Martin

Creates a simple e-commerce site where you can buy products. It consists of an python api server with a mongodb database and a javascript/nginx frontend.

## Run

1. Need to specify the `let link=<public-ip>` in `frontend/index.html`.
2. Need to specify the `let port=<port>` in `frontend/index.html`.
3. Need to change the dockerhub username in `scripts/dockerhub_push.sh`
4. Run the following command to install everything and run the app

```bash
cd simpler_ecom && scripts/run.sh
```

## Scripts

Run `scripts/install.sh` which installs and sets up docker and kubectl
Run `scripts/dockerhub_push.sh` to push the generated image to dockerhub
Run `scripts/kubernetes_launch.sh` to apply the service and deployment to the kubernetes cluster

## Kubernetes

`kubernetes/` contains the yaml files for the kubernetes cluster. Each container has its own service and deployment file. The database also has set up local persistant storage configured through the yaml files.

## Frontend

Containes frontend code and Dockerfile.

## Backend

Contains backend code and Dockerfile.
