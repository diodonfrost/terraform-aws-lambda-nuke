# -*- coding: utf-8 -*-

"""Module deleting all kafka cluster."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeKafka:
    """Abstract kafka nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize kafka nuke."""
        self.kafka = AwsClient().connect("kafka", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Kafka deleting function.

        Deleting all kafka clusters with a timestamp
        greater than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Kafka clusters to exclude from deletion
        """
        for cluster_arn in self.list_cluster(older_than_seconds, required_tags):
            try:
                self.kafka.delete_cluster(ClusterArn=cluster_arn)
                print("Nuke Kafka cluster {0}".format(cluster_arn))
            except ClientError as exc:
                nuke_exceptions("Kafka cluster", cluster_arn, exc)

    def list_cluster(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Kafka cluster list function.

        List the ARNs of all Kafka clusters with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering Kafka clusters
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Kafka clusters to exclude from deletion

        :yield Iterator[str]:
            Kafka cluster ARNs
        """
        paginator = self.kafka.get_paginator("list_clusters")

        for page in paginator.paginate():
            for cluster in page["ClusterInfoList"]:
                if cluster["CreationTime"].timestamp() < time_delete:
                    if required_tags and not self._cluster_has_required_tags(cluster["ClusterArn"], required_tags):
                        continue
                    yield cluster["ClusterArn"]

    def _cluster_has_required_tags(self, cluster_arn: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Kafka cluster has the required tags.

        :param str cluster_arn:
            The ARN of the Kafka cluster
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the Kafka cluster has all the required tags, False otherwise
        """
        try:
            response = self.kafka.list_tags_for_resource(ResourceArn=cluster_arn)
            tags = response["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Kafka cluster tagging", cluster_arn, exc)
            return False
