# -*- coding: utf-8 -*-

"""Module deleting all elasticache resources."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeElasticache:
    """Abstract elasticache nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize elasticache nuke."""
        self.elasticache = AwsClient().connect("elasticache", region_name)

        try:
            self.elasticache.describe_cache_clusters()
        except EndpointConnectionError:
            print("Elasticache resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
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
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Elasticache clusters to exclude from deletion
        """
        for cluster in self.list_clusters(older_than_seconds, required_tags):
            try:
                self.elasticache.delete_cache_cluster(CacheClusterId=cluster)
                print("Nuke elasticache cluster {0}".format(cluster))
            except ClientError as exc:
                nuke_exceptions("elasticache cluster", cluster, exc)

        for snapshot in self.list_snapshots(older_than_seconds):
            try:
                self.elasticache.delete_snapshot(SnapshotName=snapshot)
                print("Nuke elasticache snapshot {0}".format(snapshot))
            except ClientError as exc:
                nuke_exceptions("elasticache snapshot", snapshot, exc)

        for subnet in self.list_subnets():
            try:
                self.elasticache.delete_cache_subnet_group(CacheSubnetGroupName=subnet)
                print("Nuke elasticache subnet {0}".format(subnet))
            except ClientError as exc:
                nuke_exceptions("elasticache subnet", subnet, exc)

        for param in self.list_param_groups():
            try:
                self.elasticache.delete_cache_parameter_group(CacheParameterGroupName=param)
                print("Nuke elasticache param {0}".format(param))
            except ClientError as exc:
                nuke_exceptions("elasticache param", param, exc)

    def list_clusters(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Elasticache cluster list function.

        List IDs of all elasticache clusters with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter elasticache clusters
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Elasticache clusters to exclude from deletion

        :yield Iterator[str]:
            Elasticache clusters IDs
        """
        paginator = self.elasticache.get_paginator("describe_cache_clusters")

        for page in paginator.paginate():
            for cluster in page["CacheClusters"]:
                if cluster["CacheClusterCreateTime"].timestamp() < time_delete:
                    if required_tags and self._cluster_has_required_tags(cluster, required_tags):
                        continue
                    yield cluster["CacheClusterId"]

    def list_snapshots(self, time_delete: float) -> Iterator[str]:
        """Elasticache snapshots list function.

        List names of all elasticache snapshots with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter elasticache snapshots

        :yield Iterator[str]:
            Elasticache snapshots names
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
        paginator = self.elasticache.get_paginator("describe_cache_subnet_groups")

        for page in paginator.paginate():
            for subnet in page["CacheSubnetGroups"]:
                yield subnet["CacheSubnetGroupName"]

    def list_param_groups(self) -> Iterator[str]:
        """Elasticache parameters group list function.

        List elasticache param group names

        :yield Iterator[str]:
            Elasticache param group names
        """
        paginator = self.elasticache.get_paginator("describe_cache_parameter_groups")

        for page in paginator.paginate():
            for param_group in page["CacheParameterGroups"]:
                yield param_group["CacheParameterGroupName"]

    def _cluster_has_required_tags(self, cluster: dict, required_tags: Dict[str, str]) -> bool:
        """Check if the cluster has the required tags.

        :param dict cluster:
            The Elasticache cluster dictionary
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the cluster has all the required tags, False otherwise
        """
        try:
            tags = self.elasticache.list_tags_for_resource(ResourceName=cluster["ARN"])
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags["TagList"]}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for Elasticache cluster {cluster['CacheClusterId']}: {e}")
            return False
