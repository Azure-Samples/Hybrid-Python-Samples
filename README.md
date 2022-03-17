---
page_type: sample
languages:
- python
products:
- azure
description: "samples to demonstrate various interaction with azure stack using azure python SDK."
urlFragment: Hybrid-Python-Samples
---

# Hybrid-Python-Samples

This repository is for Azure Stack Hub python sdk samples. Each of the sub-directories contain README.md files detailing how to run that sample.

**Prerequisites**
Refer to this azure stack doc for more information: https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-version-profiles-python

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

1. We recommend to use a [virtual environnement](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtualenv this way:
    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

1. Clone the repository.
    ```
    git clone https://github.com/Azure-Samples/Hybrid-Python-Samples.git
    ```

1. Install the dependencies using pip.
    ```
    cd Hybrid-Storage-Python-Manage-Storage-Account
    pip install -r requirements.txt
    ```

1. Create a [service principal](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals) to work against AzureStack. Make sure your service principal has [contributor/owner role](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals#assign-role-to-service-principal) on your subscription.
1. Make a copy of `azureSecretSpConfig.json.dist` and `azureCertSpConfig.json.dist`, then rename those copies to `azureSecretSpConfig.json` and `azureCertSpConfig.json` (whichever is needed).
1. Set the following JSON properties in ./azureSecretSpConfig.json.

    | Variable                      | Description                                                  |
    |-------------------------------|--------------------------------------------------------------|
    | `clientId`                    | Service principal application id.                            |
    | `clientSecret`                | Service principal application secret.                        |
    | `tenantId`                    | Azure Stack Hub tenant id.                                   |
    | `objectId`                    | Service principal object id.                                 |
    | `subscriptionId`              | Subscription id used to access offers in Azure Stack Hub.    |
    | `resourceManagerEndpointUrl`  | Azure Stack Hub Resource Manager Endpoint.                   |
    | `location`                    | Azure Resource location.                                     |

1. Run the sample
    ```
    python example.py
    ```

