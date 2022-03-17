import os.path, json
from deployer import Deployer

def run_example(config):
    try:
        my_subscription_id = config['subscriptionId']   # your Azure Subscription Id
        my_resource_group = 'azure-python-deployment-sample'            # the resource group for deployment
        my_pub_ssh_key_path = os.path.expanduser('~/.ssh/id_rsa.pub')   # the path to your rsa public key file

        msg = "\nInitializing the Deployer class with subscription id: {}, resource group: {}" \
            "\nand public key located at: {}...\n\n"
        msg = msg.format(my_subscription_id, my_resource_group, my_pub_ssh_key_path)
        print(msg)

        # Initialize the deployer class
        deployer = Deployer(config, my_resource_group, my_pub_ssh_key_path)

        print("Beginning the deployment... \n\n")
        # Deploy the template
        my_deployment = deployer.deploy()

        print("Done deploying!!")

    finally:
        print("Cleaning up the deployment... \n\n")
        #Destroy the resource group which contains the deployment
        deployer.destroy()
        print("Clean up the deployment sucessfully. \n")

if __name__ == "__main__":
    with open('../azureSecretSpConfig.json', 'r') as f:
        config = json.load(f)
    run_example(config)