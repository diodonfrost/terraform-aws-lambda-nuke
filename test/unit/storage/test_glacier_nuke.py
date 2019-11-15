"""Tests for the glacier nuke class."""

import boto3
import time

from moto import mock_glacier

from package.storage.glacier import NukeGlacier

from .utils import create_glacier

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count",
    [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ],
)
@mock_glacier
def test_glacier_nuke(aws_region, older_than_seconds, result_count):
    """Verify glacier nuke function."""
    client = boto3.client("glacier", region_name=aws_region)

    create_glacier(region_name=aws_region)
    glacier = NukeGlacier(aws_region)
    glacier.nuke(older_than_seconds=older_than_seconds)
    glacier_list = client.list_vaults()["VaultList"]
    assert len(glacier_list) == result_count
