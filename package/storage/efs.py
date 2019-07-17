"""This script nuke all efs resources"""

import logging
import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_efs(older_than_seconds):
    """
         efs function for destroy all efs share
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    efs = boto3.client('efs')

    # Test if efs services is present in current aws region
    try:
        efs.describe_file_systems()
    except EndpointConnectionError:
        print('EFS resource is not available in this aws region')
        return

    # List all efs file systems
    efs_filesystem_list = efs_list_file_systems(time_delete)

    # Nuke all efs file systems
    for efs in efs_filesystem_list:

        # Delete efs file system
        try:
            efs.delete_file_system(FileSystemId=efs)
            print("Nuke EFS share {0}".format(efs))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def efs_list_file_systems(time_delete):
    """
       Aws efs list file system, list name of
       all efs file systems and return it in list.
    """

    # define connection
    efs = boto3.client('efs')

    # Define the connection
    paginator = efs.get_paginator('describe_file_systems')
    page_iterator = paginator.paginate()

    # Initialize efs file system list
    efs_filesystem_list = []

    # Retrieve all efs file system Id
    for page in page_iterator:
        for filesystem in page['FileSystems']:
            if efs['CreationTime'].timestamp() < time_delete:

                efs_filesystem = filesystem['FileSystemId']
                efs_filesystem_list.insert(0, efs_filesystem)

    return efs_filesystem_list
