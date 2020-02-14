# -*- coding: utf-8 -*-

"""Module deleting all rds resources."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.exceptions import nuke_exceptions


class NukeRds:
    """Abstract rds nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize rds nuke."""
        if region_name:
            self.rds = boto3.client("rds", region_name=region_name)
        else:
            self.rds = boto3.client("rds")

        try:
            self.rds.describe_db_clusters()
        except EndpointConnectionError:
            print("Rds resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
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
        for instance in self.list_instances(older_than_seconds):
            try:
                self.rds.delete_db_instance(
                    DBInstanceIdentifier=instance, SkipFinalSnapshot=True
                )
                print("Stop rds instance {0}".format(instance))
            except ClientError as exc:
                nuke_exceptions("rds instance", instance, exc)

        for cluster in self.list_clusters(older_than_seconds):
            try:
                self.rds.delete_db_cluster(
                    DBClusterIdentifier=cluster, SkipFinalSnapshot=True
                )
                print("Nuke rds cluster {0}".format(cluster))
            except ClientError as exc:
                nuke_exceptions("rds cluster", cluster, exc)

    def list_instances(self, time_delete: float) -> Iterator[str]:
        """Rds instance list function.

        List IDs of all rds instances with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter rds instances

        :yield Iterator[str]:
            Rds instances IDs
        """
        paginator = self.rds.get_paginator("describe_db_instances")

        for page in paginator.paginate():
            for instance in page["DBInstances"]:
                if instance["InstanceCreateTime"].timestamp() < time_delete:
                    yield instance["DBInstanceIdentifier"]

    def list_clusters(self, time_delete: float) -> Iterator[str]:
        """Aurora cluster list function.

        List IDs of all aurora clusters with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter aurora clusters

        :yield Iterator[str]:
            Aurora clusters IDs
        """
        paginator = self.rds.get_paginator("describe_db_clusters")

        for page in paginator.paginate():
            for cluster in page["DBClusters"]:
                if cluster["ClusterCreateTime"].timestamp() < time_delete:
                    yield cluster["DBClusterIdentifier"]
