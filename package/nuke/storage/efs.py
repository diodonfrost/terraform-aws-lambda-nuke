# -*- coding: utf-8 -*-

"""Module deleting all aws efs resources."""

from typing import Iterator

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEfs:
    """Abstract efs nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize efs nuke."""
        self.efs = AwsClient().connect("efs", region_name)

        try:
            self.efs.describe_file_systems()
        except EndpointConnectionError:
            print("EFS resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
        """EFS deleting function.

        Deleting all efs with a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for efs_file_system in self.list_file_systems(older_than_seconds):
            try:
                self.efs.delete_file_system(FileSystemId=efs_file_system)
                print("Nuke EFS share {0}".format(efs_file_system))
            except ClientError as exc:
                nuke_exceptions("efs filesystem", efs_file_system, exc)

    def list_file_systems(self, time_delete: float) -> Iterator[str]:
        """EFS list function.

        List IDS of all efs with a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter efs

        :yield Iterator[str]:
            Rfs IDs
        """
        paginator = self.efs.get_paginator("describe_file_systems")

        for page in paginator.paginate():
            for filesystem in page["FileSystems"]:
                if filesystem["CreationTime"].timestamp() < time_delete:
                    yield filesystem["FileSystemId"]
