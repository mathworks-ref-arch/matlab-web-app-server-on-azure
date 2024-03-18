#!/bin/bash -ex
# Copyright the MathWorks Inc 2020
# This script
# 1. include storage account information to dynamicOption
# 2. start controller
while getopts "n:f:k:s:c:p:d:" opt; do
    case ${opt} in
    n)  storageAccountName="$OPTARG";;
    f)  resourceGroup="$OPTARG";;
    k)  subscriptionID="$OPTARG";;
    s)  enableSSL="$OPTARG";;
    c)  certFile="$OPTARG";;
    p)  privateKeyFile="$OPTARG";;
    d)  fqdn="$OPTARG";;
    esac
done

JSONCMD='
{
	"storageAccountName": "'"$storageAccountName"'",
	"resourceGroup": "'"$resourceGroup"'",
    "subscriptionID": "'"$subscriptionID"'",
	"enableSSL": "'"$enableSSL"'",
	"certFile": "'"$certFile"'",
    "privateKeyFile": "'"$privateKeyFile"'",
    "fqdn": "'"$fqdn"'"
}
'

myPath=/MathWorks/controller/config/dynamicOptions.json
rm $myPath

#load json string into dynamic option file
echo $JSONCMD >> $myPath


#to allow web app server to listen on port 443
sudo sysctl net.ipv4.ip_unprivileged_port_start=0

#start controller
node /MathWorks/controller/index.js &