# MATLAB Web App Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Web App Server™ license. For details, see [Configure MATLAB Web App Server Licensing on the Cloud](https://www.mathworks.com/help/webappserver/ug/configure-server-license-on-cloud.html). To configure a license for use on the cloud, you need the MAC address of the network license manager on the cloud. This can be obtained from the network license manager webpage after deploying MATLAB Web App Server on Azure reference architecture. For details, see [Get License Server MAC Address](#get-network-license-manager-mac-address).    
-   A Microsoft Azure™ account.

# Costs
You are responsible for the cost of the Azure services used when you create cloud resources using this guide. Resource settings, such as instance type, will affect the cost of deployment. For cost estimates, see the pricing pages for each Azure
service you will be using. Prices are subject to change.


# Introduction 

The following guide will help you automate the process of running MATLAB Web App Server on Azure using your Azure account. The automation is accomplished using an Azure Resource Manager (ARM) template. The template is a JSON file that defines the resources needed to deploy and manage MATLAB Web App
Server on Azure. For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources).

Deploying MATLAB Web App Server on Azure automatically deploys a network license manager. However, you can also use an existing network license manager with MATLAB Web App Server on Azure by selecting `existing` from the deployment template. 

# Deployment Steps

## Step 1. Launch Template
Click the **Deploy to Azure** button to deploy resources on
    Azure. This will open the Azure Portal in your web browser.

 <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-Web App-server-on-azure%2Fmaster%2Freleases%2FR2022a%2Ftemplates%2Fazuredeploy22a.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a>

> MATLAB Release: R2022a


<!--For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)-->
<p><strong>Note:</strong> Creating resources on Azure can take at least 30 minutes.</p>

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal :

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> VERTHAM Dev</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Resource group**          | Choose a name for the resource group that will hold the resources. It is recommended you create a new resource group for each deployment. This allows all resources in a group to be deleted simultaneously. <p><em>Example:</em> Saveros</p>                                                                                                                                                                                                                                                                       |
| **Region**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). We recommend you use East US or East US 2. <p><em>Example:</em> East US</p> |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Web App Server instance runs on a VM and each instance will run multiple workers. We recommend you choose a VM size where the number of cores on your VM match the number of MATLAB workers per VM you plan on using. The template defaults to: `Standard_D4s_v3`. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D4s_v3</p> |
| **Operating System**| Choose the operating system for the server. Your options are `Windows` or `Linux`. |
| **Assign Public IP Address to VM Hosting MATLAB Web App Server** |  Select `Yes` if you want to assign a public IP address to the VM hosting the server. Otherwise, select `No`.|
| **IP Addresses Permitted to Remotely Connect to Server VM in CIDR Notation** | Specify the range of IP addresses in CIDR notation that can remotely connect to the VM hosting MATLAB Web App Server and administer it. The IP address can be a single IP address or a range of IP addresses. The format for this field is IP Address/Mask.<p><em>Example</em>: `x.x.x.x/32`<ul><li>This is the public IP address which can be found by searching for **"what is my ip address"** on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul>**NOTE:** Restricting access to the server using an IP address is not a form of authentication. MATLAB Web App Server supports authentication using OIDC. For details, see [Authentication](https://www.mathworks.com/help/webappserver/ug/authentication.html).</p>|
| **IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation** | Specify the range of IP addresses that can access the MATLAB Web App Server apps home page in CIDR notation. The format for this field is IP Address/Mask.<p><em>*Example*</em>: `x.x.x.x/24`</p> |
|**Deploy to New or Existing Virtual Network**|  Specify whether you want to create a new virtual network for your deployment or use an exisiting one. When deploying to a new virtual network, by default, the ports listed in [How do I use an existing virtual network to deploy MATLAB Web App Server?](#how-do-i-use-an-existing-virtual-network-to-deploy-matlab-web-app-server?) are opened. You can close ports 22 and 3389 after deployment is complete. |
| **Resource Group Name of Virtual Network** |   Specify the name of the Azure resource group if you are deploying to an existing virtual network. For example: webappserver_rsg. Leave unchanged if deploying to a new virtual network.|
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the virtual network where the server will be deployed. For example: webappserver-vnet. Leave unchanged if deploying to a new virtual network.|
| **Virtual Network CIDR Range** |  Specify virtual network CIDR range. For example: 123.456.789.111/24 . Leave unchanged if deploying to a new virtual network.|
| **Name of Subnet for MATLAB Web App Server** | Specify the name of the subnet that the server can use. This is a subnet name from an existing virtual network. Leave unchanged if deploying to a new virtual network.|
| **Subnet CIDR Range** |  Specify subnet CIDR range. This is a CIDR range for the subnet specified above. For example: 123.456.789.111/24 . Leave unchanged if deploying to a new virtual network. |
| **Name of Subnet for Application Gateway** | Specify the name of the subnet the application gateway can use. This is a subnet name from an existing virtual network. Leave unchanged if deploying to a new virtual network.| 
| **Subnet CIDR Range** | Specify subnet CIDR range. This is a CIDR range for subnet specified above. For example: 123.456.789.111/24 . Leave unchanged if deploying to a new virtual network.|
| **Assign Private IP Address to Application Gateway from Subnet** |   Specify a private IP address to the application gateway by selecting one from the subnet for the application gateway. For example: 10.0.1.4 . Leave unchanged if deploying to a new virtual network. |
| **Base64Encoded SSL Certificate Data in PFX Format** |   Enter a string that is a base64-encoded value of an SSL certificate in PFX format that you are using for this deployment.|
| **Password for Base64-encoded SSL Certificate** |   Enter the password for base64-encoded SSL certificate.|
| **Username to Remotely Connect to Server VM** | Specify a username to use when connecting remotely to server VM hosting MATLAB Web App Server. For example: webappadmin. You cannot use "admin" as a username.|                                                       | **Password to Remotely Connect to Server VM and Network License Manager Web Interface** | Specify a password to use when connecting remotely to server VM hosting MATLAB Web App Server. This password is also used to login to the network license manager web interface.|
| **Deploy Network License Manager** | Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for MATLAB reference architecture. Select 'No' if you want to use an exisitng license server.|

Click **Purchase** to begin the deployment. This can take up to 40 minutes.

## Step 3. Upload License File   
1. In the Azure Portal, click **Resource
    groups** and select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane and click **Microsoft.Template**.
1. Click **Outputs**. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Follow the instructions in the Network License Manager for MATLAB dashboard to upload your MATLAB Web App Server license.


## Step 4. Open the MATLAB Web App Server Apps Home Page
1.  In the Azure Portal, click **Resource
    groups** and select the resource group you created for this deployment from the list.
1.  Select **Deployments** from the left pane and click **Microsoft.Template**.
1.  Click **Outputs** from the left pane. Copy the parameter value for **webAppServerURL** and paste it in a browser.  

You are now ready to use MATLAB Web App Server on Azure. 

To run applications on MATLAB Web App Server, you need to create applications using MATLAB Compiler. For more information, see [Create Web App](https://www.mathworks.com/help/compiler/webapps/create-and-deploy-a-web-app.html) in the MATLAB Compiler documentation.

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

### Resources
| Resource Name  | Type | Description                                                                                                                                                                                                                                                                                                                        |
|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  `app-gw-sg` | Network security group | Filter network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
|  `appGw-public-ip` | Provide public IP address | Public IP address to application gateway. |
| `appGw<uniqueID>`    | Application gateway | Provide routing and load balancing service to MATLAB Web App Server instance.|
| `netlm-nsg`        | Network security group | Filter network traffic to and from network license manager resources in an Azure virtual network. |
| `netlm-server`        | Virtual machine  | Virtual machine to host network license manager. |
|  `netlm-server-ip` | Public IP address | Provide public IP address to network license manager. |
|  `netlm-server-nic` | Network interface | Provide network interface for network license manager. |
|  `netlm-server_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting network license manager. |
| `servermachine-public-ip` | Public IP address | Public IP address to connect to MATLAB Web App Server. |
| `webapp-refarch-vnet`   | Virtual network | Enable resources to communicate with each other via network. |
|  `webapp-sg-temp` | Network security group | Filter network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
|  `webappNic` | Network interface | Provide network interface for MATLAB Web App Server. |
| `webapps<uniqueID>`   | Storage account | Storage account where web app archives (.ctf files) are stored. |
| `webappVM`           | Virtual machine | Virtual machine to host MATLAB Web App Server.|
|  `webappVM_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting MATLAB Web App Server. |

<!--| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Purpose                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Gateway Network Security Group |  `app-gw-sg` | 1 | Filters network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
| Application Gateway Public IP |  `appGw-public-ip` | 1 | Public IP address of application gateway. |
| Application Gateway | `appGw<uniqueID>`    | 1 | Provides routing and load balancing service to MATLAB Web App Server instance.|
| Network License Manager Network Security Group | `netlm-nsg`        | 1 | Filters network traffic to and from network license manager resources in an Azure virtual network. |
| Network License Manager Server | `netlm-server`        | 1  | Virtual machine hosting network license manager. |
| Network License Manager Public IP |  `netlm-server-ip` | 1 | Network license manager public IP adddress. |
| Network License Manager NIC |  `netlm-server-nic` | 1 | Provides network interface for network license manager. |
| Network License Manager OS Disk |  `netlm-server_OsDisk_<uniqueID>` | 1 | Operating system disk attached to virtual machine hosting network license manager. |
| MATLAB Web App Server Public IP                           | `servermachine-public-ip` | 1                   | Public IP address to connect to MATLAB Web App Server. |
| Virtual Network                                                           | `webapp-refarch-vnet`   | 1                   | Enables resources to communicate with each other. |
| MATLAB Web App Server Network Security Group |  `webapp-sg-temp` | 1 | Filters network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
| MATLAB Web App Server NIC |  `webappNic` | 1 | Provides network interface for MATLAB Web App Server. |
| Storage account                                                            | `webapps<uniqueID>`   | 1                  | Storage account where web app archives (.ctf files) are stored. |
| MATLAB Web App Server Virtual Machine | `webappVM`           | 1                   | Virtual machine hosting MATLAB Web App Server.|
| MATLAB Web App Server OS Disk |  `webappVM_OsDisk_<uniqueID>` | 1 | Operating system disk attached to virtual machine hosting MATLAB Web App Server. |-->


# FAQ
## How do I use an existing virtual network to deploy MATLAB Web App Server?
In addition to the parameters specified in the section [Configure Cloud Resources](#step-2-configure-cloud-resources), you will also need to open the following ports in your virtual network:

| Port | Description |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `443` | Required for communicating with the dashboard. |
| `8000`, `8004`, `8080`, `9090`, `9910` | Required for communication between the dashboard, MATLAB Web App Server workers, and various microservices within the virtual network.  These ports do not need to be open to the internet. |
| `27000` | Required for communication between network license manager and the workers. |
| `65200` - `65535` | Required for the Azure application gateway health check to work. These ports need to be accessible over the internet. For more information, see [MSDN Community](https://social.msdn.microsoft.com/Forums/azure/en-US/96a77f18-3b71-45d2-a213-c4ba63fd4e63/internal-application-gateway-backend-health-is-unkown?forum=WAVirtualMachinesVirtualNetwork). |
| `22`, `3389` | (Optional) Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |


## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime |
|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|-----------------|---------------|
| MATLAB R2020b | R2018a | R2018b | R2019a | R2019b | R2020a | R2020b |
| MATLAB R2021a |  | R2018b | R2019a | R2019b | R2020a | R2020b | R2021a |
| MATLAB R2021b |  |  | R2019a | R2019b | R2020a | R2020b |R2021a | R2021b |
| MATLAB R2022a |  |  |  | R2019b | R2020a | R2020b |R2021a | R2021b | R2022a |



## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors result from either CORS not being enabled on the server or due to the fact that the server endpoint uses a self-signed 
certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit the Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-Web App-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and Javascript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Or you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate to Application Gateway](https://www.mathworks.com/help/mps/server/configure-azure-resources-reference-architecture.html#mw_6ae700e7-b895-4e90-b0fb-7292e905656e_sep_mw_1fd15ea2-d161-4694-963d-41a81fc773bf). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).