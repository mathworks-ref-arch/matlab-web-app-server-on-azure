# Health Check tests for MATLAB Web App Server Reference Architecture
# Mathworks 2023-2026

import unittest
import os
import time
import requests
import random
import sys
from datetime import date
import datetime
import testtools.AzureAuthentication as AzureAuth
import testtools.deploy as DeployOp
import testtools.git_utils as git_utils
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import ServiceEndpointPropertiesFormat, Subnet
import traceback
import json


def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, 
         sslCertificate, sslPrivateKey, location_arg, platform_arg, existingVPC, git_token):
    
    # Deploy template
    # Reference architecture in production.
    ref_arch_name = 'matlab-web-app-server-on-azure'
    branch_name = git_utils.get_current_branch()
    
    # Common parameters for template deployment.
    tenant_id = tenant_id_arg
    client_id = client_id_arg
    client_secret = client_secret_arg
    credentials = AzureAuth.authenticate_client_key(tenant_id, client_id, client_secret)
    subscription_id = subscription_id_arg
    location = location_arg
    ipAddress = requests.get("https://api.ipify.org").text + "/32"
    
    vnet_name = None
    resource_name_vnet = None
    
    if existingVPC == 'true':
        # Subnets & virtual network info
        subnets_cidr = ['10.1.0.0/24']
        vnet_cidr = '10.1.0.0/16'
        # Resource group where virtual network is created
        resource_name_vnet = 'vnet_resource_group'
        
        # Deploy a resource group with a virtual network and specified number of subnets
        try:
            print("Creating virtual network...")
            subnet_name_list, vnet_name = DeployOp.create_vnet(
                credentials,
                subscription_id,
                location,
                subnets_cidr,
                resource_name_vnet,
                vnet_cidr
            )
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
            print(f"Error creating virtual network: {e}")
            traceback.print_exc()
            raise e
    
    # Parameters for deployment
    parameters = {
        "IP Addresses Permitted to Remote into Server VM in CIDR Notation": ipAddress,
        "IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation": ipAddress,
        "Base64 Encoded SSL Certificate": sslCertificate,
        "Base64 Encoded SSL Private Key": sslPrivateKey,
        "Username to Remote into Server VM and Network License Manager Web Interface": username,
        "Password to Remote into Server VM and Network License Manager Web Interface": password
    }
    
    if existingVPC == 'true':
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
    else:
        parameters.update({
            "Operating System": platform_arg
        })
    
    # Use GitHub API with authentication
    headers = {
        'Authorization': f'token {git_token}'
    }
    
    # Use GitHub API to get releases
    api_url = f"https://api.github.com/repos/mathworks-ref-arch/{ref_arch_name}/contents/releases?ref={branch_name}"
    res = requests.get(api_url, headers=headers)
    
    if res.status_code != 200:
        print(f"Error fetching releases from GitHub API: {res.status_code}")
        print(f"Response: {res.text}")
        # Clean up VNet if it was created
        if existingVPC == 'true' and resource_name_vnet:
            try:
                DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
                print("Cleaned up virtual network due to API error")
            except:
                pass
        raise Exception(f"Failed to fetch releases from GitHub API")
    
    files = res.json()
    # Extract release names from file names and sort to get latest
    releases = sorted([f['name'] for f in files if f['name'].startswith('R')], reverse=True)
    
    if len(releases) < 2:
        print(f"Warning: Found only {len(releases)} release(s). Expected at least 2.")
    
    # Get the two latest releases
    latest_releases = releases[:2]
    
    for i in range(min(2, len(latest_releases))):
        matlab_release = latest_releases[i]
        print(f"Testing Health Check Release: {matlab_release}\n")
        
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        jsonpath = f"{matlab_release}/templates/mainTemplate.json"
        template_name = f"{github_base_dir}/{ref_arch_name}/{branch_name}/releases/{jsonpath}"
        
        resource_group_name = f"webapp-refarch-health-check-{matlab_release}-{date.today().strftime('%m-%d-%Y')}-{random.randint(1,101)}"
        
        ct = datetime.datetime.now()
        print(f"Date time before deployment of stack: {ct}")
        
        deployment_result = None
        try:
            print(f"Deploying template for {matlab_release}...")
            deployment_result = DeployOp.deploy_webapp_template(
                credentials,
                subscription_id,
                resource_group_name,
                location,
                ref_arch_name,
                template_name,
                parameters
            )
            print(f"Successfully deployed {matlab_release}")
            
        except Exception as e:
            print(f"Error during deployment: {e}")
            traceback.print_exc()
            raise e
            
        finally:
            if deployment_result or resource_group_name:
                try:
                    if existingVPC == 'true':
                        # Delete the deployment which is deployed using existing virtual network
                        print(f"Deleting deployment {resource_group_name}...")
                        deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
                        ct = datetime.datetime.now()
                        print(f"Deleted the deployment which is deployed using existing virtual network: {ct}")
                        # Wait for above deployment deletion
                        print("Waiting 900 seconds for deployment deletion to complete...")
                        time.sleep(900)
                    else:
                        # Delete the deployment
                        print(f"Deleting deployment {resource_group_name}...")
                        deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
                        ct = datetime.datetime.now()
                        print(f"Date time after deployment and deletion of stack: {ct}")
                except Exception as e:
                    print(f"Error during cleanup of deployment: {e}")
                    # Continue with cleanup even if this fails
    
    if existingVPC == 'true' and resource_name_vnet:
        try:
            # Delete deployment with virtual network
            print(f"Deleting virtual network resource group {resource_name_vnet}...")
            DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
            ct = datetime.datetime.now()
            print(f"Deleted the deployment which contains the virtual network: {ct}")
        except Exception as e:
            print(f"Error deleting virtual network: {e}")
            traceback.print_exc()


if __name__ == '__main__':
    if len(sys.argv) < 13:
        print("Error: Missing required arguments")
        print("Usage: python script.py <tenant_id> <client_id> <client_secret> <subscription_id> " +
              "<username> <password> <sslCertificate> <sslPrivateKey> <location> <platform> " +
              "<existingVPC> <git_token>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], 
         sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
