# -*- coding: utf-8 -*-
"""Tests for the keypair nuke class."""

import boto3
import time

from moto import mock_ec2

from package.nuke.compute.key_pair import NukeKeypair

from .utils import create_keypair

import pytest


@pytest.mark.parametrize(
    "aws_region, result_count", [
        ("eu-west-1", 0),
        ("eu-west-2", 0),
    ]
)
@mock_ec2
def test_keypair_nuke(aws_region, result_count):
    """Verify keypair nuke class."""
    client = boto3.client("ec2", region_name=aws_region)

    create_keypair(region_name=aws_region)
    keypair = NukeKeypair(aws_region)
    keypair.nuke()
    keypair_list = client.describe_key_pairs()["KeyPairs"]
    assert len(keypair_list) == result_count
