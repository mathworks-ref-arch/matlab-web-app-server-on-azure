## Release Notes for MATLAB Web App Server on Microsoft Azure

### R2025a

- If you assign a public IP address to the VM hosting MATLAB Web App Server, then public network access to the storage account is enabled only from selected virtual networks and IP addresses. Previously, public network access was enabled from all networks. For details, see the [Configure Cloud Resources](/releases/R2025a/README.md#step-2-configure-cloud-resources) step of the deployment process.
- If you assign a private IP address to the VM hosting MATLAB Web App Server, you must use a bastion host or jump box VM to connect to the storage account. Previously, storage account access was unrestricted. For details, see [Overview of Azure Bastion host and jumpboxes](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/connect-to-environments-privately).
- If you deploy using an existing virtual network, you must manually add a private or service endpoint to the virtual network in order to access the storage account. For details, see [Create Endpoint in Virtual Network](/releases/R2025a/README.md#create-endpoin-in-virtual-network).

### R2024b
- You can assign a private IP for the Network License Manager VM. Previously, you could only assign the Network License Manager VM a public IP address.
- You can allow a range of IP addresses to access the Network License Manager dashboard.

