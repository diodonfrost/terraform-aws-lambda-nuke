# -*- coding: utf-8 -*-

"""Module deleting all aws emr cluster."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeEmr:
    """Abstract emr nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize emr nuke."""
        if region_name:
            self.emr = boto3.client("emr", region_name=region_name)
        else:
            self.emr = boto3.client("emr")

    def nuke(self, older_than_seconds: float) -> None:
        """Emr deleting function.

        Deleting all emr cluster resources with a timestamp
        greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for cluster_id in self.list_emr(older_than_seconds):
            try:
                self.emr.terminate_job_flows(JobFlowIds=[cluster_id])
                print("Nuke emr cluster {0}".format(cluster_id))
            except ClientError as exc:
                nuke_exceptions("emr cluster", cluster_id, exc)

    def list_emr(self, time_delete: float) -> Iterator[str]:
        """Emr volume list function.

        List the IDs of all emr clusters with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter ebs volumes

        :yield Iterator[str]:
            Emr cluster IDs
        """
        paginator = self.emr.get_paginator("list_clusters")

        for page in paginator.paginate():
            for cluster in page["Clusters"]:
                timeline = cluster["Status"]["Timeline"]
                if timeline["CreationDateTime"].timestamp() < time_delete:
                    yield cluster["Id"]
