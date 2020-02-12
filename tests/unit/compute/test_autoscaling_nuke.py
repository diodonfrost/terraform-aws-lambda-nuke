"""Tests for the autoscaling group nuke class."""

import boto3
import time

from moto import mock_autoscaling, mock_ec2

from package.nuke.compute.autoscaling import NukeAutoscaling

from .utils import create_autoscaling

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_ec2
@mock_autoscaling
def test_autoscaling_nuke(aws_region, older_than_seconds, result_count):
    """Verify autoscaling nuke class."""
    client = boto3.client("autoscaling", region_name=aws_region)

    create_autoscaling(aws_region)
    asg = NukeAutoscaling(aws_region)
    asg.nuke(older_than_seconds=older_than_seconds)
    asg_list = client.describe_auto_scaling_groups()["AutoScalingGroups"]
    assert len(asg_list) == result_count


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_ec2
@mock_autoscaling
def test_launch_conf_nuke(aws_region, older_than_seconds, result_count):
    """Verify launch configuration nuke function."""
    client = boto3.client("autoscaling", region_name=aws_region)

    create_autoscaling(aws_region)
    asg = NukeAutoscaling(aws_region)
    asg.nuke(older_than_seconds=older_than_seconds)
    launch_conf_list = client.describe_launch_configurations()["LaunchConfigurations"]
    assert len(launch_conf_list) == result_count
