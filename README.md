---
services: Azure-Stack
platforms: python
author: viananth
---

# Hybrid-Storage-Python-Manage-Storage-Account

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

1. Export these environment variables into your current shell. 

    ```
    export AZURE_RESOURCE_LOCATION={your resource location}
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    export ARM_ENDPOINT={your AzureStack Resource Manager Endpoint}
    ```

1. Run the sample.

    ```
    python example.py
    ```

