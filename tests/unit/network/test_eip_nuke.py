"""Tests for the eip nuke class."""

import boto3

from moto import mock_ec2

from package.nuke.network.eip import NukeEip

from .utils import create_eip

import pytest


@pytest.mark.parametrize(
    "aws_region, result_count", [
        ("eu-west-1", 0),
        ("eu-west-2", 0),
    ]
)
@mock_ec2
def test_eip_nuke(aws_region, result_count):
    """Verify eip nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_eip(region_name=aws_region)
    eip = NukeEip(aws_region)
    eip.nuke()
    eip_list = client.describe_addresses()["Addresses"]
    assert len(eip_list) == result_count
