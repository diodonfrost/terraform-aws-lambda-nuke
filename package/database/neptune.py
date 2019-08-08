# -*- coding: utf-8 -*-

"""Module deleting all neptune resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_neptune(older_than_seconds):
    """Neptune resources deleting function.

    Deleting all neptune resources with
    a timestamp greater than older_than_seconds.
    That include:
      - clusters
      - instances
      - snapshots
      - subnets
      - param groups
      - cluster params

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    neptune = boto3.client("neptune")

    # Test if neptune services is present in current aws region
    try:
        neptune.describe_db_clusters()
    except EndpointConnectionError:
        print("neptune resource is not available in this aws region")
        return

    # Nuke all aws neptune resources
    neptune_nuke_instances(time_delete)
    neptune_nuke_clusters(time_delete)
    neptune_nuke_snapshots(time_delete)
    neptune_nuke_subnets()
    neptune_nuke_cluster_params()
    neptune_nuke_group_params()


def neptune_nuke_instances(time_delete):
    """Neptune resources deleting function.

    Deleting all neptune resources with
    a timestamp greater than older_than_seconds.
    That include:
      - clusters
      - snapshots
      - subnets
      - param groups

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune clusters
    neptune_instance_list = neptune_list_instances(time_delete)

    # Nuke all neptune clusters
    for instance in neptune_instance_list:

        try:
            neptune.delete_db_instance(
                DBInstanceIdentifier=instance, SkipFinalSnapshot=True
            )
            print("Nuke neptune instance {0}".format(instance))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBInstanceState":
                logging.info(
                    "neptune instance %s is already being deleted", instance
                )
            else:
                logging.error("Unexpected error: %s", e)


def neptune_nuke_clusters(time_delete):
    """Neptune cluster deleting function."""
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune clusters
    neptune_cluster_list = neptune_list_clusters(time_delete)

    # Nuke all neptune clusters
    for cluster in neptune_cluster_list:

        try:
            neptune.delete_db_cluster(
                DBClusterIdentifier=cluster, SkipFinalSnapshot=True
            )
            print("Nuke neptune cluster {0}".format(cluster))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBClusterStateFault":
                logging.info(
                    "neptune cluster %s is not in started state", cluster
                )
            else:
                logging.error("Unexpected error: %s", e)


def neptune_nuke_snapshots(time_delete):
    """Neptune snapshot deleting function."""
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune snapshots
    neptune_snapshot_list = neptune_list_snapshots(time_delete)

    # Nuke all neptune snapshots
    for snapshot in neptune_snapshot_list:

        # Delete netptune snapshot
        try:
            neptune.delete_db_cluster_snapshot(
                DBClusterSnapshotIdentifier=snapshot
            )
            print("Nuke neptune snapshot{0}".format(snapshot))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def neptune_nuke_subnets():
    """Neptune subnet deleting function."""
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune subnets
    neptune_subnet_list = neptune_list_subnet()

    # Nuke all neptune subnets
    for subnet in neptune_subnet_list:

        try:
            neptune.delete_db_subnet_group(DBSubnetGroupName=subnet)
            print("Nuke neptune subnet {0}".format(subnet))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBSubnetGroupStateFault":
                logging.info("%s is reserved and cannot be modified.", subnet)
            else:
                logging.error("Unexpected error: %s", e)


def neptune_nuke_cluster_params():
    """Neptune cluster params function."""
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune cluster parameters
    neptune_cluster_param_list = neptune_list_cluster_params()

    # Nuke all neptune parameters
    for param in neptune_cluster_param_list:

        try:
            neptune.delete_db_cluster_parameter_group(
                DBClusterParameterGroupName=param
            )
            print("Nuke neptune param {0}".format(param))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBParameterGroupState":
                logging.info("%s is reserved and cannot be modified.", param)
            else:
                logging.error("Unexpected error: %s", e)


def neptune_nuke_group_params():
    """Neptune group parameter function."""
    # define connection
    neptune = boto3.client("neptune")

    # List all neptune parameters
    neptune_param_list = neptune_list_params()

    # Nuke all neptune parameters
    for param in neptune_param_list:

        try:
            neptune.delete_db_parameter_group(DBParameterGroupName=param)
            print("Nuke neptune param {0}".format(param))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBParameterGroupState":
                logging.info("%s is reserved and cannot be modified.", param)
            else:
                logging.error("Unexpected error: %s", e)


def neptune_list_instances(time_delete):
    """Neptune instance list function.

    List IDs of all neptune instances with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter neptune instances
    :returns:
        List of neptune instances IDs
    :rtype:
        [str]
    """
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_instances()

    # Initialize neptune instance list
    neptune_instance_list = []

    # Retrieve all neptune instance identifier
    for instance in response["DBInstances"]:
        if instance["InstanceCreateTime"].timestamp() < time_delete:

            neptune_instance = instance["DBInstanceIdentifier"]
            neptune_instance_list.insert(0, neptune_instance)

    return neptune_instance_list


def neptune_list_clusters(time_delete):
    """Neptune cluster list function.

    List IDs of all neptune clusters with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter neptune clusters
    :returns:
        List of neptune clusters IDs
    :rtype:
        [str]
    """
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_clusters()

    # Initialize neptune cluster list
    neptune_cluster_list = []

    # Retrieve all neptune cluster name
    for cluster in response["DBClusters"]:
        if cluster["ClusterCreateTime"].timestamp() < time_delete:

            neptune_cluster = cluster["DBClusterIdentifier"]
            neptune_cluster_list.insert(0, neptune_cluster)

    return neptune_cluster_list


def neptune_list_snapshots(time_delete):
    """Neptune snapshot list function.

    List IDs of all neptune snapshots with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter neptune snapshots
    :returns:
        List of neptune snapshots IDs
    :rtype:
        [str]
    """
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_cluster_snapshots()

    # Initialize neptune snapshot list
    neptune_snapshot_list = []

    # Retrieve all neptune snapshot identifier
    for snapshot in response["DBClusterSnapshots"]:
        if snapshot["SnapshotCreateTime"].timestamp() < time_delete:

            neptune_snapshot = snapshot["DBClusterSnapshotIdentifier"]
            neptune_snapshot_list.insert(0, neptune_snapshot)

    return neptune_snapshot_list


def neptune_list_subnet():
    """Neptune subnet list function."""
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_subnet_groups()

    # Initialize neptune subnet list
    neptune_subnet_list = []

    # Retrieve all neptune subnet name
    for subnet in response["DBSubnetGroups"]:

        neptune_subnet = subnet["DBSubnetGroupName"]
        neptune_subnet_list.insert(0, neptune_subnet)

    return neptune_subnet_list


def neptune_list_cluster_params():
    """Neptune cluster param list function."""
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_cluster_parameter_groups()

    # Initialize neptune cluster parameters list
    neptune_cluster_param_list = []

    # Retrieve all neptune cluster parameter names
    for param in response["DBClusterParameterGroups"]:

        neptune_cluster_param = param["DBClusterParameterGroupName"]
        neptune_cluster_param_list.insert(0, neptune_cluster_param)

    return neptune_cluster_param_list


def neptune_list_params():
    """Neptune parameter group list function."""
    # define connection
    neptune = boto3.client("neptune")
    response = neptune.describe_db_parameter_groups()

    # Initialize neptune parameters list
    neptune_param_list = []

    # Retrieve all neptune parameters name
    for param in response["DBParameterGroups"]:

        neptune_param = param["DBParameterGroupName"]
        neptune_param_list.insert(0, neptune_param)

    return neptune_param_list
