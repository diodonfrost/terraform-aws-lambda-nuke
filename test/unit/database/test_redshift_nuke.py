"""Tests for the redshift nuke class."""

import boto3
import time

from moto import mock_redshift

from package.database.redshift import NukeRedshift

from .utils import create_redshift

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_redshift
def test_redshift_nuke(aws_region, older_than_seconds, result_count):
    """Verify redshift nuke function."""
    client = boto3.client("redshift", region_name=aws_region)

    create_redshift(region_name=aws_region)
    redshift = NukeRedshift(aws_region)
    redshift.nuke(older_than_seconds=older_than_seconds)
    redshift_list = client.describe_clusters()["Clusters"]
    assert len(redshift_list) == result_count
