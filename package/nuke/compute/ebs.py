# -*- coding: utf-8 -*-

"""Module deleting all aws ebs volume."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEbs:
    """Abstract ebs nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ebs nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Ebs deleting function.

        Deleting all ebs volumes resources with a timestamp
        greater than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EBS volumes to exclude from deletion
        """
        for volume in self.list_ebs(older_than_seconds, required_tags):
            try:
                self.ec2.delete_volume(VolumeId=volume)
                print("Nuke EBS Volume {0}".format(volume))
            except ClientError as exc:
                nuke_exceptions("ebs volume", volume, exc)

    def list_ebs(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Ebs volume list function.

        List the IDs of all ebs volumes with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering EBS volumes
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EBS volumes to exclude from deletion

        :yield Iterator[str]:
            Ebs volumes IDs
        """
        paginator = self.ec2.get_paginator("describe_volumes")

        for page in paginator.paginate():
            for volume in page["Volumes"]:
                if volume["CreateTime"].timestamp() < time_delete:
                    if required_tags and self._volume_has_required_tags(volume["VolumeId"], required_tags):
                        continue
                    yield volume["VolumeId"]

    def _volume_has_required_tags(self, volume_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the volume has the required tags.

        :param str volume_id:
            The ID of the EBS volume
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the volume has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [volume_id]}]
            )
            volume_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if volume_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("ebs volume tagging", volume_id, exc)
            return False
