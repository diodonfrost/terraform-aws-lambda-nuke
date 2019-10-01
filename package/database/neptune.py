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
    neptune = boto3.client("neptune")

    # Test if neptune services is present in current aws region
    try:
        neptune.describe_db_clusters()
    except EndpointConnectionError:
        print("neptune resource is not available in this aws region")
        return

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
    neptune = boto3.client("neptune")

    for instance in neptune_list_instances(time_delete):
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
    neptune = boto3.client("neptune")

    for cluster in neptune_list_clusters(time_delete):
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
    neptune = boto3.client("neptune")

    for snapshot in neptune_list_snapshots(time_delete):
        try:
            neptune.delete_db_cluster_snapshot(
                DBClusterSnapshotIdentifier=snapshot
            )
            print("Nuke neptune snapshot{0}".format(snapshot))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def neptune_nuke_subnets():
    """Neptune subnet deleting function."""
    neptune = boto3.client("neptune")

    for subnet in neptune_list_subnet():
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
    neptune = boto3.client("neptune")

    for param in neptune_list_cluster_params():
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
    neptune = boto3.client("neptune")

    for param in neptune_list_params():
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
    neptune_instance_list = []
    neptune = boto3.client("neptune")
    response = neptune.describe_db_instances()

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
    neptune_cluster_list = []
    neptune = boto3.client("neptune")
    response = neptune.describe_db_clusters()

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
    neptune_snapshot_list = []
    neptune = boto3.client("neptune")
    response = neptune.describe_db_cluster_snapshots()

    for snapshot in response["DBClusterSnapshots"]:
        if snapshot["SnapshotCreateTime"].timestamp() < time_delete:
            neptune_snapshot_list.append(
                snapshot["DBClusterSnapshotIdentifier"]
            )
    return neptune_snapshot_list


def neptune_list_subnet():
    """Neptune subnet list function."""
    neptune_subnet_list = []
    neptune = boto3.client("neptune")
    paginator = neptune.get_paginator("describe_db_subnet_groups")

    for page in paginator.paginate():
        for subnet in page["DBSubnetGroups"]:
            neptune_subnet_list.append(subnet["DBSubnetGroupName"])
    return neptune_subnet_list


def neptune_list_cluster_params():
    """Neptune cluster param list function."""
    neptune_cluster_param_list = []
    neptune = boto3.client("neptune")
    response = neptune.describe_db_cluster_parameter_groups()

    for param in response["DBClusterParameterGroups"]:
        neptune_cluster_param_list.append(param["DBClusterParameterGroupName"])
    return neptune_cluster_param_list


def neptune_list_params():
    """Neptune parameter group list function."""
    neptune_param_list = []
    neptune = boto3.client("neptune")
    paginator = neptune.get_paginator("describe_db_parameter_groups")

    for page in paginator.paginate():
        for param in page["DBParameterGroups"]:
            neptune_param_list.append(param["DBParameterGroupName"])
    return neptune_param_list
