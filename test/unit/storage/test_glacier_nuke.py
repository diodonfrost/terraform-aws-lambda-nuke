"""Tests for the glacier nuke class."""

import boto3
import time

from moto import mock_glacier

from package.storage.glacier import NukeGlacier

from .utils import create_glacier


@mock_glacier
def test_glacier_nuke():
    """Verify glacier nuke function."""
    aws_region = "eu-west-1"
    client = boto3.client("glacier", region_name=aws_region)

    create_glacier(region_name=aws_region)
    glacier = NukeGlacier(aws_region)
    glacier.nuke(older_than_seconds=time.time())
    glacier_list = client.list_vaults()["VaultList"]
    assert len(glacier_list) == 0
