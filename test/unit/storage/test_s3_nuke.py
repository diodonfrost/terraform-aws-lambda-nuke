"""Tests for the s3 nuke class."""

import boto3
import time

from moto import mock_s3

from package.storage.s3 import NukeS3

from .utils import create_s3


@mock_s3
def test_s3_nuke():
    """Verify s3 nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("s3", region_name=aws_region)

    create_s3(region_name=aws_region)
    s3 = NukeS3(aws_region)
    s3.nuke(older_than_seconds=time.time())
    s3_list = client.list_buckets()["Buckets"]
    assert len(s3_list) == 0
