# MATLAB Web App Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Web App Server™ license. To configure a license for use on the cloud, you must obtain the MAC address of the network license manager after deployment to the cloud. For details, see [Configure MATLAB Web App Server Licensing on the Cloud](https://www.mathworks.com/help/webappserver/ug/configure-server-license-on-cloud.html).
-   A Microsoft Azure™ account.

# Costs
You are responsible for the cost of the Azure services used when you create cloud resources using this guide. Resource settings, such as instance type, affect
the cost of deployment. For cost estimates, see the pricing pages for each Azure
service you are using. Prices are subject to change.


# Introduction 

Use this guide to automate the process of running MATLAB Web App Server on Azure using your Azure account. The automation is accomplished using an Azure Resource Manager (ARM) template. The template is a JSON file that defines the resources needed to deploy and manage MATLAB Web App Server on Azure. For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources).

Deploying MATLAB Web App Server on Azure automatically deploys a network license manager. However, you can also use an existing network license manager with MATLAB Web App Server on Azure by selecting `existing` from the deployment template.

# Deploy Reference Architecture for Your Release
To deploy the reference architecture, select your MATLAB Web App Server release from the table and follow the instructions to deploy the server using the provided template. 
| Release | Supported MATLAB Runtime Versions | Status |
| ------- | --------------------------------- | ------ |
| [R2025a](releases/R2025a/README.md) | R2025a, R2024b, R2024a, R2023b, R2023a*, R2022b* | ✅ Template available. |
| [R2024b](releases/R2024b/README.md) | R2024b, R2024a, R2023b, R2023a*, R2022b*, R2022a* | ✅ Template available. |
| [R2024a](releases/R2024a/README.md) | R2024a, R2023b, R2023a, R2022b, R2022a, R2021b | ✅ Template available. |
| [R2023b](releases/R2023b/README.md) | R2023b, R2023a, R2022b, R2022a, R2021b | ⚠️ Template will be removed in March 2026. |
| [R2023a](releases/R2023a/README.md) | R2023a, R2022b, R2022a, R2021b, R2021a, R2020b | ⚠️ Template will be removed in September 2025. |

> [!WARNING]
> \*When the server is configured to use MATLAB Runtime versions prior to R2023b, the `unsafe-inline` attribute is set in the `script-src` directive of the server's Content Security Policy on the server and cannot be removed. The attribute allows inline JavaScript execution and event handlers contained within a web app to execute on the server. These runtimes are disabled by default starting in R2024b. You can enable them using the [webapps-runtime](https://www.mathworks.com/help/webappserver/ref/webappsruntime.html) command.

MathWorks provides templates for only the five most recent releases of MATLAB Web App Server. Earlier templates are removed and are no longer supported.

# Architecture and Resources
Deploying this reference architecture creates several resources in your
resource group.

![Cluster Architecture](/images/mwas-ref-arch-azure-architecture-diagram.png?raw=true)

*Architecture on Azure*

### Resources
| Resource Name  | Type | Description                                                                                                                                                                                                                                                                                                                        |
|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `webapp-public-ip` | Public IP address | Public IP address to connect to MATLAB Web App Server. |
| `webapp-refarch-vnet`   | Virtual network | Enable resources to communicate with each other via network. |
|  `webapp-nsg` | Network security group | Filter network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
|  `webapp-nic` | Network interface | Provide network interface for MATLAB Web App Server. |
| `appstorage<uniqueID>`   | Storage account | Storage account where web app archives (.ctf files) and logs are stored. |
| `webapp-vm`           | Virtual machine | Virtual machine to host MATLAB Web App Server.|
|  `webappVM_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting MATLAB Web App Server. |

If you are deploying a new network license manager, the following resources will also be created in your resource group.

| Resource Name  | Type | Description                                                                                                                                                                                                                                                                                                                        |
|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `netlm-nsg` | Network security group | Filter network traffic to and from network license manager resources in an Azure virtual network. |
| `netlm-server`        | Virtual machine  | Virtual machine to host network license manager. |
|  `netlm-server-ip` | Public IP address | Provide public IP address to network license manager. |
|  `netlm-server-nic` | Network interface | Provide network interface for network license manager. |
|  `netlm-server_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting network license manager. |


# FAQ
## How do I deploy to an existing virtual network?
>**Note:** Your existing virtual network must have at least two available subnets for deployment. 

### Ports to Open in Existing Virtual Network
If you are deploying MATLAB Web App Server to an existing virtual network, you must open the following ports in your virtual network:
| Port | Description |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `443` | HTTPS - the port Web App Server will service if SSL is enabled |
| `22` | SSH - used for remoting into Linux machines |
| `3389` | RDP - used for remoting into Windows machines |
| `27000` | Required for communication between network license manager and Web App Server |

### Create Service Endpoint in Virtual Network (Since R2025a)
Starting in R2025a, if you are using an existing virtual network and assign a public IP address to the VM hosting MATLAB Web App Server, then you must manually add a service endpoint to the virtual network *before* deploying MATLAB Web App Server in order to create and access the storage account. For more details, see [Grant access from a virtual network](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security?tabs=azure-portal#grant-access-from-a-virtual-network) in the Microsoft Azure documentation.

You can check if such an endpoint already exists by navigating to the Azure Portal, selecting your virtual network, and clicking **Service endpoints**. If no such endpoint is present, follow these steps:
1. In the Azure Portal, click **Resource groups** and select the virtual network for this deployment.
1. In the left navigation menu, expand the **Settings** category and click **Service endpoints**.
1. Click **Add** to add the new endpoint. It must have the following parameters:

    <table>
      <tr><td><b>Service</b></td><td>Microsoft.Storage</td></tr>
      <tr><td><b>Subnet</b></td><td>Name of subnet in which the storage account will be deployed</td></tr>      
    </table>

For more information on creating endpoints, see [Create and associate service endpoint policies](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoint-policies).

### Deploy to Existing Virtual Network
To deploy MATLAB Web App Server to an existing virtual network, in the deployment template, set the **Deploy to New or Existing Virtual Network** parameter to `existing`.

Set the following parameter values in the template based on your existing virtual network. 

| Parameter Name    | Value     |
|-------------------|-----------|
| **Resource Group Name of Virtual Network** |   Specify the name of the Azure resource group that has your existing virtual network. |
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the existing virtual network where the server will be deployed. |
| **Virtual Network CIDR Range** |  Specify existing virtual network CIDR range. |
| **Name of Subnet for MATLAB Web App Server** | Specify the name of a subnet within the existing virtual network that the server can use. |
| **Server Subnet CIDR Range** |  Specify existing virtual network subnet CIDR range. |
| **Specify Private IP Address to VM Hosting MATLAB Web App Server** |   Specify a private IP address to the VM hosting the server. For example: 10.0.0.4 . |

## How do I configure OIDC authentication?
1. To use OIDC authentication on the server, you need to register with an IdP such as Microsoft® Azure® AD, or Google® Identity Platform. MATLAB Web App Server must be registered as an application with the IdP.
1. During the registration process, you need a redirect URL for MATLAB Web App Server. The format of the URL is: `https://<MATLABWebAppServer_hostname>:<port_server_is_running_on>/webapps/extauth/callback`. For example: `https://example.com:9988/webapps/extauth/callback`.
1. Create a file named `webapps_authn.json` using the JSON schema specified [here](https://www.mathworks.com/help/webappserver/ug/authentication.html#mw_908077ba-725e-4cc9-a906-a1bf29fceaf8) and place it in the `webapps_private` folder of the server. For folder location, see the [doc](https://www.mathworks.com/help/webappserver/ug/authentication.html#mw_146e67b0-5dff-4310-8d5d-544250e931a9).
1. To place the `webapps_authn.json` file in the `webapps_private` folder of the server, you need to remotely connect to the server using RDP on Windows or SCP on Linux. Once connected, you can drag-and-drop the `webapps_authn.json` file you created into the `webapps_private` folder of the server. Alternatively, you can drop the file into the file share first, before moving it to the `webapps_private` folder.
1. Restart the server by executing `webapps-restart` from a terminal on the server machine. The `webapps-restart` command is located in the `script` folder within the default installation location. For the default location, see the [doc](https://www.mathworks.com/help/webappserver/ug/set-up-matlab-web-app-server.html#responsive_offcanvas).
	
## How do I remotely connect to the server virtual machine?
### Windows Virtual Machine
1. Select the `webapp-vm` virtual machine resource from the resource group where MATLAB Web App Server was deployed.
1. Select `Connect` from the top navigation pane.
1. Select `RDP` from the drop-down menu.
1. In the IP address field, select the public IP address of the virtual machine. Leave the port as 3389.
1. Click `Download RDP File` and open the file.
1. Double-click the downloaded file to connect to the virtual machine.
1. Log in using the username and password you specified in the <strong>Configure Cloud Resources</strong> step of the deployment process.
### Linux Virtual Machine
1. Select the `webapp-vm` virtual machine resource from the resource group where MATLAB Web App Server was deployed.
1. Select `Connect` from the top navigation pane.
1. Select `Native SSH`. Follow the instructions to connect to the virtual machine.

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
