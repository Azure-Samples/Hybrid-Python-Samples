"""Create and manage resources and resource groups.
Manage Storage Account - create a new storage account, read its properties,
list all storage accounts in a given subscription or resource group,
read and regenerate the storage account keys, and delete a storage account.
This script expects that the following vars are set in azureSecretSpConfig.json:
tenantId: your Azure Active Directory tenant id or domain
clientId: your Azure Active Directory Application Client ID
clientSecret: your Azure Active Directory Application Secret
subscriptionId: your Azure Subscription Id
location: your resource location
resourceManagerEndpointUrl: your cloud's resource manager endpoint
"""
import json, random, logging
from haikunator import Haikunator
from azure.profiles import KnownProfiles
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.identity import ClientSecretCredential

from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint

# Resource Group
post_fix = random.randint(100, 500)
GROUP_NAME = 'azure-sample-group-resources-{}'.format(post_fix)

# Storage Account
STORAGE_ACCOUNT_NAME = Haikunator().haikunate(delimiter='')

def get_credentials(config):
    mystack_cloud = get_cloud_from_metadata_endpoint(config['resourceManagerEndpointUrl'])
    subscription_id = config['subscriptionId']
    credentials = ClientSecretCredential(
        client_id = config['clientId'],
        client_secret = config['clientSecret'],
        tenant_id = config['tenantId'],
        authority = mystack_cloud.endpoints.active_directory)

    return credentials, subscription_id, mystack_cloud

def run_example(config):
    """Storage management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    # By Default, use AzureStack supported profile
    try:
        logging.basicConfig(level=logging.ERROR)
        # Azure Datacenter
        LOCATION = config['location']
        credentials, subscription_id, mystack_cloud = get_credentials(config)
        scope = "openid profile offline_access" + " " + mystack_cloud.endpoints.active_directory_resource_id + "/.default"
        
        resource_client = ResourceManagementClient(
            credentials , subscription_id,
            base_url=mystack_cloud.endpoints.resource_manager,
            profile=KnownProfiles.v2020_09_01_hybrid,
            credential_scopes=[scope])

        storage_client = StorageManagementClient(
            credentials,
            subscription_id, 
            base_url=mystack_cloud.endpoints.resource_manager,
            profile=KnownProfiles.v2020_09_01_hybrid,
            credential_scopes=[scope])

        # You MIGHT need to add Storage as a valid provider for these credentials
        # If so, this operation has to be done only once for each credentials
        resource_client.providers.register('Microsoft.Storage')

        # Create Resource group
        print('Create Resource Group')
        resource_group_params = {'location': LOCATION}
        print_item(resource_client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

        # Check availability
        print('Check name availability')
        bad_account_name = 'invalid-or-used-name'
        availability = storage_client.storage_accounts.check_name_availability({ "name": bad_account_name })
        print('The account {} is available: {}'.format(bad_account_name, availability.name_available))
        print('Reason: {}'.format(availability.reason))
        print('Detailed message: {}'.format(availability.message))
        print('\n\n')

        # Create a storage account
        print('Create a storage account')
        storage_async_operation = storage_client.storage_accounts.begin_create(
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
        storage_keys = storage_client.storage_accounts.list_keys(GROUP_NAME, STORAGE_ACCOUNT_NAME)
        storage_keys = {v.key_name: v.value for v in storage_keys.keys}
        print('\tKey 1: {}'.format('key1'))
        print('\tKey 2: {}'.format('key2'))
        print('Retrieved the storage account keys successfully.')
        print("\n\n")

        # Regenerate the account key 1
        print('Regenerate the account key 1')
        storage_keys = storage_client.storage_accounts.regenerate_key(
            GROUP_NAME,
            STORAGE_ACCOUNT_NAME,
            { "key_name" :'key1'} )
        storage_keys = {v.key_name: v.value for v in storage_keys.keys}
        print('Regenerated the storage account key successfully.')
        print("\n\n")

        print_item(storage_account)
        print("\n\n")

        # Delete the storage account
        print('Delete the storage account')
        storage_client.storage_accounts.delete(GROUP_NAME, STORAGE_ACCOUNT_NAME)
        print("\n\n")
    finally:
        # Delete Resource group and everything in it
        print('Delete Resource Group')
        delete_async_operation = resource_client.resource_groups.begin_delete(GROUP_NAME)
        delete_async_operation.result()
        print("Deleted: {}".format(GROUP_NAME))
        print("\n\n")


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
    with open('../azureSecretSpConfig.json', 'r') as f:
        config = json.load(f)
    run_example(config)