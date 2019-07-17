"""This script nuke all redshift resources"""

import logging
import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_redshift(older_than_seconds):
    """
         redshift function for destroy all redshift resources
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    redshift = boto3.client('redshift')

    # Test if redshift services is present in current aws region
    try:
        redshift.describe_clusters()
    except EndpointConnectionError:
        print('redshift resource is not available in this aws region')
        return

    # Nuke all aws redshift resources
    redshift_nuke_clusters(time_delete)
    redshift_nuke_snapshots(time_delete)
    redshift_nuke_subnets()
    redshift_nuke_param_groups()


def redshift_nuke_clusters(time_delete):
    """
         redshift function for destroy all redshift databases
    """
    # define connection
    redshift = boto3.client('redshift')

    # List all redshift clusters
    redshift_cluster_list = redshift_list_clusters(time_delete)

    # Nuke all redshift clusters
    for cluster in redshift_cluster_list:

        try:
            redshift.delete_cluster(
                ClusterIdentifier=cluster,
                SkipFinalClusterSnapshot=True)
            print("Nuke redshift cluster{0}".format(cluster))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClusterStateFault':
                logging.info(
                    "redshift cluster %s is not in state started", cluster)
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_snapshots(time_delete):
    """
         redshift function for destroy all redshift snapshots
    """
    # define connection
    redshift = boto3.client('redshift')

    # List all redshift snapshots
    redshift_snapshot_list = redshift_list_snapshots(time_delete)

    # Nuke all redshift snapshots
    for snapshot in redshift_snapshot_list:

        try:
            redshift.delete_cluster_snapshot(SnapshotIdentifier=snapshot)
            print("Nuke redshift snapshot {0}".format(snapshot))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClusterSnapshotStateFault':
                logging.info(
                    "redshift snap %s is not in state available", snapshot)
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_subnets():
    """
         redshift function for destroy all redshift subnets
    """
    # define connection
    redshift = boto3.client('redshift')

    # List all redshift subnets
    redshift_subnet_list = redshift_list_subnet()

    # Nuke all redshift subnets
    for subnet in redshift_subnet_list:

        try:
            redshift.delete_cluster_subnet_group(ClusterSubnetGroupName=subnet)
            print("Nuke redshift subnet {0}".format(subnet))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClusterSubnetGroupStateFault':
                logging.info(
                    "redshift subnet %s is not in state available", subnet)
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_param_groups():
    """
         redshift function for destroy all redshift param groups
    """
    # define connection
    redshift = boto3.client('redshift')

    # List all redshift cluster parameters
    redshift_cluster_param_list = redshift_list_cluster_params()

    # Nuke all redshift parameters
    for param in redshift_cluster_param_list:

        try:
            redshift.delete_cluster_parameter_group(ParameterGroupName=param)
            print("Nuke redshift param {0}".format(param))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClusterParameterGroupStateFault':
                logging.info(
                    "redshift param %s is not in state available", param)
            elif error_code == 'InvalidParameterValue':
                logging.info(
                    "default %s parameter group cannot be deleted", param)
            else:
                logging.error("Unexpected error: %s", e)


def redshift_list_clusters(time_delete):
    """
       Aws redshift list clusters, list name of
       all redshift clusters and return it in list.
    """

    # define connection
    redshift = boto3.client('redshift')

    # Define the connection
    paginator = redshift.get_paginator('describe_clusters')
    page_iterator = paginator.paginate()

    # Initialize redshift cluster list
    redshift_cluster_list = []

    # Retrieve all redshift cluster name
    for page in page_iterator:
        for cluster in page['Clusters']:
            if cluster['ClusterCreateTime'].timestamp() < time_delete:

                redshift_cluster = cluster['ClusterIdentifier']
                redshift_cluster_list.insert(0, redshift_cluster)

    return redshift_cluster_list


def redshift_list_snapshots(time_delete):
    """
       Aws redshift list snapshots, list name of
       all redshift snapshots and return it in list.
    """

    # define connection
    redshift = boto3.client('redshift')

    # Define the connection
    paginator = redshift.get_paginator('describe_cluster_snapshots')
    page_iterator = paginator.paginate()

    # Initialize redshift snapshot list
    redshift_snapshot_list = []

    # Retrieve all redshift snapshot identifier
    for page in page_iterator:
        for snapshot in page['Snapshots']:
            if snapshot['SnapshotCreateTime'].timestamp() < time_delete:

                redshift_snapshot = snapshot['SnapshotIdentifier']
                redshift_snapshot_list.insert(0, redshift_snapshot)

    return redshift_snapshot_list


def redshift_list_subnet():
    """
       Aws redshift list subnets, list name of
       all redshift subnets and return it in list.
    """

    # define connection
    redshift = boto3.client('redshift')

    # Define the connection
    paginator = redshift.get_paginator('describe_cluster_subnet_groups')
    page_iterator = paginator.paginate()

    # Initialize redshift subnet list
    redshift_subnet_list = []

    # Retrieve all redshift subnet name
    for page in page_iterator:
        for subnet in page['ClusterSubnetGroups']:

            redshift_subnet = subnet['ClusterSubnetGroupName']
            redshift_subnet_list.insert(0, redshift_subnet)

    return redshift_subnet_list


def redshift_list_cluster_params():
    """
       Aws redshift list cluster parameters, list name of
       all redshift cluster parameters and return it in list.
    """

    # define connection
    redshift = boto3.client('redshift')

    # Define the connection
    paginator = redshift.get_paginator('describe_cluster_parameter_groups')
    page_iterator = paginator.paginate()

    # Initialize redshift cluster parameters list
    redshift_cluster_param_list = []

    # Retrieve all redshift cluster parameter names
    for page in page_iterator:
        for param in page['ParameterGroups']:

            redshift_cluster_param = param['ParameterGroupName']
            redshift_cluster_param_list.insert(0, redshift_cluster_param)

    return redshift_cluster_param_list
