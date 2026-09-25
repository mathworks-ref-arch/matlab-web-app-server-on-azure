#!/bin/bash -ex
# Copyright the MathWorks Inc 2020
# This script
# 1. include storage account information to dynamicOption
# 2. start controller
while getopts "n:f:k:s:c:p:d:a:u:b:" opt; do
    case ${opt} in
    n)  storageAccountName="$OPTARG";;
    f)  resourceGroup="$OPTARG";;
    k)  subscriptionID="$OPTARG";;
    s)  enableSSL="$OPTARG";;
    c)  certFile="$OPTARG";;
    p)  privateKeyFile="$OPTARG";;
    d)  fqdn="$OPTARG";;
    a)  allowPublicIP="$OPTARG";;
    u)  useDefaultKeycloak="$OPTARG";;
	b)  backchannelFqdn="$OPTARG";;
    esac
done


# Resolve full internal FQDN assigned by Azure
internalFqdn="$(hostname -f)"

echo "Detected internal FQDN: ${internalFqdn}"
echo "Using backchannel FQDN: ${backchannelFqdn}"

# Port configuration for Keycloak (auth), Admin Portal (management UI), and Web App Server (apps).
# Public ports are exposed to clients via the network; internal ports are for intra-VM communication.
# PRE-DEPLOYMENT:  Edit the values below before running the ARM template.
# POST-DEPLOYMENT: Edit /MathWorks/controller/config/dynamicOptions.json on the VM,
#   then restart affected services (or reboot the VM).
#   Also update the Azure Network Security Group rules to allow traffic on the new ports.
public_kc_port=8443
public_ap_port=8080
public_was_port=9988
internal_kc_port=8443
internal_ap_port=8080
internal_was_port=9988

echo "Service ports — Keycloak: ${public_kc_port}/${internal_kc_port}, Admin Portal: ${public_ap_port}/${internal_ap_port}, Web App Server: ${public_was_port}/${internal_was_port} (public/internal)"

JSONCMD='
{
	"storageAccountName": "'"$storageAccountName"'",
	"resourceGroup": "'"$resourceGroup"'",
    "subscriptionID": "'"$subscriptionID"'",
	"enableSSL": "'"$enableSSL"'",
	"certFile": "'"$certFile"'",
    "privateKeyFile": "'"$privateKeyFile"'",
    "internal_fqdn": "'"$internalFqdn"'",
    "fqdn": "'"$fqdn"'",
	"backchannelFqdn": "'"$backchannelFqdn"'",
    "allowPublicIP": "'"$allowPublicIP"'",
    "useDefaultKeycloak": "'"$useDefaultKeycloak"'",
    "public_kc_port": '"$public_kc_port"',
    "public_ap_port": '"$public_ap_port"',
    "public_was_port": '"$public_was_port"',
    "internal_kc_port": '"$internal_kc_port"',
    "internal_ap_port": '"$internal_ap_port"',
    "internal_was_port": '"$internal_was_port"'
}
'

myPath=/MathWorks/controller/config/dynamicOptions.json
rm $myPath

#load json string into dynamic option file
echo $JSONCMD >> $myPath

# Persist sysctl setting to allow non-root processes to bind to privileged ports like 443
echo "net.ipv4.ip_unprivileged_port_start=0" | sudo tee /etc/sysctl.d/99-unprivileged-ports.conf

# Apply sysctl settings immediately
sudo sysctl --system

#start controller
node /MathWorks/controller/index.js &
systemctl start mw-adminportal
