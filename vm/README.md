---
page_type: sample
languages:
- python
products:
- azure
description: "These samples demonstrate how to perform common management tasks with Microsoft AzureStack Virtual Machines
using the Azure SDK for Python"
urlFragment: Hybrid-Python-Sample-VM
---

# Hybrid-Compute-Python-Manage-VM

These samples demonstrate how to perform common management tasks
with Microsoft AzureStack Virtual Machines
using the Azure SDK for Python.
The code provided shows how to do the following:

- Create virtual machines:
    - Create a Linux virtual machine
    - Create a Windows virtual machine
- Update a virtual machine:
	- Expand a drive
	- Tag a virtual machine
	- Attach data disks
- Operate a virtual machine:
    - Start a virtual machine
    - Stop a virtual machine
    - Restart a virtual machine
- List virtual machines
- Delete a virtual machine

To see the code to perform these operations,
check out the `run_example()` function in [example.py](example.py).
Each operation is clearly labeled with a comment and a print function.
The examples are not necessarily in the order shown in the above list.


## Running this sample

Note that in order to run this sample, Ubuntu 16.04-LTS and WindowsServer 2012-R2-Datacenter images must be present in AzureStack market place. These can be either [downloaded from Azure](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-download-azure-marketplace-item) or [added to Platform Image Repository](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-add-vm-image).


Run the sample.

    ```
    python example.py
    ```

## Notes

### Retrieving a VM's OS disk

You may be tempted to try to retrieve a VM's OS disk by using
`virtual_machine.storage_profile.os_disk`.
In some cases, this may do what you want,
but be aware that it gives you an `OSDisk` object.
In order to update the OS Disk's size, as `example.py` does,
you need not an `OSDisk` object but a `Disk` object.
`example.py` gets the `Disk` object with the following:

```python
os_disk_name = virtual_machine.storage_profile.os_disk.name
os_disk = compute_client.disks.get(GROUP_NAME, os_disk_name)
```
    
## More information

Here are some helpful links:

- [Azure Python Development Center](https://azure.microsoft.com/develop/python/)
- [Azure Virtual Machines documentation](https://azure.microsoft.com/services/virtual-machines/)
- [Learning Path for Virtual Machines](https://azure.microsoft.com/documentation/learning-paths/virtual-machines/)

If you don't have a Microsoft Azure subscription you can get a FREE trial account [here](http://go.microsoft.com/fwlink/?LinkId=330212).


