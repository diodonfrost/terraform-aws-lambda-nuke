# -*- coding: utf-8 -*-
"""Tests for the ebs nuke class."""

import boto3
import time

from moto import mock_ec2

from package.nuke.compute.ebs import NukeEbs

from .utils import create_ebs

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_ec2
def test_ebs_nuke(aws_region, older_than_seconds, result_count):
    """Verify ebs volume nuke function."""
    client = boto3.client("ec2", region_name=aws_region)

    create_ebs(region_name=aws_region)
    ebs = NukeEbs(aws_region)
    ebs.nuke(older_than_seconds=older_than_seconds)
    ebs_list = client.describe_volumes()["Volumes"]
    assert len(ebs_list) == result_count
