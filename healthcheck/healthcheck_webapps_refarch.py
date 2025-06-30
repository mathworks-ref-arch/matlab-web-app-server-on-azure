import unittest
import os
import time
import re
import requests
import random
import sys
from datetime import date
import datetime

import testtools.AzureAuthentication as AzureAuth
import testtools.deploy as DeployOp
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import ServiceEndpointPropertiesFormat, Subnet

def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, ipAddress, sslCertificate, sslPrivateKey, location_arg, platform_arg, existingVPC):

    # Deploy template
    # Reference architecture in production.
    ref_arch_name = 'matlab-web-app-server-on-azure'

    # Common parameters for template deployment.
    tenant_id = tenant_id_arg
    client_id = client_id_arg
    client_secret = client_secret_arg
    credentials = AzureAuth.authenticate_client_key(tenant_id, client_id, client_secret)
    subscription_id = subscription_id_arg
    location = location_arg

    if existingVPC=='true':
        # Subnets & virtual network info
        subnets_cidr = ['10.1.0.0/24']
        vnet_cidr = '10.1.0.0/16'
        # Resource group where virtual network is created
        resource_name_vnet = 'vnet_resource_group'
        # Deploy a resource group with a virtual network and specified number of subnets
        try:
            subnet_name_list, vnet_name = DeployOp.create_vnet(credentials,
                                                            subscription_id,
                                                            location,
                                                            subnets_cidr,
                                                            resource_name_vnet,
                                                            vnet_cidr)
            subnet_name = subnet_name_list[0]
            network_client = NetworkManagementClient(credentials, subscription_id)
            # Add service endpoint to subnets
            subnet = network_client.subnets.get(resource_name_vnet, vnet_name, subnet_name)
            if not subnet.service_endpoints:
                subnet.service_endpoints = []
            subnet.service_endpoints.append(
                ServiceEndpointPropertiesFormat(service='Microsoft.Storage')
            )
            updated_subnet = network_client.subnets.begin_create_or_update(
                resource_name_vnet,
                vnet_name,
                subnet_name,
                subnet
            ).result()
            print(f"Enabled Microsoft.Storage service endpoint for subnet: {subnet_name}")
        except Exception as e:
            raise(e)
    # Parameters for deployment
    parameters = {
        "IP Addresses Permitted to Remote into Server VM in CIDR Notation": ipAddress,
        "IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation": ipAddress,
        "Base64 Encoded SSL Certificate": sslCertificate,
        "Base64 Encoded SSL Private Key": sslPrivateKey,
        "Username to Remote into Server VM and Network License Manager Web Interface": username,
        "Password to Remote into Server VM and Network License Manager Web Interface": password
    }

    if existingVPC=='true':
        parameters.update({
            "Deploy to New or Existing Virtual Network": "existing",
            "Name of Virtual Network Where MATLAB Web App Server Will Be Deployed": vnet_name,
            "Virtual Network CIDR Range": vnet_cidr,
            "Name of Subnet for MATLAB Web App Server": subnet_name,
            "Server Subnet CIDR Range": subnets_cidr[0],
            "Specify Private IP Address to VM Hosting MATLAB Web App Server": '10.1.0.4',
            "Resource Group Name Of Virtual Network": resource_name_vnet,
            "Operating System": platform_arg
        })

    # Find latest MATLAB release from Github page and get template json path.
    res = requests.get(
        f"https://github.com/mathworks-ref-arch/{ref_arch_name}/tree/main/releases/"
    )
    latest_releases = [
        re.findall(r"releases/(R\d{4}[ab]\b)", res.text)[-1],
        re.findall(r"releases/(R\d{4}[ab]\b)", res.text)[-2]
    ]
    for i in range(2):
        matlab_release = latest_releases[i]
        print("Testing Health Check Release: " + matlab_release + "\n")
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        jsonpath = f"{matlab_release}/templates/mainTemplate.json"
        template_name = f"{github_base_dir}/{ref_arch_name}/main/releases/{jsonpath}"
        resource_group_name = "webapp-refarch-health-check-" + matlab_release + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))
        ct = datetime.datetime.now()
        print("Date time before deployment of stack:-", ct)

        try:
            deployment_result = DeployOp.deploy_webapp_template(credentials,
                                                       subscription_id,
                                                       resource_group_name,
                                                       location,
                                                       ref_arch_name,
                                                       template_name,
                                                       parameters
                                                       )
        except Exception as e:
            raise(e)
        finally:
             if existingVPC=='true':
                # Delete the deployment which is deployed using existing virtual network
                deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
                ct = datetime.datetime.now()
                print("Deleted the deployment which is deployed using existing virtual network:-",ct)
                # Wait for above deployment deletion
                time.sleep(900)
             else:
                # Delete the deployment
                deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
                ct = datetime.datetime.now()
                print("Date time after deployment and deletion of stack:-", ct)

    if existingVPC=='true':
        # Delete deployment with virtual network
        DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
        ct = datetime.datetime.now()
        print("Deleted the deployment which contains the virtual network:-", ct)

    if existingVPC=='true':
        # Delete deployment with virtual network
        DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
        ct = datetime.datetime.now()
        print("Deleted the deployment which contains the virtual network:-", ct)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
