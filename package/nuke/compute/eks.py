# -*- coding: utf-8 -*-

"""Module deleting all aws EKS cluster resources."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEks:
    """Abstract eks nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize eks nuke."""
        self.eks = AwsClient().connect("eks", region_name)

        try:
            self.eks.list_clusters()
        except EndpointConnectionError:
            print("eks resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """EKS cluster deleting function.

        Deleting all EKS clusters with a timestamp greater than
        older_than_seconds and optionally matching required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the clusters to exclude from deletion
        """
        for cluster_name in self.list_clusters(older_than_seconds, required_tags):
            try:
                self.eks.delete_cluster(name=cluster_name)
                print("Nuke EKS Cluster {0}".format(cluster_name))
            except ClientError as exc:
                nuke_exceptions("eks cluster", cluster_name, exc)

    def list_clusters(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """EKS cluster list function.

        List the names of all EKS clusters with a timestamp lower than
        time_delete and optionally matching required tags.

        :param int time_delete:
            Timestamp in seconds used for filter EKS clusters
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the clusters to exclude from deletion

        :yield Iterator[str]:
            EKS cluster names
        """
        response = self.eks.list_clusters()

        for cluster_name in response["clusters"]:
            cluster_details = self.eks.describe_cluster(name=cluster_name)
            if cluster_details["cluster"]["createdAt"].timestamp() < time_delete:
                if required_tags and not self._cluster_has_required_tags(cluster_name, required_tags):
                    continue
                yield cluster_name

    def _cluster_has_required_tags(self, cluster_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the EKS cluster has the required tags.

        :param str cluster_name:
            The name of the EKS cluster
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the cluster has all the required tags, False otherwise
        """
        try:
            response = self.eks.list_tags_for_resource(resourceArn=cluster_name)
            tags = response["tags"]
            tag_dict = {tag["key"]: tag["value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("EKS cluster tagging", cluster_name, exc)
            return False
