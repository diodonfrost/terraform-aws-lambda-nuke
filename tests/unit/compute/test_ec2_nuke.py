# -*- coding: utf-8 -*-
"""Tests for the ec2 nuke class."""

import boto3
import time

from moto import mock_ec2

from package.nuke.compute.ec2 import NukeEc2

from .utils import create_instances

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, {'Code': 48, 'Name': 'terminated'}),
        ("eu-west-2", time.time() + 43200, {'Code': 48, 'Name': 'terminated'}),
        ("eu-west-2", 630720000, {'Code': 16, 'Name': 'running'}),
    ]
)
@mock_ec2
def test_ec2_nuke(aws_region, older_than_seconds, result_count):
    """Verify instances nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_instances(count=3, region_name=aws_region)
    ec2 = NukeEc2(aws_region)
    ec2.nuke_instances(time_delete=older_than_seconds)
    ec2_list = client.describe_instances()["Reservations"][0]["Instances"]
    for instance in ec2_list:
        assert instance["State"] == result_count
