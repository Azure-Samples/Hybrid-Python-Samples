---
page_type: sample
languages:
- python
products:
- azure
description: "This sample explains how to use Azure Resource Manager templates to deploy your Resources to Azure Stack."
urlFragment: Hybrid-Python-TemplateDeployment
---

# Hybrid-Python-TemplateDeployment

This sample explains how to use Azure Resource Manager templates to deploy your Resources to Azure Stack using the Azure SDK for Python.

In this sample, we are going to deploy a resource template which contains an Ubuntu 16.04 LTS virtual machine using
ssh public key authentication, storage account, and virtual network with public IP address. The virtual network
contains a single subnet with a single network security group rule which allows traffic on port 22 for ssh with a single
network interface belonging to the subnet. The virtual machine is a `Standard_A1` size.

## Run this sample

```
python example.py
```