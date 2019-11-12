"""Tests for the spot nuke class."""

import boto3
import time

from moto import mock_ec2

from package.compute.spot import NukeSpot

from .utils import create_spot

@mock_ec2
def test_spot_nuke():
    """Verify spot nuke class."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_spot(region_name=aws_region, count=3)
    spot = NukeSpot(aws_region)
    spot.nuke(older_than_seconds=time.time())
    spot_request_list = client.describe_spot_instance_requests()["SpotInstanceRequests"]
    assert len(spot_request_list) == 0
