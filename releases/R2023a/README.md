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

 <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-web-app-server-on-azure%2Fstaging-doc%2Freleases%2FR2023a%2Ftemplates%2FmainTemplate.json"  target ="_blank" >  <img src="https://aka.ms/deploytoazurebutton"/>  </a>

> MATLAB Release: R2023a
<!--For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)-->
<p><strong>Note:</strong> Creating resources on Azure can take up to 10 minutes.</p>

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal :

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> `VERTHAM Dev`</p>|
| **Resource group**          | Choose a name for the resource group that will hold the resources. <p><em>Example:</em> `Saveros`</p>|
| **Region**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). <p><em>Example:</em> `East US`</p> |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Web App Server instance runs on a VM and each instance will run multiple workers. We recommend you choose a VM size where the number of cores on your VM match the number of MATLAB workers per VM you plan on using. The template defaults to: `Standard_D4_v3`. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> `Standard_D4_v3`</p> |
| **Operating System**| Choose the operating system for the server. Your options are `Windows` or `Linux`. |
|**Deploy to New or Existing Virtual Network**|  Specify whether you want to create a `new` virtual network for your deployment or use an `existing` one. When deploying to a new virtual network, by default, the ports listed in [below](#how-do-i-deploy-to-an-existing-virtual-network) are opened. Depending on your security requirements, you can choose to close ports 22 and 3389 after the deployment is complete. |
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the virtual network where the server will be deployed.<ul><li>If deploying to a new virtual network, you can use the default `webapp-refarch-vnet` name or specify a new name for the virtual network.</li><li>If deploying to an existing virtual network, the name you specify must match the name of an existing virtual network.</li></ul> |
| **Resource Group Name of Virtual Network** | <ul><li>If deploying to a new virtual network, leave the default `resourceGroup().name` value unchanged.</li><li>If deploying to an existing virtual network, specify the name of the resource group containing the existing existing virtual network. For example: `webappserver_rsg`.</li></ul> |
| **Virtual Network CIDR Range** |  Specify the virtual network CIDR range. For example: `10.0.0.0/16` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new virtual network.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing virtual network.</li></ul> |
| **Name of Subnet for MATLAB Web App Server** | Specify the name of the subnet that the server can use.<ul><li>If deploying to a new virtual network, this specifies the name of the subnet to be created in the virtual network.</li><li>If deploying to an existing virtual network, this must match the name of a subnet in the existing virtual network.</li></ul> |
| **Server Subnet CIDR Range** |  Specify subnet CIDR range. This is a CIDR range for the subnet specified above. For example: `10.0.0.0/24` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new subnet.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing subnet.</li></ul> |
| **Specify Private IP Address to VM Hosting MATLAB Web App Server** |   Specify an unused private IP address to be assigned to the VM hosting the server. For example: `10.0.0.4` .  |
| **Assign Public IP Address to VM Hosting MATLAB Web App Server** |  Select `Yes` if you want to assign a public IP address to the VM hosting the server. Otherwise, select `No`. If you select 'No', you must create a new virtual machine and add it to the same virtual network as the MATLAB Web App Server deployment. The ability to access the web apps home page or remotely connect to the server machine can be accomplished only through this virtual machine.|
| **IP Addresses Permitted to Remote into Server VM in CIDR Notation** | Specify the range of IP addresses in CIDR notation that can remote into the VM hosting MATLAB Web App Server and administer it. The format for CIDR addresses is IP Address/Mask. <p><em>Example</em>: `x.x.x.x/32`</p> You may also specify a comma separated list of CIDR addresses (no spaces). <p><em>*Example*</em>: `x.x.x.x/32,x.x.x.x/32`</p> <ul><li> To determine your IP address, you can search for **"what is my ip address"** on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul>**NOTE:** Restricting access to the server using an IP address is not a form of authentication. MATLAB Web App Server supports authentication using OIDC. For details, see [Authentication](https://www.mathworks.com/help/webappserver/ug/authentication.html).|
| **IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation** | Specify the range of IP addresses that can access the MATLAB Web App Server apps home page in CIDR notation. The format for CIDR addresses is IP Address/Mask. <p><em>*Example*</em>: `x.x.x.x/24`</p> You may also specify a comma separated list of CIDR addresses (no spaces). <p><em>*Example*</em>: `x.x.x.x/24,z.z.z.z/24`</p> |
| **Base64 Encoded SSL Certificate** |   Enter a string that is a base64-encoded value of an SSL certificate in PEM format. You can Base64 encode a PEM file using the following command in either a Windows or Linux terminal: <p> ```base64 -w 0 "cert.pem" > "cert.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here "cert.txt") should be used for this parameter. <p><strong>NOTE:</strong><ul><li>MATLAB Web App Server only supports the `.pem` SSL certificate format.</li><li>SSL keys must be 2048 bits in length and must be private.</li><li>Intermediate certificates are not supported by the server.</li><li>Private key should not be password protected.</li></ul>|
| **Base64 Encoded SSL Private Key** |   Enter a string that is a base64-encoded value of an SSL private key file in PEM format. You can Base64 encode a PEM file using the following command in either a Windows or Linux terminal: <p> ```base64 -w 0 "key.pem" > "key.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here "key.txt") should be used for this parameter. |
| **Username to Remote into Server VM** | Specify a username to use when remoting into server VM hosting MATLAB Web App Server. The username must be at least 7 characters long. This username is also used to login to the network license manager portal. For example: webappadmin. You cannot use "admin" as a username. |
| **Password to Remote into Server VM and Network License Manager Web Interface** | Specify a password to use when remoting into server VM hosting MATLAB Web App Server. This password is also used to login to the network license manager portal. Password requirements are: <p><ul><li>Must be between 12-123 characters.</li><li>Have uppercase and lowercase characters.</li><li>Have a digit.</li><li>Have a special character.</li></ul> |
| **Deploy Network License Manager** | Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for MATLAB reference architecture. Select 'No' if you want to use an existing license manager. When using an exisiting license manager, the MATLAB Web App Server deployment and the license manager must be in the same virtual network.|

Click **Create** to begin the deployment. This can take up to 10 minutes.

## Step 3. Upload License File   
1. In the Azure Portal, click **Resource
    groups** and select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane and click **Microsoft.Template**.
1. Click **Outputs**. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Follow the instructions in the Network License Manager for MATLAB dashboard to upload your MATLAB Web App Server license.


## Step 4. Open the MATLAB Web App Server Apps Home Page
1.  In the Azure Portal, click **Resource
    groups** and select the resource group you created for this deployment from the list.
1.  Select **Deployments** from the left pane and click **Microsoft.Template**.
1.  Click **Outputs** from the left pane. Copy the parameter value for **webAppServerURL** and paste it in a browser.  

You are now ready to use MATLAB Web App Server on Azure. 

To run applications on MATLAB Web App Server, you need to create applications using MATLAB Compiler. For more information, see [Create Web App](https://www.mathworks.com/help/compiler/webapps/create-and-deploy-a-web-app.html) in the MATLAB Compiler documentation.

# Get Network License Manager MAC Address
>**NOTE:**The network license manager MAC address is available only after the deployment to the cloud is complete.
To get the MAC address of the network license manager:
1. Log in to the Network License Manager for MATLAB dashboard using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Click Administration > License.
1. Copy the license server MAC address displayed at the top.

# Upload Apps
1. Select the `webapp<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share and click the `ctfs` folder.
1. Click `Upload` to browse and upload your app by following the prompts.

# View Log Files
1. Select the `webapp<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share and click the `logs` folder to view the logs.

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

### Resources
| Resource Name  | Type | Description                                                                                                                                                                                                                                                                                                                        |
|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `netlm-nsg`        | Network security group | Filter network traffic to and from network license manager resources in an Azure virtual network. |
| `netlm-server`        | Virtual machine  | Virtual machine to host network license manager. |
|  `netlm-server-ip` | Public IP address | Provide public IP address to network license manager. |
|  `netlm-server-nic` | Network interface | Provide network interface for network license manager. |
|  `netlm-server_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting network license manager. |
| `webapp-public-ip` | Public IP address | Public IP address to connect to MATLAB Web App Server. |
| `webapp-refarch-vnet`   | Virtual network | Enable resources to communicate with each other via network. |
|  `webapp-nsg` | Network security group | Filter network traffic to and from MATLAB Web App Server resources in an Azure virtual network. |
|  `webapp-nic` | Network interface | Provide network interface for MATLAB Web App Server. |
| `webapps<uniqueID>`   | Storage account | Storage account where web app archives (.ctf files) are stored. |
| `webapp-vm`           | Virtual machine | Virtual machine to host MATLAB Web App Server.|
|  `webappVM_OsDisk_<uniqueID>` | Disk | Operating system disk attached to virtual machine hosting MATLAB Web App Server. |


# FAQ
## How do I deploy to an existing virtual network?
>**Note:** Your existing virtual network must have at least two available subnets for deployment. 
1. To deploy MATLAB Web App Server to an existing virtual network, set the **Deploy to New or Existing Virtual Network** paratmeter to `existing`.  
1. Set the following parameter values in the [Configure Cloud Resources](#step-2-configure-cloud-resources) section based on your existing virtual network and open the ports listed below. 

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Resource Group Name of Virtual Network** |   Specify the name of the Azure resource group that has your existing virtual network. |
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the existing virtual network where the server will be deployed. |
| **Virtual Network CIDR Range** |  Specify existing virtual network CIDR range. |
| **Name of Subnet for MATLAB Web App Server** | Specify the name of a subnet within the existing virtual network that the server can use. |
| **Server Subnet CIDR Range** |  Specify existing virtual network subnet CIDR range. |
| **Specify Private IP Address to VM Hosting MATLAB Web App Server** |   Specify a private IP address to the VM hosting the server. For example: 10.0.0.4 . |

**Ports to Open in Existing Virtual Network**

| Port | Description |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `443` | HTTPS - the port Web App Server will service if SSL is enabled |
| `22` | SSH - used for remoting into Linux machines |
| `3389` | RDP - used for remoting into Windows machines |
| `27000` | Required for communication between network license manager and Web App Server |



## How do I launch a template that uses a previous MATLAB release?
You may use one of the deploy buttons below to deploy an older release of MATLAB Web App Server Reference Architecture. Note that the operating system is a parameter of the ARM template.
| Release | Windows Server / Ubuntu                                                                 
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2022b  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-web-app-server-on-azure%2Fstaging-doc%2Freleases%2FR2022b%2Ftemplates%2FmainTemplate.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |
| R2022a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-web-app-server-on-azure%2Fstaging-doc%2Freleases%2FR2022a%2Ftemplates%2FmainTemplate.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |


## How do I configure OIDC authentication?
1. To use OIDC authentication on the server, you need to register with an IdP such as Microsoft® Azure® AD, or Google® Identity Platform. MATLAB Web App Server must be registered as an application with the IdP.
1. During the registration process, you need a redirect URL for MATLAB Web App Server. The format of the URL is: `https://<MATLABWebAppServer_hostname>:<port_server_is_running_on>/webapps/extauth/callback`. For example: `https://example.com:9988/webapps/extauth/callback`.
1. Create a file named `webapps_authn.json` using the JSON schema specified [here](https://www.mathworks.com/help/webappserver/ug/authentication.html#mw_908077ba-725e-4cc9-a906-a1bf29fceaf8) and place it in the `webapps_private` folder of the server. For folder location, see the [doc](https://www.mathworks.com/help/webappserver/ug/authentication.html#mw_146e67b0-5dff-4310-8d5d-544250e931a9).
1. To place the `webapps_authn.json` file in the `webapps_private` folder of the server, you need to remotely connect to the server using RDP on Windows or SCP on Linux. Once connected, you can drag-and-drop the `webapps_authn.json` file you created into the `webapps_private` folder of the server. Alternatively, you can drop the file into the file share first, before moving it to the `webapps_private` folder.
1. Restart the server by executing `webapps-restart` from a terminal on the the server machine. The `webapps-restart` command is located in the `script` folder within the default installation location. For default location, see the [doc](https://www.mathworks.com/help/webappserver/ug/set-up-matlab-web-app-server.html#responsive_offcanvas).

## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime |
|---------------|----------------|
| MATLAB R2023a |  R2020b, R2021a, R2021b, R2022a, R2022b, R2023a |
| MATLAB R2022b |  R2020a, R2020b, R2021a, R2021b, R2022a, R2022b |  
| MATLAB R2022a |  R2019b, R2020a, R2020b, R2021a, R2021b, R2022a |    

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
