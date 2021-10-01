# -*- coding: utf-8 -*-
"""Tests for the security nuke class."""

import boto3

from moto import mock_ec2

from package.nuke.network.security_group import NukeSecurityGroup

from .utils import create_security_group

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

    create_security_group(region_name=aws_region)
    security = NukeSecurityGroup(aws_region)
    security.nuke()
    security_group_list = client.describe_security_groups()["SecurityGroups"]
    assert len(security_group_list) == result_count
