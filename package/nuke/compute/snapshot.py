# -*- coding: utf-8 -*-

"""Module deleting all ec2 snpashot."""

from typing import Iterator

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeSnapshot:
    """Abstract ec2 snpashot in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize snpashot nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float) -> None:
        """Ec2 snapshot deleting function.

        Delete all snapshot present on the current aws account.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for snapshot_id in self.list_snapshot(older_than_seconds):
            try:
                self.ec2.delete_snapshot(SnapshotId=snapshot_id)
                print("Nuke snapshot {0}".format(snapshot_id))
            except ClientError as exc:
                nuke_exceptions("ec2 snapshot", snapshot_id, exc)

    def list_snapshot(self, time_delete: float) -> Iterator[str]:
        """Snapshot list function.

        List the IDs of all snapshot owner with a timestamp lower
        than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter AMI

        :yield Iterator[str]:
            AMI IDs
        """
        paginator = self.ec2.get_paginator("describe_snapshots")

        for page in paginator.paginate(OwnerIds=["self"]):
            for snapshot in page["Snapshots"]:
                if snapshot["StartTime"].timestamp() < time_delete:
                    yield snapshot["SnapshotId"]
