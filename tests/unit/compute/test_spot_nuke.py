"""Tests for the spot nuke class."""

import boto3
import time

from moto import mock_ec2

from package.nuke.compute.spot import NukeSpot

from .utils import create_spot

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 3),
    ]
)
@mock_ec2
def test_spot_nuke(aws_region, older_than_seconds, result_count):
    """Verify spot nuke class."""
    client = boto3.client("ec2", region_name=aws_region)

    create_spot(region_name=aws_region, count=3)
    spot = NukeSpot(aws_region)
    spot.nuke(older_than_seconds=older_than_seconds)
    spot_request_list = client.describe_spot_instance_requests()["SpotInstanceRequests"]
    assert len(spot_request_list) == result_count
