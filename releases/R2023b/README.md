# MATLAB Web App Server on Microsoft Azure - R2023b
Follow these steps to deploy the R2023b MATLAB Web App Server reference architecture on Microsoft Azure. To deploy reference architectures for other releases, see [Deploy Reference Architecture for Your Release](/README.md#deploy-reference-architecture-for-your-release). 

## Step 1. Launch Template
To deploy resources on Azure, click **Deploy to Azure**. The Azure Portal open in your web browser.

<a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-web-app-server-on-azure%2Fmain%2Freleases%2FR2023b%2Ftemplates%2FmainTemplate.json"  target ="_blank" >  <img src="https://aka.ms/deploytoazurebutton"/>  </a>

> MATLAB Release: R2023b

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
|**Deploy to New or Existing Virtual Network**|  Specify whether you want to create a `new` virtual network for your deployment or use an `existing` one. When deploying to a new virtual network, by default, the ports listed [here](/README.md#ports-to-open-in-existing-virtual-network) are opened. Depending on your security requirements, you can choose to close ports 22 and 3389 after the deployment is complete. |
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the virtual network where the server will be deployed.<ul><li>If deploying to a new virtual network, you can use the default `webapp-refarch-vnet` name or specify a new name for the virtual network.</li><li>If deploying to an existing virtual network, the name you specify must match the name of an existing virtual network.</li></ul> |
| **Resource Group Name of Virtual Network** | <ul><li>If deploying to a new virtual network, leave the default `resourceGroup().name` value unchanged.</li><li>If deploying to an existing virtual network, specify the name of the resource group containing the existing existing virtual network. For example: `webappserver_rsg`.</li></ul> |
| **Virtual Network CIDR Range** |  Specify the virtual network CIDR range. For example: `10.0.0.0/16` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new virtual network.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing virtual network.</li></ul> |
| **Name of Subnet for MATLAB Web App Server** | Specify the name of the subnet that the server can use.<ul><li>If deploying to a new virtual network, this specifies the name of the subnet to be created in the virtual network.</li><li>If deploying to an existing virtual network, this must match the name of a subnet in the existing virtual network.</li></ul> |
| **Server Subnet CIDR Range** |  Specify subnet CIDR range. This is a CIDR range for the subnet specified above. For example: `10.0.0.0/24` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new subnet.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing subnet.</li></ul> |
| **Specify Private IP Address to VM Hosting MATLAB Web App Server** |   Specify an unused private IP address to be assigned to the VM hosting the server. For example: `10.0.0.4` .  |
| **Assign Public IP Address to VM Hosting MATLAB Web App Server** |  Select `Yes` if you want to assign a public IP address to the VM hosting the server. Otherwise, select `No`. If you select 'No', you must create a new virtual machine and add it to the same virtual network as the MATLAB Web App Server deployment. The ability to access the web apps home page or remotely connect to the server machine can be accomplished only through this virtual machine.|
| **IP Addresses Permitted to Remote into Server VM in CIDR Notation** | Specify the range of IP addresses in CIDR notation that can remote into the VM hosting MATLAB Web App Server and administer it. The format for CIDR addresses is IP Address/Mask. <p><em>Example</em>: `x.x.x.x/32`</p><ul><li> To determine your IP address, you can search for **"what is my ip address"** on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP address.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul>**NOTE:** Restricting access to the server using an IP address is not a form of authentication. MATLAB Web App Server supports authentication using OIDC. For details, see [Authentication](https://www.mathworks.com/help/webappserver/ug/authentication.html).|
| **IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation** | Specify the range of IP addresses that can access the MATLAB Web App Server apps home page in CIDR notation. The format for CIDR addresses is IP Address/Mask. <p><em>*Example*</em>: `x.x.x.x/24`</p> You may also specify a comma separated list of CIDR addresses (no spaces). <p><em>*Example*</em>: `x.x.x.x/24,z.z.z.z/24`</p> |
| **Base64 Encoded SSL Certificate** |   Enter a string that is a base64-encoded value of an SSL certificate in PEM format. On Windows, you can Base64 encode a PEM file using a utility such as openssl. On Linux, you can Base64 encode a PEM file using the following command in the terminal: <p> ```base64 -w 0 "cert.pem" > "cert.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here "cert.txt") should be used for this parameter. <p><strong>NOTE:</strong><ul><li>MATLAB Web App Server only supports the `.pem` SSL certificate format.</li><li>SSL keys must be 2048 bits in length and must be private.</li><li>Intermediate certificates are not supported by the server.</li><li>SSL certificate should not be password protected.</li><li>Private key should not be password protected.</li></ul>|
| **Base64 Encoded SSL Private Key** |   Enter a string that is a base64-encoded value of an SSL private key file in PEM format. On Windows, you can Base64 encode a PEM file using a utility such as openssl. On Linux, you can Base64 encode a PEM file using the following command in the terminal: <p> ```base64 -w 0 "key.pem" > "key.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here "key.txt") should be used for this parameter. |
| **Username to Remote into Server VM** | Specify a username to use when remoting into server VM hosting MATLAB Web App Server. The username must be at least 7 characters long. This username is also used to login to the network license manager portal. For example: webappadmin. You cannot use "admin" as a username. |
| **Password to Remote into Server VM and Network License Manager Web Interface** | Specify a password to use when remoting into server VM hosting MATLAB Web App Server. This password is also used to login to the network license manager portal. Password requirements are: <p><ul><li>Must be between 12-123 characters.</li><li>Have uppercase and lowercase characters.</li><li>Have a digit.</li><li>Have a special character.</li></ul> |
| **Deploy Network License Manager** | Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for MATLAB reference architecture. Select 'No' if you want to use an existing license manager. When using an existing license manager, the MATLAB Web App Server deployment and the license manager must be in the same virtual network.|

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
## Upload from Azure Portal
1. Select the `appstorage<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share.
1. Select `Browse` from the left navigation pane. You see two folders: `apps` and `logs`.
1. Click the `apps` folder.
1. Click `Upload` to browse and upload your app by following the prompts.
## Upload by Remoting into Server VM
### Windows Virtual Machine
1. Remotely connect to the server VM. For details, see [How do I remotely connect to the server virtual machine?](/README.md#how-do-i-remotely-connect-to-the-server-virtual-machine).
1. Open File Explorer and select `This PC`.
1. Double-click `Network Drive (W:)` to open it.
1. Double-click the `apps` folder.
1. Copy your app to this folder.

**Note**: `Network Drive (W:)` is mapped to: `\\appstorage<uniqueID>.file.core.windows.net\webapps`.

### Linux Virtual Machine
1. Obtain the public IP address of the server VM. For details, see [How do I remotely connect to the server virtual machine?](/README.md#how-do-i-remotely-connect-to-the-server-virtual-machine).
1. From a local command shell, copy your app to the server VM in the folder `/mnt/webapps/apps` using SCP with the command format `scp <local/path/to/webapp> <username>@<virtualMachineIP>:/mnt/webapps/apps`. Authenticate using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
For example: `scp ./mywebapp.ctf webappadmin@192.168.1.1:/mnt/webapps/apps`.

# View Log Files
1. Select the `appstorage<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share.
1. Select `Browse` from the left navigation pane. You see two folders: `apps` and `logs`.
1. Click the `logs` folder to view the logs.
