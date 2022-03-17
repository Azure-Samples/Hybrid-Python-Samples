"""Create a Keyvault in a resource group.
Set a secret inside the keyvault.
Retrieve the secret from the keyvault.
List all the keyvaults in the resource group.
Delete keyvault and resource group.

This script expects that the following vars are set in azureSecretSpConfig.json:

tenantId: your Azure Active Directory tenant id or domain
objectId: The object ID of the User or Application for access policies.
clientId: your Azure Active Directory Application Client ID
clientSecret: your Azure Active Directory Application Secret
subscriptionId: your Azure Subscription Id
AZURE_RESOURCE_LOCATION: your resource location
resourceManagerEndpointUrl: your cloud's resource manager endpoint
"""

import json, logging, random
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.profiles import KnownProfiles
from haikunator import Haikunator
from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint

haikunator = Haikunator()

# Keyvault 
KV_NAME = haikunator.haikunate()

def get_credentials(config):
    mystack_cloud = get_cloud_from_metadata_endpoint(
        config['resourceManagerEndpointUrl'])
    subscription_id = config['subscriptionId']

    credentials = ClientSecretCredential(
        client_id = config['clientId'],
        client_secret = config['clientSecret'],
        tenant_id = config['tenantId'],
        authority = mystack_cloud.endpoints.active_directory
    )

    return credentials, subscription_id, mystack_cloud

def run_example(config):
    """Keyvault management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    # By Default, use AzureStack supported profile
    
    try:
        KnownProfiles.default.use(KnownProfiles.v2020_09_01_hybrid)

        credentials, subscription_id, mystack_cloud = get_credentials(config)
        scope = "openid profile offline_access" + " " + mystack_cloud.endpoints.active_directory_resource_id + "/.default"
        
        resource_client = ResourceManagementClient(
            credentials,
            subscription_id,
            base_url=mystack_cloud.endpoints.resource_manager,
            profile=KnownProfiles.v2020_09_01_hybrid,
            credential_scopes=[scope])

        kv_client = KeyVaultManagementClient(credentials,
                    subscription_id,
                    base_url=mystack_cloud.endpoints.resource_manager,
                    profile=KnownProfiles.v2020_09_01_hybrid,
                    credential_scopes=[scope])

        # Azure Data center
        LOCATION = config['location']

        # Resource Group
        post_fix = random.randint(100, 500)
        GROUP_NAME = 'azure-sample-group-resources-{}'.format(post_fix)

        # Create Resource group
        print('Create Resource Group')
        resource_group_params = {'location': LOCATION}
        print_item(resource_client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

        # Create a vault
        print('\nCreate a vault')
        vault = kv_client.vaults.begin_create_or_update(
            GROUP_NAME,
            KV_NAME,
            {
                'location': LOCATION,
                'properties': {
                    'sku': {
                        'name': 'standard',
                        'family': 'A'
                    },
                    'tenant_id': config['tenantId'],
                    'access_policies': [{
                        'tenant_id': config['tenantId'],
                        'object_id': config['objectId'],
                        'permissions': {
                            'keys': ['all'],
                            'secrets': ['all']
                        }
                    }]
                }
            }
        )
        created_vault = vault.result()
        print_item(created_vault)

        kv_data_client = SecretClient(vault_url=created_vault.properties.vault_uri, credential=credentials)

        #set and get a secret from the vault to validate the client is authenticated
        print('creating secret...')
        secret_bundle = kv_data_client.set_secret('auth-sample-secret', 'client is authenticated to the vault')
        print(secret_bundle)

        print('getting secret...')
        secret_retrived = kv_data_client.get_secret(secret_bundle.name)
            #vault.properties.vault_uri, 'auth-sample-secret', secret_version=KeyVaultId.version_none)
        print(secret_retrived)

        # List the Key vaults
        print('\nList KeyVaults')
        for vault in kv_client.vaults.list():
            print_item(vault)

        # Delete keyvault
        print('\nDelete Keyvault')
        kv_client.vaults.delete(GROUP_NAME, KV_NAME)
    
    finally:
        # Delete Resource group and everything in it
        print('\nDelete Resource Group')
        delete_async_operation = resource_client.resource_groups.begin_delete(GROUP_NAME)
        delete_async_operation.result()
        print("\nDeleted: {}".format(GROUP_NAME))


def print_item(group):
    """Print an instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))


if __name__ == "__main__":
    with open('../azureSecretSpConfig.json', 'r') as f:
        config = json.load(f)
    run_example(config)