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

def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, ipAddress, sslCertificate, sslPrivateKey, location_arg, platform_arg):

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

    # Subnets & virtual network info
    subnets_cidr = ['10.0.0.0/24']
    vnet_cidr = '10.0.0.0/16'

    # Resource group where virtual network is created
    resource_name_vnet = 'vnet_resource_group'

    # Deploy a resource group with a virtual network and specified number of subnets
    try:
          subnet_name, vnet_name = DeployOp.create_vnet(credentials,
                                                        subscription_id,
                                                        location,
                                                        subnets_cidr,
                                                        resource_name_vnet,
                                                        vnet_cidr)

    except Exception as e:
        raise(e)
    print(subnet_name[0])
    # Parameters for deployment
    parameters = {
        "IP Addresses Permitted to Remote into Server VM in CIDR Notation": "0.0.0.0/0",
        "IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation": ipAddress,
        "Base64 Encoded SSL Certificate": sslCertificate,
        "Base64 Encoded SSL Private Key": sslPrivateKey,
        "Username to Remote into Server VM and Network License Manager Web Interface": username,
        "Password to Remote into Server VM and Network License Manager Web Interface": password,
        "Deploy to New or Existing Virtual Network": "existing",
        "Name of Virtual Network Where MATLAB Web App Server Will Be Deployed": vnet_name,
        "Virtual Network CIDR Range": vnet_cidr,
        "Name of Subnet for MATLAB Web App Server": subnet_name[0],
        "Server Subnet CIDR Range": subnets_cidr[0],
        "Resource Group Name Of Virtual Network": resource_name_vnet,
        "Operating System": platform_arg
    }

    print(parameters)

    # Find latest MATLAB release from Github page and get template json path.
    res = requests.get(
        f"https://github.com/mathworks-ref-arch/{ref_arch_name}/tree/main/releases/"
    )
    latest_releases = [re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-1], re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-2]]
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

    # Delete the deployment which is deployed using existing virtual network
    deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
    print("Deleted the deployment which is deployed using existing virtual network")
    # Wait for above deployment deletion
    time.sleep(900)
    # Delete deployment with virtual network
    DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
    print("Deleted the deployment which contains the virtual network")

if __name__ == '__main__':
    main("99dd3a11-4348-4468-9bdd-e5072b1dc1e6","f0d681d1-15e6-40e6-a8a7-d82f686578a8","6IP70T.0y5~_ldiG.8aNKSK6oKaPOcl5qp","2fe59ed0-c022-4411-b2c3-4a2021c1df9c", "azureadmin", "Password123", "144.212.3.4", "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlEYlRDQ0FsV2dBd0lCQWdJVUYxQW52S3czTXdvei9hUW0vSlJRNnlpTzR2WXdEUVlKS29aSWh2Y05BUUVMDQpCUUF3UlRFTE1Ba0dBMVVFQmhNQ1ZWTXhFekFSQmdOVkJBZ01DbE52YldVdFUzUmhkR1V4SVRBZkJnTlZCQW9NDQpHRWx1ZEdWeWJtVjBJRmRwWkdkcGRITWdVSFI1SUV4MFpEQWdGdzB5TXpBME1EY3hOVEEyTlRoYUdBOHlNVEl6DQpNRE14TkRFMU1EWTFPRm93UlRFTE1Ba0dBMVVFQmhNQ1ZWTXhFekFSQmdOVkJBZ01DbE52YldVdFUzUmhkR1V4DQpJVEFmQmdOVkJBb01HRWx1ZEdWeWJtVjBJRmRwWkdkcGRITWdVSFI1SUV4MFpEQ0NBU0l3RFFZSktvWklodmNODQpBUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTkJwYzF1TVBzVDZONDdRWlVTYjR1a1RYV2swVWcxVDVhYVhzdmZ1DQpZSlVFd2F1TUxiWEk5aEMrdExLcW44UHh5ZE1nTWtLeU9oVWlIRDFKdDNzLzBMRUg5NGg2VGlPa2VsMnNNOTlaDQpQc25ncHhYa0M1ZFhvQ0VkNkUwaGtNUlhpK21aQzM3OXp0dUhkNmlJNU51LzZLdnNsdkJkODJkbmtubm80OS9VDQplcUpKYTdqc0hmSXNLc3ZlZm96YmR4M0ZmS29ZK3hjb2FrMnpKTkZ1eERjTmFabmhYdkJpNDI4UjZ3L3hldjdBDQp1aUV2ekN6alB1bHJ2bTdJVmZ6OUd1dk9xNXJkU3FJVk5MNFFJc1JSNDMyY1V6ejFXREhMMjFsNmwxZmZhSnRKDQppZTV3dzM3UXBhMjE5dFBZY1JXRVVqeDlweUhyOHk1ZGZhNlRYWlVVZjRpNnNCRUNBd0VBQWFOVE1GRXdIUVlEDQpWUjBPQkJZRUZOT0t2SEdOa0xQQXlCWmhwMDdQRk5vZkRXc0ZNQjhHQTFVZEl3UVlNQmFBRk5PS3ZIR05rTFBBDQp5QlpocDA3UEZOb2ZEV3NGTUE4R0ExVWRFd0VCL3dRRk1BTUJBZjh3RFFZSktvWklodmNOQVFFTEJRQURnZ0VCDQpBTGRGVGdNdGVJRFVWdm9hcVlPTUh1U3h5MGI4N296Rkp5dzJvS1lMbUZBS3QxOUJxQ2YzZHdkclViRGRGR1gzDQp2TjFlekhvUmFjOUNXbWJGRUZ6MHViUWY5YVRscDU2aGNpWUk4cnB6NU5UNVJ0SmxhY2JQTWZLOXNkZU8zQ09RDQpkenlISUo4U0IybVZ2WFZWR01hOFozZHFadCsveVcrMEljS3YzY2lFNmFENThtTUw3Q25CRzlkanRQWEJnSWYxDQpZTHE5eldhMlplaDlhLy9pUVJLWHRpZnM5anNoTm1wYmtEYmxkdmxXdGJXeTBTU21QTXVuTUsxOCs0RHRKODB5DQptVDFjREVwb0t4WWZPU0ZGUTRHdExXWEsyQ1Jnc3I1MXJYZHNLVE9zK3VObzJONjk2NFRzdnNWRTRDd2t2UmE1DQpCTDFhSjVWZEY3bGNSSmdBM0FnMTZ5VT0NCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0NCg==", "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tDQpNSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUURRYVhOYmpEN0UramVPDQowR1ZFbStMcEUxMXBORklOVStXbWw3TDM3bUNWQk1HcmpDMjF5UFlRdnJTeXFwL0Q4Y25USURKQ3Nqb1ZJaHc5DQpTYmQ3UDlDeEIvZUllazRqcEhwZHJEUGZXVDdKNEtjVjVBdVhWNkFoSGVoTklaREVWNHZwbVF0Ky9jN2JoM2VvDQppT1RiditpcjdKYndYZk5uWjVKNTZPUGYxSHFpU1d1NDdCM3lMQ3JMM242TTIzY2R4WHlxR1BzWEtHcE5zeVRSDQpic1EzRFdtWjRWN3dZdU52RWVzUDhYcit3TG9oTDh3czR6N3BhNzV1eUZYOC9ScnJ6cXVhM1VxaUZUUytFQ0xFDQpVZU45bkZNODlWZ3h5OXRaZXBkWDMyaWJTWW51Y01OKzBLV3R0ZmJUMkhFVmhGSThmYWNoNi9NdVhYMnVrMTJWDQpGSCtJdXJBUkFnTUJBQUVDZ2dFQWFxcHQxaDhUU1RGZkdnTGlzWml2SytjeldkTGpZOXJhb01iblhDbHUyUllVDQpJVDZmYm5pcUo2dlRROVk3NnNkbktsMUNIQXluMllVWnV1eHRzZkRaV0tIaE9NS1FGNEhvOXVSWnNDZzNFSStnDQpOSDRBeUxhYVNCak1laDJCd0Z1bVNpcUFUY0NOREtKcXhhRTZzSldwK2NRZkJHcXhWdTBWZEx1VFZVMmtia1lFDQpRRDVrY0Jod2RDbHdhYUNLS1lhSWVSalFncmROR0U2SWoyREpsNG1IVzQzcmZscWtHb3JRMDJLOE9xOEdXdmJyDQpRNTdKMithN1B3R05naG9BK3U4UDJGSmVXREpCSzlJTnp3ajZhRXJCbWZxZlVib25UOGErdHQ4STkyL1dQdnNFDQo5VmxpSXlDWFFla0hTOHJ3dzk0allvNEFUQmpQT3ErcWRJSFpDWEhQb1FLQmdRRDd5ekhWUHphd2hGSlJuTUk5DQpZNE1nSHdrZU9UMEpMK3FOT1lkc1prVUUxNGk3cThYWXJ0RDBkbnd5UGtQWHd5WFJvNmdSVEU4bUZoVkdISm5xDQp2Y2xHVzFXOTQzRWp1ZGsvTllDaGxNTVAzeG1VQjRMbnJtUVcwRGJUME1EYWN0U2FFZHU2TmlWYmpaekF4ZndsDQpENndDUU1uck9PaVBxa2hCN0FuNG9tTXNiUUtCZ1FEVDVMdGtvUmZCNVVxSXR3Q1ROUTV1anQ1RmhnTlF3WDlnDQpsTHZSRXVaWjBsR0FVMXVkZHJ1eHVZZzNETEdSdGNqWDhWV1RDbXAzTGNqMmF3WGFadFhEdFpGY0Y3UlFDdk95DQptTFBvZnZzYThOYU5Hb2s4M0tMSFVHYzBjRGtzNTVEV0NIdkkreFBvaWdVM1NiTDVSUkUxL2tNZUx0K0d5WVM0DQovVmdtYnhNRHRRS0JnRlFEWVhaQXFGUFBZdFFlVk9VOHplU3ExbFVDVGk1QmthWmJlcWNkbkl2WUNxUnIxUkRPDQppNlAxNE15MjM5WWZKQUJGOWU4SG9pVVlHek1RbWY2c0ludGFRRXFpbC82T3BVRWs3ZTE4QUhYTVAvR1hiQU0zDQp1ZWV1dzR4N1M4M1hvTDVqbFFnVnh2TThWZ0F3VDBoaWFVYzdMT1JTVWE2VjU1UXZXTWhnRG0wbEFvR0FOb0wxDQpvcUcrMXVjQ0VjSGlwL3hTUmljREQ2ZTJXcVFzL00vR3NiYkhBL3lUY3d2KzJiZWQrYzdkT0N4UDBraU43dC9yDQpQL1RDQnY4RVlFQ1FOT3VYdXMyUEk3NEZhVUlvQjU0NVNtckFkdUhXa0Y1dlIvVUsrM08zMlVtMXE5TzI4eGtqDQpuMFRZams1VG9UR1lsWUFyT1ZTOE41dWZiYkdTTDNVZHBHV1c0ckVDZ1lFQTlPRXB1UUN2N2pweG5RRUNIMTJ4DQp1QlR3S1dYTGE1aEJtbEtsODd5T05lOFp1NzA0RXQyVDRpQ3h6TXRTb3JJNTRPZU5EV1RKMzZjTGR6UHJSYVZ3DQpHcEkzcGxrRG1DRm5FTmV2RzhneG4ybDNJV1pDSnNQSi94d3BSd0FTOWJwZmlvSGpBWTNadjRXaDBzenBRN0JFDQp2TURzaXA1VCtQdzRnQWpDN0ZGcmprND0NCi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0NCg==", "eastus", "Windows")
    #main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])