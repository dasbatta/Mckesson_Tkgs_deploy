#!/usr/bin/env bash

# Script to prepare the jumpbox with the CLIs (tanzu, kubectl, kapp, ytt, etc.)

echo "==================================== Running apt to get necessary packages..."
sudo apt update
sudo apt install python3-pip -y
sudo apt install git -y
sudo apt install openssh-server -y

echo "Adding python libraries needed for automation..."
pip3 install pyVmomi

echo
echo 'Get the CLI bundles (tanzu, kubectl, velero) from vmware.'
echo See: https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.6/vmware-tanzu-kubernetes-grid-16/GUID-install-cli.html
echo Hit return when done.
read ANS

gunzip Downloads/tanzu*.gz
gunzip Downloads/kubectl*.gz
gunzip Downloads/velero*.gz

echo "==================================== Installing 'tanzu' CLI..."
mkdir Downloads/tanzu
tar xvf Downloads/tanzu*.tar -C Downloads/tanzu
sudo install Downloads/tanzu/cli/core/v0.25.4/tanzu-core-linux_amd64 /usr/local/bin/tanzu

tanzu init
tanzu version
tanzu plugin clean
tanzu plugin sync
tanzu plugin list

echo "==================================== Installing 'kubectl' CLI..."
chmod ugo+x Downloads/kubectl*.1
sudo install Downloads/kubectl*.1 /usr/local/bin/kubectl
kubectl version

echo "==================================== Installing 'ytt' CLI..."
gunzip Downloads/tanzu/cli/ytt*.gz
chmod ugo+x Downloads/tanzu/cli/ytt*.1
sudo install Downloads/tanzu/cli/ytt*.1 /usr/local/bin/ytt
ytt version

echo "==================================== Installing 'kapp' CLI..."
gunzip Downloads/tanzu/cli/kapp*.gz
chmod ugo+x Downloads/tanzu/cli/kapp*.1
sudo install Downloads/tanzu/cli/kapp*.1 /usr/local/bin/kapp
kapp version

echo "==================================== Installing 'kbld' CLI..."
gunzip Downloads/tanzu/cli/kbld*.gz
chmod ugo+x Downloads/tanzu/cli/kbld*.1
sudo install Downloads/tanzu/cli/kbld*.1 /usr/local/bin/kbld
kbld version

echo "==================================== Installing 'imgpkg' CLI..."
gunzip Downloads/tanzu/cli/imgpkg*.gz
chmod ugo+x Downloads/tanzu/cli/imgpkg*.1
sudo install Downloads/tanzu/cli/imgpkg*.1 /usr/local/bin/imgpkg
imgpkg version
