---
page_type: sample
languages:
- python
products:
- azure
description: "This sample shows how to manage your storage account using the Azure Storage Management package for Python."
urlFragment: Hybrid-Python-Samples
---

# Hybrid-Python-Samples

This sample shows how to manage your storage account using the Azure Storage Management package for Python. The Storage Resource Provider is a client library for working with the storage accounts in your Azure subscription. Using the client library, you can create a new storage account, read its properties, list all storage accounts in a given subscription or resource group, read and regenerate the storage account keys, and delete a storage account.  

**On this page**

- [Run this sample](#run)
- What is example.py doing?
    - Check storage account name availability
    - Create a new storage account
    - Get the properties of an account
    - List storage accounts
    - List storage accounts by resource group
    - Get the storage account keys
    - Regenerate a storage account key
    - Delete a storage account
    - Usage

<a id="run"></a>
## Run this sample

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
    git clone https://github.com/Azure-Samples/Hybrid-Storage-Python-Manage-Storage-Account.git
    ```

1. Install the dependencies using pip.

    ```
    cd Hybrid-Storage-Python-Manage-Storage-Account
    pip install -r requirements.txt
    ```

1. Create a [service principal](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals) to work against AzureStack. Make sure your service principal has [contributor/owner role](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals#assign-role-to-service-principal) on your subscription.

1. Set the following JSON properties in ./azureAppSpConfig.json.

    | Variable              | Description                                                 |
    |-----------------------|-------------------------------------------------------------|
    | `clientId`            | Service principal application id.                            |
    | `clientSecret`        | Service principal application secret.                        |
    | `tenantId`            | Azure Stack Hub tenant id.                                   |
    | `subscriptionId`      | Subscription id used to access offers in Azure Stack Hub.    |
    | `resourceManagerUrl`  | Azure Stack Hub Resource Manager Endpoint.                   |
    | `location`            | Azure Resource location.                                     |

1. Run the sample.

    ```
    python example.py
    ```

