
"""This script nuke all efs resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError

EFS = boto3.client('efs')

def nuke_all_efs(older_than_seconds, logger):
    """
         efs function for destroy all efs share
    """

    #### Nuke all efs share ####
    try:
        response = EFS.describe_file_systems()
    except EndpointConnectionError:
        print('EFS service is not available in this aws region')
        return

    time_delete = time.time() - older_than_seconds

    for efs in response['FileSystems']:

        if efs['CreationTime'].timestamp() < time_delete:

            # Nuke efs share
            EFS.delete_file_system(FileSystemId=efs['FileSystemId'])
            logger.info("Nuke EFS share %s", efs['FileSystemId'])
