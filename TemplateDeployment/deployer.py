"""A deployer class to deploy a template on Azure"""
import os.path
import json
from haikunator import Haikunator
from azure.profiles import KnownProfiles
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint
from azure.mgmt.resource.resources.models import Deployment
from azure.mgmt.resource.resources.models import DeploymentProperties

class Deployer(object):
    """ Initialize the deployer class with config, resource group and public key.

    :raises IOError: If the public key path cannot be read (access or not exists)
    :raises KeyError: If clientId, clientSecret or tenantId variables are not defined in azureSecretSpConfig.json
    """
    name_generator = Haikunator()

    def __init__(self, config, resource_group, pub_ssh_key_path='~/id_rsa.pub'):
        mystack_cloud = get_cloud_from_metadata_endpoint(config['resourceManagerEndpointUrl'])
        credentials = ClientSecretCredential(
            client_id = config['clientId'],
            client_secret = config['clientSecret'],
            tenant_id = config['tenantId'],
            authority = mystack_cloud.endpoints.active_directory
            )

        self.location = config['location']   
        self.subscription_id = config['subscriptionId']
        self.resource_group = resource_group
        self.dns_label_prefix = self.name_generator.haikunate()

        pub_ssh_key_path = os.path.expanduser(pub_ssh_key_path)
        # Will raise if file not exists or not enough permission
        with open(pub_ssh_key_path, 'r') as pub_ssh_file_fd:
            self.pub_ssh_key = pub_ssh_file_fd.read()

        self.credentials = credentials
        scope = "openid profile offline_access" + " " + mystack_cloud.endpoints.active_directory_resource_id + "/.default"
        self.client = ResourceManagementClient(
            credentials , self.subscription_id,
            base_url = mystack_cloud.endpoints.resource_manager,
            profile=KnownProfiles.v2020_09_01_hybrid,
            credential_scopes = [scope])

    def deploy(self):
        """Deploy the template to a resource group."""

        resource_group_params = {'location': self.location}
        self.client.resource_groups.create_or_update(self.resource_group, resource_group_params)

        template_path = os.path.join(os.path.dirname(__file__), 'template.json')
        with open(template_path, 'r') as template_file_fd:
            template = json.load(template_file_fd)

        parameters = {
            'sshKeyData': self.pub_ssh_key,
            'vmName': 'azure-deployment-sample-vm',
            'dnsLabelPrefix': self.dns_label_prefix
        }

        parameters = {k: {'value': v} for k, v in parameters.items()}

        deployment_properties = DeploymentProperties(mode=DeploymentMode.incremental, template=template, parameters=parameters)

        deployment_async_operation = self.client.deployments.begin_create_or_update(
            self.resource_group,
            'azure-sample',
            Deployment(properties=deployment_properties)
        )
        deployment_async_operation.wait()


    def destroy(self):
        """Destroy the given resource group"""
        self.client.resource_groups.begin_delete(self.resource_group).result()
        print("\nDeleted: {}".format(self.resource_group))