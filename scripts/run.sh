#!/bin/bash

# Run the application

set -x
sudo ./scripts/install.sh
sudo docker login
sudo ./scripts/dockerhub_push.sh
sudo ./scripts/kubernetes_launch.sh
set +x

echo "Kubernetes cluster launched. Waiting for pods to be ready..."