# simpler_ecom

BY: Håvard Furdal Seim, Erik Martin

Creates a simple e-commerce site where you can buy products. It consists of an python api server with a mongodb database and a javascript frontend.

## Single command install

```bash
cd simpler_ecom && scripts/run.sh
```

## Installation

Run `scripts/install.sh` which installs and sets up docker and kubectl
Run `scripts/dockerhub_push.sh` to push the generated image to dockerhub
Run `scripts/kubernetes_launch.sh` to apply the service and deployment to the kubernetes cluster
