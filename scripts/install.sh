export DEBIAN_FRONTEND=noninteractive
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://dl.k8s.io/apt/doc/apt-key.gpg 
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list 
sudo apt update -y 
sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh 
sudo sh get-docker.sh 
sudo usermod -aG docker ${USER} 
sudo systemctl enable docker 
sudo systemctl start docker 
sudo apt-get install -y apt-transport-https ca-certificates curl vim git 
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg 
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list 
sudo apt-get update -y
sudo apt-get install -y kubelet kubeadm kubectl 
sudo apt-mark hold kubelet kubeadm kubectl 
sudo swapoff -a 
sudo sed -i.bak -r 's/(.+ swap .+)/#\1/' /etc/fstab 
echo -e "overlay\nbr_netfilter" | sudo tee /etc/modules-load.d/k8s.conf 
sudo modprobe overlay 
sudo modprobe br_netfilter 
echo -e "net.bridge.bridge-nf-call-ip6tables = 1\nnet.bridge.bridge-nf-call-iptables = 1\nnet.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/kubernetes.conf 
sudo sysctl --system 
sudo apt install -y containerd.io 
sudo mkdir -p /etc/containerd 
sudo containerd config default | sudo tee /etc/containerd/config.toml 
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml 
sudo systemctl restart containerd 
sudo systemctl enable containerd 
lsmod | grep br_netfilter 
sudo systemctl enable kubelet 
sudo kubeadm config images pull --cri-socket /run/containerd/containerd.sock 
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --cri-socket /run/containerd/containerd.sock 
mkdir -p $HOME/.kube 
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config 
sudo chown $(id -u):$(id -g) $HOME/.kube/config 
kubectl cluster-info 
wget https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml 
kubectl apply -f kube-flannel.yml 
kubectl get pods -n kube-flannel 
kubectl get nodes -o wide 
kubectl get nodes 
kubectl taint nodes --all node-role.kubernetes.io/control-plane-