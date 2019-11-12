"""Tests for the ebs nuke class."""

import boto3
import time

from moto import mock_ec2

from package.compute.ebs import NukeEbs

from .utils import create_ebs


@mock_ec2
def test_ebs_nuke():
    """Verify ebs volume nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_ebs(region_name=aws_region)
    ebs = NukeEbs(aws_region)
    ebs.nuke(older_than_seconds=time.time())
    ebs_list = client.describe_volumes()["Volumes"]
    assert len(ebs_list) == 0
