# -*- coding: utf-8 -*-

"""This script nuke all neptune resources"""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_neptune(older_than_seconds):
    """
         neptune function for destroy all neptune resources
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
    """
         neptune function for destroy all neptune instances
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
    """
         neptune function for destroy all neptune clusters
    """
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
    """
         neptune function for destroy all neptune snapshots
    """
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
    """
         neptune function for destroy all neptune subnets
    """
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
    """
         neptune function for destroy all neptune cluster params
    """
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
    """
         neptune function for destroy all neptune group params
    """
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
    """
       Aws neptune list instances, list name of
       all neptune instances and return it in list.
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
    """
       Aws neptune list clusters, list name of
       all neptune clusters and return it in list.
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
    """
       Aws neptune list snapshots, list name of
       all neptune snapshots and return it in list.
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
    """
       Aws neptune list subnets, list name of
       all neptune subnets and return it in list.
    """

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
    """
       Aws neptune list cluster parameters, list name of
       all neptune cluster parameters and return it in list.
    """

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
    """
       Aws neptune list parameters, list name of
       all neptune parameters and return it in list.
    """

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
