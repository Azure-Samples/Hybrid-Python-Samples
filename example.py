"""Create and manage resources and resource groups.
Manage Storage Account - create a new storage account, read its properties,
list all storage accounts in a given subscription or resource group,
read and regenerate the storage account keys, and delete a storage account.

This script expects that the following environment vars are set:

AZURE_TENANT_ID: your Azure Active Directory tenant id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application Secret
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
AZURE_RESOURCE_LOCATION: your resource location
ARM_ENDPOINT: your cloud's resource manager endpoint
"""
import os
import random
import logging
from haikunator import Haikunator
from azure.profiles import KnownProfiles
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountUpdateParameters,
    Sku,
    SkuName,
    Kind
)

from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint

# Azure Datacenter
LOCATION = os.environ['AZURE_RESOURCE_LOCATION']

# Resource Group
post_fix = random.randint(100, 500)
GROUP_NAME = 'azure-sample-group-resources-{}'.format(post_fix)

# Storage Account
STORAGE_ACCOUNT_NAME = Haikunator().haikunate(delimiter='')


def get_credentials():
    mystack_cloud = get_cloud_from_metadata_endpoint(
        os.environ['ARM_ENDPOINT'])
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID'],
        cloud_environment=mystack_cloud
    )
    return credentials, subscription_id, mystack_cloud


def run_example():
    """Storage management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    # By Default, use AzureStack supported profile
    KnownProfiles.default.use(KnownProfiles.v2018_03_01_hybrid)
    logging.basicConfig(level=logging.ERROR)

    credentials, subscription_id, mystack_cloud = get_credentials()

    resource_client = ResourceManagementClient(credentials, subscription_id,
                                               base_url=mystack_cloud.endpoints.resource_manager)
    storage_client = StorageManagementClient(credentials, subscription_id,
                                             base_url=mystack_cloud.endpoints.resource_manager)

    # You MIGHT need to add Storage as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register('Microsoft.Storage')

    # Create Resource group
    print('Create Resource Group')
    resource_group_params = {'location': LOCATION}
    print_item(resource_client.resource_groups.create_or_update(
        GROUP_NAME, resource_group_params))

    # Check availability
    print('Check name availability')
    bad_account_name = 'invalid-or-used-name'
    availability = storage_client.storage_accounts.check_name_availability(
        bad_account_name)
    print('The account {} is available: {}'.format(
        bad_account_name, availability.name_available))
    print('Reason: {}'.format(availability.reason))
    print('Detailed message: {}'.format(availability.message))
    print('\n\n')

    # Create a storage account
    print('Create a storage account')
    storage_async_operation = storage_client.storage_accounts.create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            'sku': {'name': 'standard_lrs'},
            'kind': 'storage',
            'location': LOCATION
        }
    )
    storage_account = storage_async_operation.result()
    print_item(storage_account)
    print('\n\n')

    # Get storage account properties
    print('Get storage account properties')
    storage_account = storage_client.storage_accounts.get_properties(
        GROUP_NAME, STORAGE_ACCOUNT_NAME)
    print_item(storage_account)
    print("\n\n")

    # List Storage accounts
    print('List storage accounts')
    for item in storage_client.storage_accounts.list():
        print_item(item)
    print("\n\n")

    # List Storage accounts by resource group
    print('List storage accounts by resource group')
    for item in storage_client.storage_accounts.list_by_resource_group(GROUP_NAME):
        print_item(item)
    print("\n\n")

    # Get the account keys
    print('Get the account keys')
    storage_keys = storage_client.storage_accounts.list_keys(
        GROUP_NAME, STORAGE_ACCOUNT_NAME)
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    print('\tKey 1: {}'.format(storage_keys['key1']))
    print('\tKey 2: {}'.format(storage_keys['key2']))
    print("\n\n")

    # Regenerate the account key 1
    print('Regenerate the account key 1')
    storage_keys = storage_client.storage_accounts.regenerate_key(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        'key1')
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    print('\tNew key 1: {}'.format(storage_keys['key1']))
    print("\n\n")

    print_item(storage_account)
    print("\n\n")

    # Delete the storage account
    print('Delete the storage account')
    storage_client.storage_accounts.delete(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    print("\n\n")

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("Deleted: {}".format(GROUP_NAME))
    print("\n\n")

    # List usage
    print('List usage')
    for usage in storage_client.usage.list():
        print('\t{}'.format(usage.name.value))


def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


if __name__ == "__main__":
    run_example()
