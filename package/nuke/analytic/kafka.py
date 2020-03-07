# -*- coding: utf-8 -*-

"""Module deleting all kafka cluster."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeKafka:
    """Abstract kafka nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize kafka nuke."""
        if region_name:
            self.kafka = boto3.client("kafka", region_name=region_name)
        else:
            self.kafka = boto3.client("kafka")

    def nuke(self, older_than_seconds: float) -> None:
        """Kafka deleting function.

        Deleting all kafka cluster with a timestamp greater than
        older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for cluster_arn in self.list_cluster(older_than_seconds):
            try:
                self.kafka.delete_cluster(ClusterArn=cluster_arn)
                print("Nuke kafka cluster {0}".format(cluster_arn))
            except ClientError as exc:
                nuke_exceptions("kafka cluster", cluster_arn, exc)

    def list_cluster(self, time_delete: float) -> Iterator[str]:
        """Kafka cluster list function.

        List the IDs of all kafka clusters with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter ebs volumes

        :yield Iterator[str]:
            Kafka cluster arm
        """
        paginator = self.kafka.get_paginator("list_clusters")

        for page in paginator.paginate():
            for cluster in page["ClusterInfoList"]:
                if cluster["CreationTime"].timestamp() < time_delete:
                    yield cluster["ClusterArn"]
