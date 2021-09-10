---
page_type: sample
languages:
- python
products:
- azure
description: "This sample explains how to use Azure Resource Manager templates to deploy your Resources to AzureStack."
urlFragment: Hybrid-Resource-Manager-Python-Template-Deployment
---

# Hybrid-Resource-Manager-Python-Template-Deployment

This sample explains how to use Azure Resource Manager templates to deploy your Resources to AzureStack. It shows how to
deploy your Resources by using the Azure SDK for Python.

When deploying an application definition with a template, you can provide parameter values to customize how the
resources are created. You specify values for these parameters either inline or in a parameter file.

## Incremental and complete deployments

By default, Resource Manager handles deployments as incremental updates to the resource group. With incremental
deployment, Resource Manager:

- leaves unchanged resources that exist in the resource group but are not specified in the template
- adds resources that are specified in the template but do not exist in the resource group
- does not re-provision resources that exist in the resource group in the same condition defined in the template

With complete deployment, Resource Manager:

- deletes resources that exist in the resource group but are not specified in the template
- adds resources that are specified in the template but do not exist in the resource group
- does not re-provision resources that exist in the resource group in the same condition defined in the template

You specify the type of deployment through the Mode property, as shown in the examples below.

## Deploy with Python

In this sample, we are going to deploy a resource template which contains an Ubuntu 16.04 LTS virtual machine using
ssh public key authentication, storage account, and virtual network with public IP address. The virtual network
contains a single subnet with a single network security group rule which allows traffic on port 22 for ssh with a single
network interface belonging to the subnet. The virtual machine is a `Standard_A1` size. You can find the template
[here](https://github.com/azure-samples/Hybrid-Resource-Manager-Python-Template-Deployment/blob/master/templates/template.json).

### To run this sample, do the following:


 Run the script.
    
    ```
    python example.py
    ```

### What is this azure_deployment.py Doing?

The entry point for this sample is [example.py](https://github.com/azure-samples/Hybrid-Resource-Manager-Python-Template-Deployment/blob/master/azure_deployment.py). This script uses the `Deployer` class
below to deploy the aforementioned template to the subscription and resource group specified in `my_resource_group`
and `my_subscription_id` respectively. By default the script will use the ssh public key from your default ssh
location. please make sure it's present in ~/id_rsa.pub location.


After the script runs, you should see something like the following in your output:

```
$ python example.py

Initializing the Deployer class with subscription id: 11111111-1111-1111-1111-111111111111, resource group: azure-python-deployment-sample
and public key located at: /Users/you/.ssh/id_rsa.pub...

Beginning the deployment...

Done deploying!!

You can connect via: `ssh azureSample@damp-dew-79.local.cloudapp.azurestack.external`
```

You should be able to run `ssh azureSample@{your dns name}` to connect to your new VM.