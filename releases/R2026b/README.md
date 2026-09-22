# MATLAB Web App Server on Microsoft Azure - R2026b
Follow these steps to deploy the R2026b MATLAB Web App Server reference architecture on Microsoft Azure. To deploy reference architectures for other releases, see [Deploy Reference Architecture for Your Release](/README.md?tab=readme-ov-file#deploy-reference-architecture-for-your-release).

## Prerequisites
Before deploying MATLAB Web App Server within an existing virtual network, you must configure the virtual network to enable connectivity. For details, see [How do I deploy to an existing virtual network?](/README.md?tab=readme-ov-file#how-do-i-deploy-to-an-existing-virtual-network) in the FAQ.

## Step 1. Launch Template
To deploy resources on Azure, click **Deploy to Azure**. The Azure Portal open in your web browser.

<a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-web-app-server-on-azure%2Fmain%2Freleases%2FR2026b%2Ftemplates%2FmainTemplate.json"  target ="_blank" >  <img src="https://aka.ms/deploytoazurebutton"/>  </a>

> MATLAB Release: R2026b

<p><strong>Note:</strong> Creating resources on Azure can take up to 10 minutes.</p>

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal:

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> `VERTHAM Dev`</p>|
| **Resource group**          | Choose a name for the resource group that will hold the resources. <p><em>Example:</em> `Saveros`</p>|
| **Region**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). <p><em>Example:</em> `East US`</p> |
| **Server VM Instance Size** | Specify the VM size you plan on using for deployment. Each MATLAB Web App Server instance runs on a VM, and each instance can run multiple sessions. Choose a VM size that has at least one core per four sessions you plan on using, with a minimum of two cores. The template defaults to: `Standard_D4s_v5`. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see the Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> `Standard_D4_v4`</p> |
| **Operating System**| Choose the operating system for the server. Your options are `Windows` or `Linux`. |
|**Deploy to New or Existing Virtual Network**|  Specify whether you want to create a `new` virtual network for your deployment or use an `existing` one. When deploying to a new virtual network, by default, the following ports are opened: 443, 22, 3389, and 27000. Depending on your security requirements, you can choose to close ports 22 and 3389 after the deployment is complete. <p><p>If you are deploying to an existing virtual network, you may need to configure the network before deployment. For details, see [How do I deploy to an existing virtual network?](/README.md?tab=readme-ov-file#how-do-i-deploy-to-an-existing-virtual-network) in the FAQ.|
| **Name of Virtual Network Where MATLAB Web App Server Will Be Deployed** |  Specify the name of the virtual network where the server will be deployed.<ul><li>If deploying to a new virtual network, you can use the default `webapp-refarch-vnet` name or specify a new name for the virtual network.</li><li>If deploying to an existing virtual network, the name you specify must match the name of an existing virtual network.</li></ul> |
| **Resource Group Name of Virtual Network** | <ul><li>If deploying to a new virtual network, leave the default `resourceGroup().name` value unchanged.</li><li>If deploying to an existing virtual network, specify the name of the resource group containing the existing existing virtual network. For example: `webappserver_rsg`.</li></ul> |
| **Virtual Network CIDR Range** |  Specify the virtual network CIDR range. For example: `10.0.0.0/16` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new virtual network.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing virtual network.</li></ul> |
| **Name of Subnet for MATLAB Web App Server** | Specify the name of the subnet that the server can use.<ul><li>If deploying to a new virtual network, this specifies the name of the subnet to be created in the virtual network.</li><li>If deploying to an existing virtual network, this must match the name of a subnet in the existing virtual network.</li></ul> |
| **Server Subnet CIDR Range** |  Specify subnet CIDR range. This is a CIDR range for the subnet specified above. For example: `10.0.0.0/24` .<ul><li>If deploying to a new virtual network, specify a suitable CIDR range to be used for the new subnet.</li><li>If deploying to an existing virtual network, this must match the CIDR range of the existing subnet.</li></ul> |
| **Specify Private IP Address to VM Hosting MATLAB Web App Server** |   Specify an unused private IP address to be assigned to the VM hosting the server. For example: `10.0.0.4` .  |
| **Assign Public IP Address to VM Hosting MATLAB Web App Server** | Specify whether to assign a public IP address to the virtual machine hosting the server. This setting also controls which IP addresses are allowed to access the storage account. <ul><li>If you select `Yes`, Azure assigns the MATLAB Web App Server VM a public IP address, and you can access the storage account using the MATLAB Web App Server VM. Additionally, the first parameter in each of the following template parameters is allowed to access the storage account: <ul><li>**IP Addresses Permitted to Remote into Server VM in CIDR Notation**</li><li>**IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation**</li></ul> You can use the Azure Portal to specify additional IP address ranges that can access the storage account. To do so, in your storage account settings under **Networking**, add IP address ranges using the IP Address/Mask format.<p>**Note:** If you are using an existing virtual network, you must manually add a service endpoint to the virtual network *before* deployment. For details, see [How do I deploy to an existing virtual network?](/README.md?tab=readme-ov-file#how-do-i-deploy-to-an-existing-virtual-network) in the FAQ.</p></li><li>If you select `No`, the MATLAB Web App Server VM is assigned a private IP, and the storage account's public network access is disabled. You can access the storage account, the web apps home page, or remotely connect to the server machine from the MATLAB Web App Server VM or by creating a new virtual machine in the same virtual network as the MATLAB Web App Server deployment. This VM is called a Bastion host or jumpbox. For details, see [Overview of Azure Bastion host and jumpboxes](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/connect-to-environments-privately#overview-of-azure-bastion-host-and-jumpboxes).<p>**Note:** If you are using an existing virtual network, you must ensure the deployment subnet has default outbound internet access enabled. For more details, see [How do I deploy to an existing virtual network?](/README.md?tab=readme-ov-file#how-do-i-deploy-to-an-existing-virtual-network) in the FAQ.</p></li></ul> <p> |
| **IP Addresses Permitted to Remote into Server VM in CIDR Notation** | Specify the range of IP addresses in CIDR notation that can remote into the VM hosting MATLAB Web App Server and administer it. The format for CIDR addresses is IP Address/Mask. <p><em>Example</em>: `x.x.x.x/32`</p><ul><li> To determine your IP address, you can search for **"what is my ip address"** on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP address.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul>**Note:** Restricting access to the server using an IP address is not a form of authentication. MATLAB Web App Server supports authentication using OIDC. For details, see [Authentication](https://www.mathworks.com/help/webappserver/ug/authentication.html).|
| **IP Addresses Allowed to Access MATLAB Web App Server Apps Home Page in CIDR Notation** | Specify the range of IP addresses that can access the MATLAB Web App Server apps home page in CIDR notation. The format for CIDR addresses is IP Address/Mask. <p><em>*Example*</em>: `x.x.x.x/24`</p> You may also specify a comma separated list of CIDR addresses (no spaces). <p><em>*Example*</em>: `x.x.x.x/24,z.z.z.z/24`</p> |
| **Base64 Encoded SSL Certificate** |   Enter a string that is a base64-encoded value of an SSL certificate in PEM format. On Linux, you can Base64 encode a PEM file using the following command in the terminal: <p> ```base64 -w 0 "cert.pem" > "cert.txt"``` </p> On Windows, you can Base64 encode a PEM file with a utility such as openssl or by using the following command in a PowerShell terminal: <p> ```[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("cert.pem")) \| Set-Content -NoNewline -Encoding Ascii "cert.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here `"cert.txt"`) should be used for this parameter. <p><strong>Note:</strong><ul><li>MATLAB Web App Server only supports the `.pem` SSL certificate format.</li><li>SSL keys must be 2048 bits in length and must be private.</li><li>To use intermediate certificates, you must provide a single certificate chain file. The `.pem` file must contain the server certificate followed by the intermediate certificates concatenated in order.</li><li>SSL certificate should not be password protected.</li><li>Private key should not be password protected.</li></ul>|
| **Base64 Encoded SSL Private Key** |   Enter a string that is a base64-encoded value of an SSL private key file in PEM format. On Linux, you can Base64 encode a PEM file using the following command in the terminal: <p> ```base64 -w 0 "key.pem" > "key.txt"``` </p> On Windows, you can Base64 encode a PEM file with a utility such as openssl or by using the following command in a PowerShell terminal: <p> ```[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("key.pem")) \| Set-Content -NoNewline -Encoding Ascii "key.txt"``` </p> You may need to change the filename arguments accordingly. The contents of the output file (here `"key.txt"`) should be used for this parameter. |
| **Username to Remote into Server VM** | Specify a username to use when remoting into server VM hosting MATLAB Web App Server. The username must be at least 7 characters long. This username is also used to login to the network license manager portal. For example: `webappadmin`. You cannot use `admin` as a username. |
| **Password to Remote into Server VM and Network License Manager Web Interface** | Specify a password to use when remoting into server VM hosting MATLAB Web App Server. This password is also used to login to the network license manager portal. Password requirements are: <p><ul><li>Must be between 12-123 characters.</li><li>Have uppercase and lowercase characters.</li><li>Have a digit.</li><li>Have a special character.</li></ul> |
| **Deploy Network License Manager** | Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for MATLAB reference architecture. Select 'No' if you want to use an existing license manager. When using an existing license manager, the MATLAB Web App Server deployment and the license manager must be in the same virtual network.|
| **Location** | Region to store resources in. All resources are deployed in the same region as the resource group.<p><em>Examples:</em> `eastus, westus, westus3`</p> |

Click **Create** to begin the deployment. This can take up to 10 minutes.

## Step 3. Upload License File   
1. In the Azure Portal, click **Resource
    groups** and select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane and click **Microsoft.Template**.
1. Click **Outputs**. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Follow the instructions in the Network License Manager for MATLAB dashboard to upload your MATLAB Web App Server license.

## Step 4. Connect and Log In to the Admin Portal (Linux Server Only)
> **Note:** The Internet Explorer web browser is not supported for accessing the admin portal.

The MATLAB Web App Server admin portal provides a web-based interface to configure and manage the server instance on the cloud. The admin portal is only available for servers deployed on Ubuntu Linux. For more details on accessing and using the admin portal, see [Manage MATLAB Web App Server Using Admin Portal](https://www.mathworks.com/help/webappserver/ug/manage-matlab-web-app-server-using-admin-portal-on-aws-reference-architecture.html).

1. In the Stack details for your stack, click the **Outputs** tab.
1. Look for the key named `AdminPortalUrl` and click the corresponding URL listed under **value**. This opens the admin portal Overview page.
1. The first time you access the admin portal, log in using the following username and password:

    <table>
      <tr><td>Username</td><td>matlab-webapps-admin</td></tr>
      <tr><td>Password</td><td>matlab-webapps-admin</td></tr>
    </table>

1. After logging in for the first time, you are prompted to change the password.

## Step 5. Open the MATLAB Web App Server Apps Home Page
1.  In the Azure Portal, click **Resource
    groups** and select the resource group you created for this deployment from the list.
1.  Select **Deployments** from the left pane and click **Microsoft.Template**.
1.  Click **Outputs** from the left pane. Copy the parameter value for **webAppServerURL** and paste it in a browser.  

You are now ready to use MATLAB Web App Server on Azure. 

To run applications on MATLAB Web App Server, you need to create applications using MATLAB Compiler. For more information, see [Create Web App](https://www.mathworks.com/help/compiler/webapps/create-and-deploy-a-web-app.html) in the MATLAB Compiler documentation.

# Get Network License Manager MAC Address
>**Note:** The network license manager MAC address is available only after the deployment to the cloud is complete.

To get the MAC address of the network license manager:
1. Log in to the Network License Manager for MATLAB dashboard using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Click **Administration** and then **License**.
1. Copy the license server MAC address displayed at the top.

# Upload Apps
## Upload from Azure Portal
>**Note:** If you set **Assign Public IP Address to VM Hosting MATLAB Web App Server** to `No` in the deployment template, then public network access is disabled for the storage account, and you must use a Bastion host or jumpbox VM to connect to the storage account. For details, see [Overview of Azure Bastion host and jumpboxes](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/connect-to-environments-privately#overview-of-azure-bastion-host-and-jumpboxes).

1. Select the `appstorage<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share.
1. Select `Browse` from the left navigation pane. You see two folders: `apps` and `logs`.
1. Click the `apps` folder.
1. Click `Upload` to browse and upload your app by following the prompts.

## Upload by Remoting into Server VM
### Windows Virtual Machine
1. Remotely connect to the server VM. For details, see [How do I remotely connect to the server virtual machine?](/README.md?tab=readme-ov-file#how-do-i-remotely-connect-to-the-server-virtual-machine) in the FAQ.
1. Open File Explorer and select `This PC`.
1. Double-click `Network Drive (W:)` to open it.
1. Double-click the `apps` folder.
1. Copy your app to this folder.

**Note**: `Network Drive (W:)` is mapped to: `\\appstorage<uniqueID>.file.core.windows.net\webapps`.

### Linux Virtual Machine
1. Obtain the public IP address of the server VM. For details, see [How do I remotely connect to the server virtual machine?](/README.md?tab=readme-ov-file#how-do-i-remotely-connect-to-the-server-virtual-machine) in the FAQ.
1. From a local command shell, copy your app to the server VM in the folder `/mnt/webapps/apps` using SCP with the command format `scp <local/path/to/webapp> <username>@<virtualMachineIP>:/mnt/webapps/apps`. Authenticate using the username and password you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
For example: `scp ./mywebapp.ctf webappadmin@192.168.1.1:/mnt/webapps/apps`.

# Update SSL/TLS Certificates
The deployment generates self-signed SSL/TLS certificates for Keycloak authentication and admin portal services on the VM. For more details, including certificate requirements, see [Enable SSL on MATLAB Web App Server](https://www.mathworks.com/help/webappserver/ug/enable-ssl.html) in the MathWorks documentation.

The **Base64 Encoded SSL Certificate** and **Base64 Encoded SSL Private Key** template input parameters specify the SSL certificate and private key for MATLAB Web App Server. They encrypt HTTPS traffic between clients and MATLAB Web App Server. You may want to provide your own Web App Server SSL certificate if you own a domain name and want to avoid browser security warnings.

>**Note (Linux only):** If you replace the Web App Server SSL certificate, you must also replace the Keycloak and admin portal certificates on the VM. The SAN of the new Web App Server SSL certificate must include the SAN of each VM certificate. For details, see [Replace Keycloak Certificate](#replace-keycloak-certificate-linux-only).

## VM Certificate Locations
| Location | Purpose | CN | SAN | Default Expiration | CA file required |
|----------|---------|----|-----|--------------------|------------------|
| Linux: `/MathWorks`<br>Windows: `C:\MathWorks` | Web App Server SSL | `webapps.com` | N/A | As provided | No. |
| `/MathWorks/Keycloak/data/tls` | Keycloak authentication (Linux only) | Public fully qualified domain name (FQDN) | `localhost`, VM private DNS name | 1 year | Yes. The SAN of the Web App Server SSL certificate must include the SAN of this certificate. If using a private/internal CA, first add your root CA certificate to the system trust store. If your root CA is already in the system trust store, copy the public certificate to the corresponding `.ca` file name. |
| `/local/MathWorks/webapps/latest/config/webapps_private` | Admin portal services (Linux only) | Public fully qualified domain name (FQDN) | `localhost`, VM private DNS name | 5 years | Yes. The SAN of the Web App Server SSL certificate must include the SAN of this certificate. If using a private/internal CA, first add your root CA certificate to the system trust store. |

## Replace VM Certificates
1. Connect to the server VM using SSH. For details, see [How do I remotely connect to the server virtual machine?](/README.md?tab=readme-ov-file#how-do-i-remotely-connect-to-the-server-virtual-machine) in the FAQ.
1. Navigate to the certificate location listed in the table above.
1. Back up the existing key, certificate, and (if present) CA files.
1. Replace certificate files in place with your updated versions.
1. To apply the changes, restart the server.

## Replace Keycloak Certificate (Linux only)
To replace the Keycloak certificate, you must recreate the Keycloak Docker container and update the hostname (`KC_HOSTNAME`). Keycloak stores realm configuration, users, groups, and authentication provider connections outside the container, preserving them across container recreations.

1. Connect to the server VM using SSH. For details, see [How do I remotely connect to the server virtual machine?](/README.md?tab=readme-ov-file#how-do-i-remotely-connect-to-the-server-virtual-machine) in the FAQ.
1. Stop the Keycloak container: `docker stop mw-keycloak`
1. Delete the container: `docker rm mw-keycloak`
1. Locate the `docker_commands.log` file in the Keycloak data folder created at install time.
1. Find the `docker create` command that includes `--name mw-keycloak`.
1. Re-issue that `docker create` command, replacing the value of `-e KC_HOSTNAME=<current-value>` with the public-facing domain name for your deployment.
1. Reconnect the container to the private network: `docker network connect mw-keycloak-net mw-keycloak`
1. Start the container: `docker start mw-keycloak`

# View Log Files
## View Logs Using Azure Portal
1. Select the `appstorage<uniqueID>` storage account resource from the resource group where MATLAB Web App Server was deployed.
1. Select `File shares` from the left navigation pane under the `Data storage` category.
1. Select the `webapps` file share.
1. Select `Browse` from the left navigation pane. You see two folders: `apps` and `logs`.
1. Click the `logs` folder to view the logs.

## View Logs Using Admin Portal
1. Navigate to the admin portal using the instructions in [Step 4](#step-4-connect-and-log-in-to-the-admin-portal-linux-server-only) of the deployment process.
1. View logs on the **Audit Logs**, **Server Logs**, and **Launcher Logs** pages. For more details, see [Manage MATLAB Web App Server Using Admin Portal](https://www.mathworks.com/help/webappserver/ug/manage-matlab-web-app-server-using-admin-portal-on-aws-reference-architecture.html).
