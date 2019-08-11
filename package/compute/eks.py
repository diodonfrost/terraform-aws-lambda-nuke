# -*- coding: utf-8 -*-

"""Module deleting all aws EKS cluster resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_eks(older_than_seconds):
    """EKS cluster deleting function.

    Deleting all EKS clusters with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    eks = boto3.client("eks")

    try:
        eks.list_clusters()
    except EndpointConnectionError:
        print("eks resource is not available in this aws region")
        return

    # Deleting eks clusters
    for cluster in eks_list_clusters(time_delete):
        try:
            eks.delete_cluster(name=cluster)
            print("Nuke EKS Cluster{0}".format(cluster))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def eks_list_clusters(time_delete):
    """EKS cluster list function.

    List the names of all EKS clusters with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter EKS clusters
    :returns:
        List of EKS cluster names
    :rtype:
        [str]
    """
    eks_cluster_list = []
    eks = boto3.client("eks")
    response = eks.list_clusters()

    for kube in response["clusters"]:
        k8s = eks.describe_cluster(name=kube)
        if k8s["cluster"]["createdAt"].timestamp() < time_delete:
            eks_cluster_list.append(kube)
    return eks_cluster_list
