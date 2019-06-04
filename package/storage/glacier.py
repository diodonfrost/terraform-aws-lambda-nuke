
"""This script nuke all glacier resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError


def nuke_all_glacier(older_than_seconds, logger):
    """
         glacier function for destroy all kubernetes vaults
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    glacier = boto3.client('glacier')

    try:
        glacier.list_vaults()
    except EndpointConnectionError:
        print('glacier resource is not available in this aws region')
        return

    # List all glacier vault
    glacier_vault_list = glacier_list_vaults(time_delete)

    # Nuke all glacier vault
    for vault in glacier_vault_list:

        # Delete glacier vault
        glacier.delete_vault(vaultName=vault)
        logger.info("Nuke glacier vault %s", vault)


def glacier_list_vaults(time_delete):
    """
       Aws glacier container service, list name of
       all glacier vault and return it in list.
    """

    # Define the connection
    glacier = boto3.client('glacier')
    paginator = glacier.get_paginator('list_vaults')
    page_iterator = paginator.paginate()

    # Initialize glacier vault list
    glacier_vault_list = []

    # Retrieve all glacier vault
    for page in page_iterator:
        for vault in page['VaultList']:
            if vault['CreationDate'].timestamp() < time_delete:

                glacier_vault = vault['VaultName']
                glacier_vault_list.insert(0, glacier_vault)

    return glacier_vault_list
