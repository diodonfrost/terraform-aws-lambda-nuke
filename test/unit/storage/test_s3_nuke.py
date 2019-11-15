"""Tests for the s3 nuke class."""

import boto3
import time

from moto import mock_s3

from package.storage.s3 import NukeS3

from .utils import create_s3

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_s3
def test_s3_nuke(aws_region, older_than_seconds, result_count):
    """Verify s3 nuke function."""
    client = boto3.client("s3", region_name=aws_region)

    create_s3(region_name=aws_region)
    s3 = NukeS3(aws_region)
    s3.nuke(older_than_seconds=older_than_seconds)
    s3_list = client.list_buckets()["Buckets"]
    assert len(s3_list) == result_count
