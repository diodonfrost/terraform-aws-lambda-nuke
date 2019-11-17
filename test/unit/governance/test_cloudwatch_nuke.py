"""Tests for the cloudwatch nuke class."""

import boto3
import time

from moto import mock_cloudwatch

from package.governance.cloudwatch import NukeCloudwatch

from .utils import create_cloudwatch_dashboard, create_cloudwatch_alarm

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_cloudwatch
def test_cloudwatch_dashboard_nuke(aws_region, older_than_seconds, result_count):
    """Verify cloudwatch dashboard nuke function."""
    client = boto3.client("cloudwatch", region_name=aws_region)

    create_cloudwatch_dashboard(region_name=aws_region)
    cloudwatch = NukeCloudwatch(aws_region)
    cloudwatch.nuke(older_than_seconds)
    cloudwatch_dashboard_list = client.list_dashboards()["DashboardEntries"]
    assert len(cloudwatch_dashboard_list) == result_count


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_cloudwatch
def test_cloudwatch_alarm_nuke(aws_region, older_than_seconds, result_count):
    """Verify cloudwatch alarm nuke function."""
    client = boto3.client("cloudwatch", region_name=aws_region)

    create_cloudwatch_alarm(region_name=aws_region)
    cloudwatch = NukeCloudwatch(aws_region)
    cloudwatch.nuke(older_than_seconds)
    cloudwatch_list = client.describe_alarms()["MetricAlarms"]
    assert len(cloudwatch_list) == result_count
