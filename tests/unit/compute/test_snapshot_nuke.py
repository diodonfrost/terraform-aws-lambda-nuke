# -*- coding: utf-8 -*-
"""Tests for the snapshot nuke class."""

import boto3
import time

from moto import mock_ec2

from package.nuke.compute.snapshot import NukeSnapshot

from .utils import create_snapshot

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count",
    [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ],
)
@mock_ec2
def test_snapshot_nuke(aws_region, older_than_seconds, result_count):
    """Verify snapshot nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_snapshot(region_name=aws_region)
    snapshot = NukeSnapshot(aws_region)
    snapshot.nuke(older_than_seconds=older_than_seconds)
    snapshot_list = client.describe_snapshots(
        Filters=[{"Name": "owner-id", "Values": ["111122223333"]}]
    )["Snapshots"]
    assert len(snapshot_list) == result_count
