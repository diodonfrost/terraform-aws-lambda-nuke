# -*- coding: utf-8 -*-

"""Module deleting all redshift resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_redshift(older_than_seconds):
    """Redshift resources deleting function.

    Deleting all redshift resources with
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
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    redshift = boto3.client("redshift")

    # Test if redshift services is present in current aws region
    try:
        redshift.describe_clusters()
    except EndpointConnectionError:
        print("redshift resource is not available in this aws region")
        return

    redshift_nuke_clusters(time_delete)
    redshift_nuke_snapshots(time_delete)
    redshift_nuke_subnets()
    redshift_nuke_param_groups()


def redshift_nuke_clusters(time_delete):
    """Redshift cluster deleting function."""
    redshift = boto3.client("redshift")

    for cluster in redshift_list_clusters(time_delete):
        try:
            redshift.delete_cluster(
                ClusterIdentifier=cluster, SkipFinalClusterSnapshot=True
            )
            print("Nuke redshift cluster{0}".format(cluster))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidClusterStateFault":
                logging.info(
                    "redshift cluster %s is not in state started", cluster
                )
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_snapshots(time_delete):
    """Redshift snapshot deleting function."""
    redshift = boto3.client("redshift")

    for snapshot in redshift_list_snapshots(time_delete):
        try:
            redshift.delete_cluster_snapshot(SnapshotIdentifier=snapshot)
            print("Nuke redshift snapshot {0}".format(snapshot))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidClusterSnapshotStateFault":
                logging.info(
                    "redshift snap %s is not in state available", snapshot
                )
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_subnets():
    """Redshift subnet deleting function."""
    redshift = boto3.client("redshift")

    for subnet in redshift_list_subnet():
        try:
            redshift.delete_cluster_subnet_group(
                ClusterSubnetGroupName=subnet
            )
            print("Nuke redshift subnet {0}".format(subnet))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidClusterSubnetGroupStateFault":
                logging.info(
                    "redshift subnet %s is not in state available", subnet
                )
            else:
                logging.error("Unexpected error: %s", e)


def redshift_nuke_param_groups():
    """Redshift parameter group deleting function."""
    redshift = boto3.client("redshift")

    for param in redshift_list_cluster_params():
        try:
            redshift.delete_cluster_parameter_group(ParameterGroupName=param)
            print("Nuke redshift param {0}".format(param))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidClusterParameterGroupStateFault":
                logging.info(
                    "redshift param %s is not in state available", param
                )
            elif error_code == "InvalidParameterValue":
                logging.info(
                    "default %s parameter group cannot be deleted", param
                )
            else:
                logging.error("Unexpected error: %s", e)


def redshift_list_clusters(time_delete):
    """Redshift cluster list function.

    List IDs of all redshift cluster with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter redshift cluster
    :returns:
        List of redshift cluster IDs
    :rtype:
        [str]
    """
    redshift_cluster_list = []
    redshift = boto3.client("redshift")
    paginator = redshift.get_paginator("describe_clusters")

    for page in paginator.paginate():
        for cluster in page["Clusters"]:
            if cluster["ClusterCreateTime"].timestamp() < time_delete:
                redshift_cluster = cluster["ClusterIdentifier"]
                redshift_cluster_list.insert(0, redshift_cluster)
    return redshift_cluster_list


def redshift_list_snapshots(time_delete):
    """Redshift snapshot list function.

    List IDs of all redshift snapshots with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter redshift snapshots
    :returns:
        List of redshift snapshots IDs
    :rtype:
        [str]
    """
    redshift_snapshot_list = []
    redshift = boto3.client("redshift")
    paginator = redshift.get_paginator("describe_cluster_snapshots")

    for page in paginator.paginate():
        for snapshot in page["Snapshots"]:
            if snapshot["SnapshotCreateTime"].timestamp() < time_delete:
                redshift_snapshot = snapshot["SnapshotIdentifier"]
                redshift_snapshot_list.insert(0, redshift_snapshot)
    return redshift_snapshot_list


def redshift_list_subnet():
    """Redshift subnet list function."""
    redshift_subnet_list = []
    redshift = boto3.client("redshift")
    paginator = redshift.get_paginator("describe_cluster_subnet_groups")

    for page in paginator.paginate():
        for subnet in page["ClusterSubnetGroups"]:
            redshift_subnet = subnet["ClusterSubnetGroupName"]
            redshift_subnet_list.insert(0, redshift_subnet)
    return redshift_subnet_list


def redshift_list_cluster_params():
    """Redshift cluster parameter list function."""
    redshift_cluster_param_list = []
    redshift = boto3.client("redshift")
    paginator = redshift.get_paginator("describe_cluster_parameter_groups")

    for page in paginator.paginate():
        for param in page["ParameterGroups"]:
            redshift_cluster_param = param["ParameterGroupName"]
            redshift_cluster_param_list.insert(0, redshift_cluster_param)
    return redshift_cluster_param_list
