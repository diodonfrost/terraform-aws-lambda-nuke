# -*- coding: utf-8 -*-
"""Tests for the snapshot nuke class."""

import time

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws

from package.nuke.compute.snapshot import NukeSnapshot

from .utils import create_snapshot


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, expect_deleted",
    [
        ("eu-west-1", time.time() + 43200, True),
        ("eu-west-2", time.time() + 43200, True),
        ("eu-west-2", 630720000, False),
    ],
)
@mock_aws
def test_snapshot_nuke(aws_region, older_than_seconds, expect_deleted):
    """Verify snapshot nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    snapshot_id = create_snapshot(region_name=aws_region)
    snapshot = NukeSnapshot(aws_region)
    snapshot.nuke(older_than_seconds=older_than_seconds)

    if expect_deleted:
        with pytest.raises(ClientError):
            client.describe_snapshots(SnapshotIds=[snapshot_id])
    else:
        snapshot_list = client.describe_snapshots(SnapshotIds=[snapshot_id])[
            "Snapshots"
        ]
        assert len(snapshot_list) == 1
