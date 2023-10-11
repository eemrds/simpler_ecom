#!/bin/bash

# Run the application

read -p "Enter IP address: " ip
ip=${ip:-"127.0.0.1"}

set -x
./scripts/install.sh
echo "API_IP=${ip}" > ./frontend/.env
./scripts/dockerhub_push.sh
./scripts/kubernetes_launch.sh
set +x

echo "Kubernetes cluster launched. Waiting for pods to be ready..."
echo "Go to http://$ip:30081."