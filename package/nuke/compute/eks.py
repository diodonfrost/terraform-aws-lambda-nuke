# -*- coding: utf-8 -*-

"""Module deleting all aws EKS cluster resources."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.exceptions import nuke_exceptions


class NukeEks:
    """Abstract eks nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize eks nuke."""
        if region_name:
            self.eks = boto3.client("eks", region_name=region_name)
        else:
            self.eks = boto3.client("eks")

        try:
            self.eks.list_clusters()
        except EndpointConnectionError:
            print("eks resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
        """EKS cluster deleting function.

        Deleting all EKS clusters with a timestamp greater than
        older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for cluster in self.list_clusters(older_than_seconds):
            try:
                self.eks.delete_cluster(name=cluster)
                print("Nuke EKS Cluster{0}".format(cluster))
            except ClientError as exc:
                nuke_exceptions("eks cluster", cluster, exc)

    def list_clusters(self, time_delete: float) -> Iterator[str]:
        """EKS cluster list function.

        List the names of all EKS clusters with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter EKS clusters

        :yield Iterator[str]:
            EKS cluster names
        """
        response = self.eks.list_clusters()

        for kube in response["clusters"]:
            k8s = self.eks.describe_cluster(name=kube)
            if k8s["cluster"]["createdAt"].timestamp() < time_delete:
                yield kube
