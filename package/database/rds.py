# -*- coding: utf-8 -*-

"""Module deleting all rds resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_rds(older_than_seconds):
    """Rds resources deleting function.

    Deleting all rds resources with
    a timestamp greater than older_than_seconds.
    That include:
      - Aurora clusters
      - rds instances
      - snapshots
      - subnets
      - param groups

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    rds = boto3.client("rds")

    # Test if rds services is present in current aws region
    try:
        rds.describe_db_instances()
    except EndpointConnectionError:
        print("rds resource is not available in this aws region")
        return

    rds_nuke_instances(time_delete)
    rds_nuke_clusters(time_delete)


def rds_nuke_instances(time_delete):
    """Rds instance nuke function."""
    rds = boto3.client("rds")

    for instance in rds_list_instances(time_delete):
        try:
            rds.delete_db_instance(DBInstanceIdentifier=instance)
            print("Stop rds instance {0}".format(instance))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBInstanceState":
                logging.info("rds instance %s is not started", instance)
            else:
                logging.error("Unexpected error: %s", e)


def rds_nuke_clusters(time_delete):
    """Rds cluster nuke function."""
    rds = boto3.client("rds")

    for cluster in rds_list_clusters(time_delete):
        try:
            rds.delete_db_cluster(DBClusterIdentifier=cluster)
            print("Nuke rds cluster {0}".format(cluster))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidDBClusterStateFault":
                logging.info("rds cluster %s is not started", cluster)
            else:
                logging.error("Unexpected error: %s", e)


def rds_list_instances(time_delete):
    """Rds instance list function.

    List IDs of all rds instances with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter rds instances
    :returns:
        List of rds instances IDs
    :rtype:
        [str]
    """
    rds_instance_list = []
    rds = boto3.client("rds")
    paginator = rds.get_paginator("describe_db_instances")

    for page in paginator.paginate():
        for instance in page["DBInstances"]:
            if instance["InstanceCreateTime"].timestamp() < time_delete:
                rds_instance_list.append(instance["DBInstanceIdentifier"])
    return rds_instance_list


def rds_list_clusters(time_delete):
    """Aurora cluster list function.

    List IDs of all aurora clusters with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter aurora clusters
    :returns:
        List of aurora clusters IDs
    :rtype:
        [str]
    """
    rds_cluster_list = []
    rds = boto3.client("rds")
    paginator = rds.get_paginator("describe_db_clusters")

    for page in paginator.paginate():
        for cluster in page["DBClusters"]:
            if cluster["ClusterCreateTime"].timestamp() < time_delete:
                rds_cluster_list.append(cluster["DBClusterIdentifier"])
    return rds_cluster_list
