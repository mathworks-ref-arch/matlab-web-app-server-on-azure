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
| **Location**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). We recommend you use East US or East US 2. <p><em>Example:</em> East US</p>                                                                                                                                                                                                                          |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Web App Server instance runs on a VM and each instance will run multiple workers. We recommend you choose a VM size where the number of cores on your VM match the number of MATLAB workers per VM you plan on using. The template defaults to: `Standard_D4s_v3`. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D4s_v3</p> |
| **Platform**| Choose the operating system for the server. Microsoft Windows and Linux are the only available options. |
| **Assign Public IP to Instance Hosting MATLAB Web App Server** |  <details> |
| **IP Addresses Permitted to Remote into Server VM in CIDR Notation** | Specify the IP address of the administrator using CIDR notation. The administrator can remotely connect to the EC2 instance that hosts MATLAB Web App Server and administer it. The IP address can be a single IP address or a range of IP addresses. The format for this field is IP Address/Mask.The format for this field is IP Address/Mask. <p><em>Example</em>: `x.x.x.x/32`<ul><li>This is the public IP address which can be found by searching for **"what is my ip address"** on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul>**NOTE:** Restricting access to the server using an IP address is not a form of authentication. MATLAB Web App Server supports authentication using LDAP and OIDC. For details, see [Authentication](https://www.mathworks.com/help/webappserver/ug/authentication.html).</p>|
| **IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page** | Complete this field only if you selected **"No"** in the previous field. Specify the range of IP addresses that can access the MATLAB Web App Server apps home page in CIDR notation. The format for this field is IP Address/Mask.<p><em>*Example*</em>: `x.x.x.x/24`</p> |
|**New or Existing Virtual Network**|  Specify whether you want to create a new virtual network for your deployment or use an exisiting one. You can use the default values or enter new values based on your network setup for the following paramaters. <br/><br/> When deploying in a new virtual network, by default, the deployment keeps the ports listed in [How do I use an existing virtual network to deploy MATLAB Web App Server?](#How-do-I-use-an-existing-virtual-network-to-deploy-MATLAB-Web App-Server) open. You can close ports 22 and 3389 after deployment is complete. |
| **Virtual Network Name** |  Specify the name of your existing virtual network or use the default value.   |
| **Virtual Network CIDR Range** |  Specify the IP address range of the virtual network in CIDR notation or use the default value. |
| **Subnet for Server** | Specify the subnet for the server. |
| **Subnet for Server--CIDR Range** |  Specify the IP address range of the first subnet in CIDR notation or use the default value. The first subnet hosts the dashboard and other resources. |
| **Subnet for Application Gateway** | Specify the subnet for the application gateway.| 
| **Subnet for Application Gateway--CIDR Range** | Specify the IP address range of the second subnet in CIDR notation or use the default value. The second subnet hosts the application gateway. |
| **Subnet for Application Gateway--Available Private IP Address** |   Specify an unused IP address from Subnet 2 or use the default value. This IP address serves as the private IP of the application gateway. |
| **Resource Group Name Of Virtual Network** |   Specify the resource group name of the virtual network or use the default value.    |
| **Base64Encoded PFX Certificate Data** |   Enter a string that is a base64-encoded value of an SSL certificate in PFX format.    |
| **Password for Base64-encoded PFX Certificate** |   If the certificate requires a password, enter it here. Otherwise, leave the field blank.    |
| **Admin Username** | Specify the administrator user name for all VMs. Use this user name to log in to the MATLAB Web App Server dashboard.|                                                                      
| **Admin Password** | Specify the administrator password for all VMs. Use this password to log in to the MATLAB Web App Server dashboard. If you also deploy the network license manager, use this password to log in to the network license manager dashboard.|
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
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Gateway Network Security Group |  `app-gw-sg` | 1 | TBD |
| Application Gateway Public IP |  `appGw-public-ip` | 1 | TBD |
| Application Gateway | `appGw<uniqueID>`    | 1                   | Provides routing and load balancing service to MATLAB Web App Server instances.|
| Network License Manager Network Security Group | `netlm-nsg`        | 1                   | TBD |
| Network License Manager | `netlm-server`        | 1                   | TBD |
| Network License Manager Public IP |  `netlm-server-ip` | 1 | TBD |
| Network License Manager NIC |  `netlm-server-nic` | 1 | TBD |
| Network License Manager OS Disk |  `netlm-server_OsDisk_<uniqueID>` | 1 | TBD |
| MATLAB Web App Server Public IP                           | `servermachine-public-ip` | 1                   | Public IP address to connect to MATLAB Web App Server. |
| Virtual Network                                                           | `webapp-refarch-vnet`   | 1                   | Enables resources to communicate with each other. |
| MATLAB Web App Server Network Security Group |  `webapp-sg-temp` | 1 | TBD |
| MATLAB Web App Server NIC |  `webappNic` | 1 | TBD |
| Storage account                                                            | `webapps<uniqueID>`   | 1                  | Storage account where the deployable archives (CTF files) are stored. |
| MATLAB Web App Server Virtual Machine | `webappVM`           | 1                   | Virtual machine (VM) that hosts MATLAB Web App Server.|
| MATLAB Web App Server OS Disk |  `webappVM_OsDisk_<uniqueID>` | 1 | TBD |


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