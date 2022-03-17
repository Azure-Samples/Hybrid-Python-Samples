"""Create and manage resources and resource groups.
Manage resources and resource groups - create, update and delete a resource group,
deploy a solution into a resource group, export an ARM template. Create, read, update
and delete a resource.
This script expects that the following environment vars are present in azureSecretSpConfig.json:
tenantId: your Azure Active Directory tenant id or domain
clientId: your Azure Active Directory Application Client ID
clientSecret: your Azure Active Directory Application Secret
subscriptionId: your Azure Subscription Id
location: your resource location
resourceManagerEndpointUrl: your cloud's resource manager endpoint
"""
import os, random, json, logging
from datetime import datetime
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential

from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint
from azure.profiles import KnownProfiles

# Resource Group
postfix = random.randint(100, 500)
GROUP_NAME = 'azure-sample-group-resources-{}'.format(postfix)

def run_example(config):
    """Resource Group management example."""
    try:
        logging.basicConfig(level=logging.ERROR)

        mystack_cloud = get_cloud_from_metadata_endpoint(
            config['resourceManagerEndpointUrl'])

        subscription_id = config['subscriptionId']
        # Azure stack location
        location = config['location']

        credentials = ClientSecretCredential(
            client_id = config['clientId'],
            client_secret = config['clientSecret'],
            tenant_id = config['tenantId'],
            authority = mystack_cloud.endpoints.active_directory
        )

        KnownProfiles.default.use(KnownProfiles.v2020_09_01_hybrid)
        scope = "openid profile offline_access" + " " + mystack_cloud.endpoints.active_directory_resource_id + "/.default"
        
        client = ResourceManagementClient(
            credentials , subscription_id,
            base_url=mystack_cloud.endpoints.resource_manager,
            credential_scopes=[scope])

        #
        # Managing resource groups
        #
        resource_group_params = {'location': location}

        # List Resource Groups
        print('List Resource Groups')
        for item in client.resource_groups.list():
            print_item(item)

        # Create Resource group
        print('Create Resource Group')
        print_item(client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

        # Modify the Resource group
        print('Modify Resource Group')
        resource_group_params.update(tags={'hello': 'world'})
        print_item(client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

        # Create a Key Vault in the Resource Group
        print('Create a Key Vault via a Generic Resource Put')
        key_vault_params = {
            'location': location,
            'properties': {
                'sku': {'family': 'A', 'name': 'standard'},
                'tenantId': config['tenantId'],
                'accessPolicies': [],
                'enabledForDeployment': True,
                'enabledForTemplateDeployment': True,
                'enabledForDiskEncryption': True
            }
        }

        client.resources.begin_create_or_update(
            resource_group_name=GROUP_NAME,
            resource_provider_namespace="Microsoft.KeyVault",
            parent_resource_path="",
            resource_type="vaults",
            resource_name='azureSampleVault' + datetime.utcnow().strftime("-%H%M%S"),
            parameters = key_vault_params,
            api_version="2016-10-01"
        ).result()

        # List Resources within the group
        print('List all of the resources within the group')
        for item in client.resources.list_by_resource_group(GROUP_NAME):
            print_item(item)

        # Export the Resource group template
        print('Export Resource Group Template')
        BODY = {
            'resources': ['*']
        }
        rgTemplate = client.resource_groups.begin_export_template(GROUP_NAME, BODY).result()
        print(rgTemplate.template)
        print('\n\n')
    finally:
        # Delete Resource group and everything in it
        print('Delete Resource Group')
        client.resource_groups.begin_delete(GROUP_NAME).result()
        print("\nDeleted: {}".format(GROUP_NAME))


def print_item(group):
    """Print ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
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