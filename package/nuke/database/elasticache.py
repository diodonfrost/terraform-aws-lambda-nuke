# -*- coding: utf-8 -*-

"""Module deleting all elasticache resources."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.exceptions import nuke_exceptions


class NukeElasticache:
    """Abstract elasticache nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize elasticache nuke."""
        if region_name:
            self.elasticache = boto3.client(
                "elasticache", region_name=region_name
            )
        else:
            self.elasticache = boto3.client("elasticache")

        try:
            self.elasticache.describe_cache_clusters()
        except EndpointConnectionError:
            print("Elasticache resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
        """Elasticache resources deleting function.

        Deleting all elasticache resources with
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
        self.nuke_clusters(older_than_seconds)
        self.nuke_snapshots(older_than_seconds)
        self.nuke_subnets()
        self.nuke_param_groups()

    def nuke_clusters(self, time_delete: float) -> None:
        """Elasticache cluster deleting function.

        Deleting elasticache cluster with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for cluster in self.list_clusters(time_delete):
            try:
                self.elasticache.delete_cache_cluster(CacheClusterId=cluster)
                print("Nuke elasticache cluster {0}".format(cluster))
            except ClientError as exc:
                nuke_exceptions("elasticache cluster", cluster, exc)

    def nuke_snapshots(self, time_delete: float) -> None:
        """Elasticache snapshot deleting function.

        Deleting elasticache snapshot with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for snapshot in self.list_snapshots(time_delete):
            try:
                self.elasticache.delete_snapshot(SnapshotName=snapshot)
                print("Nuke elasticache snapshot {0}".format(snapshot))
            except ClientError as exc:
                nuke_exceptions("elasticache snapshot", snapshot, exc)

    def nuke_subnets(self) -> None:
        """Elasticache subnet deleting function.

        Deleting elasticache subnets
        """
        for subnet in self.list_subnets():

            try:
                self.elasticache.delete_cache_subnet_group(
                    CacheSubnetGroupName=subnet
                )
                print("Nuke elasticache subnet{0}".format(subnet))
            except ClientError as exc:
                nuke_exceptions("elasticache subnet", subnet, exc)

    def nuke_param_groups(self) -> None:
        """Elasticache param group deleting function.

        Deleting elasticache parameter groups
        """
        for param in self.list_param_groups():
            try:
                self.elasticache.delete_cache_parameter_group(
                    CacheParameterGroupName=param
                )
                print("Nuke elasticache param {0}".format(param))
            except ClientError as exc:
                nuke_exceptions("elasticache param", param, exc)

    def list_clusters(self, time_delete: float) -> Iterator[str]:
        """Elasticache cluster list function.

        List IDs of all elasticache clusters with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter elasticache clusters

        :yield Iterator[str]:
            Elasticache clusters IDs
        """
        paginator = self.elasticache.get_paginator("describe_cache_clusters")

        for page in paginator.paginate():
            for cluster in page["CacheClusters"]:
                if cluster["CacheClusterCreateTime"].timestamp() < time_delete:
                    yield cluster["CacheClusterId"]

    def list_snapshots(self, time_delete: float) -> Iterator[str]:
        """Elasticache snapshots list function.

        List names of all elasticache snapshots with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter elasticache snapshots

        :yield Iterator[str]:
            Elasticache snpashots names
        """
        paginator = self.elasticache.get_paginator("describe_snapshots")

        for page in paginator.paginate():
            for snapshot in page["Snapshots"]:
                date_snap = snapshot["NodeSnapshots"][0]["SnapshotCreateTime"]
                if date_snap.timestamp() < time_delete:
                    yield snapshot["SnapshotName"]

    def list_subnets(self) -> Iterator[str]:
        """Elasticache subnet list function.

        List elasticache subnet group names

        :yield Iterator[str]:
            Elasticache subnet group names
        """
        paginator = self.elasticache.get_paginator(
            "describe_cache_subnet_groups"
        )

        for page in paginator.paginate():
            for subnet in page["CacheSubnetGroups"]:
                yield subnet["CacheSubnetGroupName"]

    def list_param_groups(self) -> Iterator[str]:
        """Elasticache parameters group list function.

        List elasticache param group names

        :yield Iterator[str]:
            Elasticache param group names
        """
        paginator = self.elasticache.get_paginator(
            "describe_cache_parameter_groups"
        )

        for page in paginator.paginate():
            for param_group in page["CacheParameterGroups"]:
                yield param_group["CacheParameterGroupName"]
