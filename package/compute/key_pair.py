
"""This script nuke all key pairs"""

import boto3

EC2 = boto3.client('ec2')

def nuke_all_key_pair(logger):
    """
         ec2 function for nuke all key pairs
    """

    #### Nuke all volumes ####
    response = EC2.describe_key_pairs()

    for keypair in response['KeyPairs']:

        # Nuke all ec2 key pair
        EC2.delete_key_pair(KeyName=keypair['KeyName'])
        logger.info("Nuke Key Pair %s", keypair['KeyName'])
