# -*- coding: utf-8 -*-

"""Module deleting all aws emr cluster."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEmr:
    """Abstract emr nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize emr nuke."""
        self.emr = AwsClient().connect("emr", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Emr deleting function.

        Deleting all emr cluster resources with a timestamp
        greater than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EMR clusters to exclude from deletion
        """
        for cluster_id in self.list_emr(older_than_seconds, required_tags):
            try:
                self.emr.terminate_job_flows(JobFlowIds=[cluster_id])
                print("Nuke EMR Cluster {0}".format(cluster_id))
            except ClientError as exc:
                nuke_exceptions("EMR cluster", cluster_id, exc)

    def list_emr(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Emr cluster list function.

        List the IDs of all EMR clusters with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering EMR clusters
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EMR clusters to exclude from deletion

        :yield Iterator[str]:
            EMR cluster IDs
        """
        paginator = self.emr.get_paginator("list_clusters")

        for page in paginator.paginate():
            for cluster in page["Clusters"]:
                timeline = cluster["Status"]["Timeline"]
                if timeline["CreationDateTime"].timestamp() < time_delete:
                    if required_tags and self._cluster_has_required_tags(cluster["Id"], required_tags):
                        continue
                    yield cluster["Id"]

    def _cluster_has_required_tags(self, cluster_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the EMR cluster has the required tags.

        :param str cluster_id:
            The ID of the EMR cluster
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the EMR cluster has all the required tags, False otherwise
        """
        try:
            response = self.emr.describe_cluster(ClusterId=cluster_id)
            tags = response["Cluster"]["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("EMR cluster tagging", cluster_id, exc)
            return False
