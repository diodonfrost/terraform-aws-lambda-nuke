# -*- coding: utf-8 -*-
"""Tests for the emr nuke class."""

import boto3
import time

from moto import mock_emr

from package.nuke.analytic.emr import NukeEmr

from .utils import create_emr

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count",
    [
        ("eu-west-1", time.time() + 43200, "TERMINATED"),
        ("eu-west-2", time.time() + 43200, "TERMINATED"),
        ("eu-west-2", 630720000, "WAITING"),
    ],
)
@mock_emr
def test_emr_nuke(aws_region, older_than_seconds, result_count):
    """Verify emr nuke function."""
    client = boto3.client("emr", region_name=aws_region)

    create_emr(region_name=aws_region)
    emr = NukeEmr(aws_region)
    emr.nuke(older_than_seconds=older_than_seconds)
    emr_list = client.list_clusters()
    assert emr_list["Clusters"][0]["Status"]["State"] == result_count
