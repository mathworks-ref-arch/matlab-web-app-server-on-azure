## Release Notes for MATLAB Web App Server on Microsoft Azure

### R2025a
- You can assign a public or private IP address to the VM hosting MATLAB Web App Server. Previously, you could only assign a public IP address.
    - If you assign a public IP address to the VM hosting MATLAB Web App Server, then public network access to the storage account is enabled only from selected virtual networks and IP addresses. Previously, public network access was enabled from all networks.
    - If you assign a private IP address to the VM hosting MATLAB Web App Server, you must use a bastion host or jump box VM to connect to the storage account. For details, see [Overview of Azure Bastion host and jumpboxes](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/connect-to-environments-privately).
- If you deploy using an existing virtual network, you must manually add a private or service endpoint to the virtual network in order to access the storage account.

### R2024b
- You can assign a private IP for the Network License Manager VM as well as a range of IP addresses to access the Network License Manager dashboard. 

