#!/bin/bash -ex
# Copyright the MathWorks Inc 2020
# This script
# 1. include storage account information to dynamicOption
# 2. start controller
while getopts "n:f:k:s:c:p:" opt; do
    case ${opt} in
    n)  storageAccountName="$OPTARG";;
    f)  resourceGroup="$OPTARG";;
    k)  subscriptionID="$OPTARG";;
    s)  enableSSL="$OPTARG";;
    c)  certFile="$OPTARG";;
    p)  privateKeyFile="$OPTARG";;
    esac
done

JSONCMD='
{
	"storageAccountName": "'"$storageAccountName"'",
	"resourceGroup": "'"$resourceGroup"'",
    "subscriptionID": "'"$subscriptionID"'",
	"enableSSL": "'"$enableSSL"'",
	"certFile": "'"$certFile"'",
    "privateKeyFile": "'"$privateKeyFile"'"
}
'

myPath=/MathWorks/controller/config/dynamicOptions.json
rm $myPath

#load json string into dynamic option file
echo $JSONCMD >> $myPath

#to allow web app server to listen on port 443
sudo sysctl net.ipv4.ip_unprivileged_port_start=0

sudo apt -y install xorg openbox xterm
sudo sed -i 's/allowed_users=console/allowed_users=anybody/' /etc/X11/Xwrapper.config
sudo sed -i 's/Environment=/Environment="DISPLAY=:0"/' /etc/systemd/system/mw-webapps-launcher-R2022a.service
echo 'sleep infinity' >> ~/.xinitrc
xinit xterm &
export DISPLAY=:0
sudo xhost +SI:localuser:MwWebAppsWorkerR2022a

#start controller
node /MathWorks/controller/index.js &