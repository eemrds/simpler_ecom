#!/bin/bash

# Run the application

read -p "Enter IP address: " ip
ip=${ip:-"127.0.0.1"}

set -x
sudo ./scripts/install.sh
echo "API_IP=${ip}" > ./frontend/.env
sudo ./scripts/dockerhub_push.sh
sudo ./scripts/kubernetes_launch.sh
set +x

echo "Kubernetes cluster launched. Waiting for pods to be ready..."
echo "Go to http://$ip:30081."