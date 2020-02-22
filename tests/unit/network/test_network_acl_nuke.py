"""Tests for the security nuke class."""

import boto3

from moto import mock_ec2

from package.nuke.network.network_acl import NukeNetworkAcl

from .utils import create_network_acl

import pytest


@pytest.mark.parametrize(
    "aws_region, result_count", [
        ("eu-west-1", 0),
        ("eu-west-2", 0),
    ]
)
@mock_ec2
def test_security_nuke(aws_region, result_count):
    """Verify security nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_network_acl(region_name=aws_region)
    security = NukeNetworkAcl(aws_region)
    security.nuke()
    network_acl_list = client.describe_network_acls()["NetworkAcls"]
    assert len(network_acl_list) == result_count
