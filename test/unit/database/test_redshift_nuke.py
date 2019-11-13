"""Tests for the redshift nuke class."""

import boto3
import time

from moto import mock_redshift

from package.database.redshift import NukeRedshift

from .utils import create_redshift


@mock_redshift
def test_redshift_nuke():
    """Verify redshift nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("redshift", region_name=aws_region)

    create_redshift(region_name=aws_region)
    redshift = NukeRedshift(aws_region)
    redshift.nuke(older_than_seconds=time.time() + 86400)
    redshift_list = client.describe_clusters()["Clusters"]
    assert len(redshift_list) == 0
