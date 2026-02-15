# -*- coding: utf-8 -*-
"""Tests for the ami nuke class."""

import time

import boto3
import pytest
from moto import mock_aws

from package.nuke.compute.ami import NukeAmi

from .utils import create_ami


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count",
    [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ],
)
@mock_aws
def test_ebs_nuke(aws_region, older_than_seconds, result_count):
    """Verify ami nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_ami(region_name=aws_region)
    ami = NukeAmi(aws_region)
    ami.nuke(older_than_seconds=older_than_seconds)
    ami_list = client.describe_images(Owners=["self"])["Images"]
    assert len(ami_list) == result_count
