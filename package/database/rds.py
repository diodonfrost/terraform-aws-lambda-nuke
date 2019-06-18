"""This script nuke all rds resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


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
        try:
            rds.delete_db_instance(DBInstanceIdentifier=instance)
            print("Stop rds instance {0}".format(instance))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidDBInstanceState':
                logger.info("rds instance %s is not started", instance)
            else:
                logger.error("Unexpected error: %s" % e)

    # List all rds clusters
    rds_cluster_list = rds_list_clusters(time_delete)

    # Nuke all rds clusters
    for cluster in rds_cluster_list:

        # Delete Aurora cluster
        try:
            rds.delete_db_cluster(DBClusterIdentifier=cluster)
            print("Nuke rds cluster {0}".format(cluster))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidDBClusterStateFault':
                logger.info("rds cluster %s is not started", cluster)
            else:
                logger.error("Unexpected error: %s" % e)


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


def rds_list_clusters(time_delete):
    """
       Aws rds list db clusters, list name of
       all rds db clusters and return it in list.
    """

    # define connection
    rds = boto3.client('rds')

    # Define the connection
    paginator = rds.get_paginator('describe_db_clusters')
    page_iterator = paginator.paginate()

    # Initialize rds cluster list
    rds_cluster_list = []

    # Retrieve all rds cluster identifier
    for page in page_iterator:
        for cluster in page['DBClusters']:
            if cluster['ClusterCreateTime'].timestamp() < time_delete:

                rds_cluster = cluster['DBClusterIdentifier']
                rds_cluster_list.insert(0, rds_cluster)

    return rds_cluster_list
