## Release Notes for MATLAB Web App Server on Microsoft Azure

### R2025a
- You can now deploy MATLAB Web App Server R2025a using the Microsoft Azure reference architecture.
- The **Assign Public IP Address to VM Hosting MATLAB Web App Server** entry of the deployment template controls access to the storage account. For details, see the **Assign Public IP Address to VM Hosting MATLAB Web App Server** entry in the [Configure Cloud Resources](/releases/R2025a/README.md#step-2-configure-cloud-resources) step of the deployment process.
    - If you assign a public IP address to the VM hosting MATLAB Web App Server, then public network access to the storage account is enabled only from selected virtual networks and IP addresses. Previously, public network access was enabled from all networks.
    - If you assign a private IP address to the VM hosting MATLAB Web App Server, then public network access to the storage account is disabled. You must use the MATLAB Web App Server VM or a bastion host to connect to the storage account. Previously, public network access was enabled from all networks.
- If you deploy using an existing virtual network and assign a public IP address to the VM hosting MATLAB Web App Server, you must manually add a service endpoint to the virtual network before deploying MATLAB Web App Server in order to create and access the storage account. For details, see [How do I deploy to an existing virtual network?](/README.md#how-do-i-deploy-to-an-existing-virtual-network).

### R2024b
- You can now deploy MATLAB Web App Server R2024b using the Microsoft Azure reference architecture.
- You can assign a private IP address for the Network License Manager VM. Previously, you could only assign the Network License Manager VM a public IP address.
- You can allow a range of IP addresses to access the Network License Manager dashboard.