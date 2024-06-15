# -*- coding: utf-8 -*-

"""Module deleting all ec2 snapshot."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeSnapshot:
    """Abstract ec2 snapshot in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize snapshot nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Ec2 snapshot deleting function.

        Delete all snapshot present on the current aws account.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the snapshots to exclude from deletion
        """
        for snapshot_id in self.list_snapshot(older_than_seconds, required_tags):
            try:
                self.ec2.delete_snapshot(SnapshotId=snapshot_id)
                print("Nuke snapshot {0}".format(snapshot_id))
            except ClientError as exc:
                nuke_exceptions("ec2 snapshot", snapshot_id, exc)

    def list_snapshot(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Snapshot list function.

        List the IDs of all snapshots with a timestamp lower
        than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering snapshots
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the snapshots to exclude from deletion

        :yield Iterator[str]:
            Snapshot IDs
        """
        paginator = self.ec2.get_paginator("describe_snapshots")

        for page in paginator.paginate(OwnerIds=["self"]):
            for snapshot in page["Snapshots"]:
                if snapshot["StartTime"].timestamp() < time_delete:
                    if required_tags and self._snapshot_has_required_tags(snapshot["SnapshotId"], required_tags):
                        continue
                    yield snapshot["SnapshotId"]

    def _snapshot_has_required_tags(self, snapshot_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the snapshot has the required tags.

        :param str snapshot_id:
            The ID of the EC2 snapshot
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the snapshot has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [snapshot_id]}]
            )
            snapshot_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if snapshot_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("ec2 snapshot tagging", snapshot_id, exc)
            return False
