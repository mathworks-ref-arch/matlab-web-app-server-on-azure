import urllib.request, json
import azure.functions as func
import uuid

from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.compute import ComputeManagementClient
from azure.common import credentials
from azure.common.credentials import ServicePrincipalCredentials
from msrestazure.azure_active_directory import AADTokenCredentials
from azure.mgmt.resource.resources.models import DeploymentProperties
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.resource.resources.models import TemplateLink
import testtools.getResourceClient as getResourceClient
from azure.mgmt.network import NetworkManagementClient

def deploy_webapp_template(credentials,
    subscription_id,
    resource_group_name,
    location,
    ref_arch_name,
    template_name,
    resource_group_params):

    with urllib.request.urlopen(f'{template_name}') as url:
        template = json.loads(url.read().decode())

    parameters = {k: {'value': v} for k, v in resource_group_params.items()}

    deployment_properties = {
            'mode': DeploymentMode.incremental,
            'template': template,
            'parameters': parameters
    }

    resource_client = getResourceClient.get_resource_client(credentials, subscription_id)

    # Create resource group...
    resource_client.resource_groups.create_or_update(
        resource_group_name,
        {'location': location}
    )
    
    print("Beginning the deployment... \n\n")
    # Deploy template.

    deployment = resource_client.deployments.begin_create_or_update(
        resource_group_name,
        f'{ref_arch_name}-deployment',
        {
            "properties": deployment_properties
        }
    )

    # Block because of VM quotas.
    deployment.wait()
    print(deployment)

    #extract output
    deployment_result = resource_client.deployments.get(resource_group_name, f'{ref_arch_name}-deployment')
    print(deployment_result)
    print("Done with the deployment... \n\n")
    return deployment_result

def create_vnet(credentials,
    subscription_id,
    location,
    subnets_cidr,
    resource_name_vnet,
    vnet_cidr):

    resource_client = getResourceClient.get_resource_client(credentials, subscription_id)
    vnet_name = "my_vnet-" + str(uuid.uuid4())

    # Create resource group
    print("Creating a resource group with a virtual network... \n")
    resource_client.resource_groups.create_or_update(
        resource_name_vnet,
        {'location': location}
    )
    network_client = NetworkManagementClient(credentials, subscription_id)

    print("Resource group created...\n")

    # Create virtual network
    async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
        resource_group_name=resource_name_vnet,
        virtual_network_name=vnet_name,
        parameters={
            'location': location,
            'address_space': {
                'address_prefixes': [vnet_cidr]
            }
        }
    )

    # Wait for the virtual network creation to complete
    async_vnet_creation.result()

    print("Added a virtual network... \n")

    # Array to store the names of the subnets created
    subnet_names = []

    for i in range(1, len(subnets_cidr) + 1):

         # Create Subnet
         subnet_name = "subnet_" + str(i) + "-" + str(uuid.uuid4())
         async_subnet_creation = network_client.subnets.begin_create_or_update(
             resource_group_name=resource_name_vnet,
             virtual_network_name=vnet_name,
             subnet_name=subnet_name,
             subnet_parameters={
                 'address_prefix': subnets_cidr[i - 1]
             }
         )
         subnet_info = async_subnet_creation.result()
         # Add created subnet name to subnet_names array
         subnet_names.append(subnet_info.name)

    print("Added " + str(len(subnets_cidr)) + " subnets")
    # Return the names of subnets created and name of the virtual network
    return subnet_names, vnet_name
    
def delete_resourcegroup(credentials, subscription_id, resource_group_name) :
    resource_client = getResourceClient.get_resource_client(credentials, subscription_id)
    print("Deleting the deployment... \n\n")
    deployment_deletion = resource_client.resource_groups.begin_delete(resource_group_name)
    print(deployment_deletion)
    #return deployment_deletion
