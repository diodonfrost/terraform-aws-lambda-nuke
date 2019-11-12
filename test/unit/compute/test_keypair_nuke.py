"""Tests for the keypair nuke class."""

import boto3
import time

from moto import mock_ec2

from package.compute.key_pair import NukeKeypair

from .utils import create_keypair

@mock_ec2
def test_keypair_nuke():
    """Verify keypair nuke class."""
    aws_region = "eu-west-1"
    client = boto3.client("ec2", region_name=aws_region)

    create_keypair(region_name=aws_region)
    keypair = NukeKeypair(aws_region)
    keypair.nuke()
    keypair_list = client.describe_key_pairs()["KeyPairs"]
    assert len(keypair_list) == 0
