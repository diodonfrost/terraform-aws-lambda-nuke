"""This script nuke all rds resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError


def nuke_all_rds(older_than_seconds, logger):
    """
         rds function for destroy all rds database
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    rds = boto3.client('rds')

    # Test if rds services is present in current aws region
    try:
        rds.describe_db_instances()
    except EndpointConnectionError:
        print('rds resource is not available in this aws region')
        return

    # List all rds instances
    rds_instance_list = rds_list_instances(time_delete)

    # Nuke all rds instances
    for instance in rds_instance_list:

        # Delete rds instance
        rds.delete_db_instance(
            DBInstanceIdentifier=instance,
            SkipFinalSnapshot=True)
        logger.info("Nuke rds share %s", instance)


def rds_list_instances(time_delete):
    """
       Aws rds list db instances, list name of
       all rds db instances and return it in list.
    """

    # define connection
    rds = boto3.client('rds')

    # Define the connection
    paginator = rds.get_paginator('describe_db_instances')
    page_iterator = paginator.paginate()

    # Initialize rds instance list
    rds_instance_list = []

    # Retrieve all rds instance identifier
    for page in page_iterator:
        for instance in page['DBInstances']:
            if instance['InstanceCreateTime'].timestamp() < time_delete:

                rds_instance = instance['DBInstanceIdentifier']
                rds_instance_list.insert(0, rds_instance)

    return rds_instance_list
