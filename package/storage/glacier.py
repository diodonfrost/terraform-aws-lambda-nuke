# -*- coding: utf-8 -*-

"""Module deleting all aws Glacier resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_glacier(older_than_seconds):
    """Glacier deleting function.

    Deleting all Glacier with a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    glacier = boto3.client("glacier")

    try:
        glacier.list_vaults()
    except EndpointConnectionError:
        print("glacier resource is not available in this aws region")
        return

    # List all glacier vault
    glacier_vault_list = glacier_list_vaults(time_delete)

    # Nuke all glacier vault
    for vault in glacier_vault_list:

        # Delete glacier vault
        try:
            glacier.delete_vault(vaultName=vault)
            print("Nuke glacier vault {0}".format(vault))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def glacier_list_vaults(time_delete):
    """Glacier vault list function.

    List the names of all Glacier vaults with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Glacier vaults
    :returns:
        List of Glacier vaults names
    :rtype:
        [str]
    """
    # Define the connection
    glacier = boto3.client("glacier")
    paginator = glacier.get_paginator("list_vaults")
    page_iterator = paginator.paginate()

    # Initialize glacier vault list
    glacier_vault_list = []

    # Retrieve all glacier vault
    for page in page_iterator:
        for vault in page["VaultList"]:
            if vault["CreationDate"].timestamp() < time_delete:

                glacier_vault = vault["VaultName"]
                glacier_vault_list.insert(0, glacier_vault)

    return glacier_vault_list
