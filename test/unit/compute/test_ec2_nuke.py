"""Tests for the ec2 nuke class."""

import boto3
import time

from moto import mock_ec2

from package.compute.ec2 import NukeEc2

from .utils import create_instances


@mock_ec2
def test_ec2_nuke():
    """Verify instances nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_instances(count=3, region_name=aws_region)
    ec2 = NukeEc2(aws_region)
    ec2.nuke_instances(time_delete=time.time())
    ec2_list = client.describe_instances()["Reservations"][0]["Instances"]
    for instance in ec2_list:
        assert instance["State"] == {'Code': 48, 'Name': 'terminated'}
