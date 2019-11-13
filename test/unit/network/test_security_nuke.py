"""Tests for the security nuke class."""

import boto3

from moto import mock_ec2

from package.network.security import NukeNetworksecurity

from .utils import create_security


@mock_ec2
def test_security_nuke():
    """Verify security nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_security(region_name=aws_region)
    security = NukeNetworksecurity(aws_region)
    security.nuke()
    security_group_list = client.describe_security_groups()["SecurityGroups"]
    network_acl_list = client.describe_network_acls()["NetworkAcls"]
    assert len(security_group_list) == 0
    assert len(network_acl_list) == 0
