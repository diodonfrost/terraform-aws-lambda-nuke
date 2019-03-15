"""This script nuke all neptune resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_neptune(older_than_seconds, logger):
    """
         neptune function for destroy all neptune database
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    neptune = boto3.client('neptune')

    # Test if neptune services is present in current aws region
    try:
        neptune.describe_db_clusters()
    except EndpointConnectionError:
        print('neptune resource is not available in this aws region')
        return

    # List all neptune clusters
    neptune_cluster_list = neptune_list_clusters(time_delete)

    # Nuke all neptune clusters
    for cluster in neptune_cluster_list:

        try:
            neptune.delete_db_cluster(
                DBClusterIdentifier=cluster,
                SkipFinalSnapshot=True)
            logger.info("Nuke neptune cluster %s", cluster)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidDBClusterStateFault':
                logger.info("neptune cluster %s is not in state started", cluster)
            else:
                print("Unexpected error: %s" % e)

    # List all neptune snapshots
    neptune_snapshot_list = neptune_list_snapshots(time_delete)

    # Nuke all neptune snapshots
    for snapshot in neptune_snapshot_list:

        neptune.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier=snapshot)
        logger.info("Nuke neptune snapshot %s", snapshot)

    # List all neptune subnets
    neptune_subnet_list = neptune_list_subnet()

    # Nuke all neptune subnets
    for subnet in neptune_subnet_list:

        try:
            neptune.delete_db_subnet_group(DBSubnetGroupName=subnet)
            logger.info("Nuke neptune subnet %s", subnet)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidDBSubnetGroupStateFault':
                logger.info("%s is reserved and cannot be modified.", subnet)
            else:
                print("Unexpected error: %s" % e)

    # List all neptune cluster parameters
    neptune_cluster_param_list = neptune_list_cluster_params()

    # Nuke all neptune parameters
    for param in neptune_cluster_param_list:

        try:
            neptune.delete_db_cluster_parameter_group(DBClusterParameterGroupName=param)
            logger.info("Nuke neptune param %s", param)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidDBParameterGroupState':
                logger.info("%s is reserved and cannot be modified.", param)
            else:
                print("Unexpected error: %s" % e)

    # List all neptune parameters
    neptune_param_list = neptune_list_params()

    # Nuke all neptune parameters
    for param in neptune_param_list:

        try:
            neptune.delete_db_parameter_group(DBParameterGroupName=param)
            logger.info("Nuke neptune param %s", param)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidDBParameterGroupState':
                logger.info("%s is reserved and cannot be modified.", param)
            else:
                print("Unexpected error: %s" % e)


def neptune_list_clusters(time_delete):
    """
       Aws neptune list clusters, list name of
       all neptune clusters and return it in list.
    """

    # define connection
    neptune = boto3.client('neptune')
    response = neptune.describe_db_clusters()

    # Initialize neptune cluster list
    neptune_cluster_list = []

    # Retrieve all neptune cluster name
    for cluster in response['DBClusters']:
        if cluster['ClusterCreateTime'].timestamp() < time_delete:

            neptune_cluster = cluster['DBClusterIdentifier']
            neptune_cluster_list.insert(0, neptune_cluster)

    return neptune_cluster_list


def neptune_list_snapshots(time_delete):
    """
       Aws neptune list snapshots, list name of
       all neptune snapshots and return it in list.
    """

    # define connection
    neptune = boto3.client('neptune')
    response = neptune.describe_db_cluster_snapshots()

    # Initialize neptune snapshot list
    neptune_snapshot_list = []

    # Retrieve all neptune snapshot identifier
    for snapshot in response['DBClusterSnapshots']:
        if snapshot['SnapshotCreateTime'].timestamp() < time_delete:

            neptune_snapshot = snapshot['DBClusterSnapshotIdentifier']
            neptune_snapshot_list.insert(0, neptune_snapshot)

    return neptune_snapshot_list


def neptune_list_subnet():
    """
       Aws neptune list subnets, list name of
       all neptune subnets and return it in list.
    """

    # define connection
    neptune = boto3.client('neptune')
    response = neptune.describe_db_subnet_groups()

    # Initialize neptune subnet list
    neptune_subnet_list = []

    # Retrieve all neptune subnet name
    for subnet in response['DBSubnetGroups']:

        neptune_subnet = subnet['DBSubnetGroupName']
        neptune_subnet_list.insert(0, neptune_subnet)

    return neptune_subnet_list


def neptune_list_cluster_params():
    """
       Aws neptune list cluster parameters, list name of
       all neptune cluster parameters and return it in list.
    """

    # define connection
    neptune = boto3.client('neptune')
    response = neptune.describe_db_cluster_parameter_groups()

    # Initialize neptune cluster parameters list
    neptune_cluster_param_list = []

    # Retrieve all neptune cluster parameter names
    for param in response['DBClusterParameterGroups']:

        neptune_cluster_param = param['DBClusterParameterGroupName']
        neptune_cluster_param_list.insert(0, neptune_cluster_param)

    return neptune_cluster_param_list


def neptune_list_params():
    """
       Aws neptune list parameters, list name of
       all neptune parameters and return it in list.
    """

    # define connection
    neptune = boto3.client('neptune')
    response = neptune.describe_db_parameter_groups()

    # Initialize neptune parameters list
    neptune_param_list = []

    # Retrieve all neptune parameters name
    for param in response['DBParameterGroups']:

        neptune_param = param['DBParameterGroupName']
        neptune_param_list.insert(0, neptune_param)

    return neptune_param_list
