"""Tests for the eip nuke class."""

import boto3

from moto import mock_ec2

from package.network.eip import NukeEip

from .utils import create_eip


@mock_ec2
def test_eip_nuke():
    """Verify eip nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_eip(region_name=aws_region)
    eip = NukeEip(aws_region)
    eip.nuke()
    eip_list = client.describe_addresses()["Addresses"]
    assert len(eip_list) == 0
