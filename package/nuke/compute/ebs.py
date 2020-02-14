# -*- coding: utf-8 -*-

"""Module deleting all aws ebs volume."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeEbs:
    """Abstract ebs nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ebs nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def nuke(self, older_than_seconds: float) -> None:
        """Ebs deleting function.

        Deleting all ebs volumes resources with a timestamp
        greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for volume in self.list_ebs(older_than_seconds):
            try:
                self.ec2.delete_volume(VolumeId=volume)
                print("Nuke EBS Volume {0}".format(volume))
            except ClientError as exc:
                nuke_exceptions("ebs volume", volume, exc)

    def list_ebs(self, time_delete: float) -> Iterator[str]:
        """Ebs volume list function.

        List the IDs of all ebs volumes with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter ebs volumes

        :yield Iterator[str]:
            Ebs volumes IDs
        """
        paginator = self.ec2.get_paginator("describe_volumes")

        for page in paginator.paginate():
            for volume in page["Volumes"]:
                if volume["CreateTime"].timestamp() < time_delete:
                    yield volume["VolumeId"]
