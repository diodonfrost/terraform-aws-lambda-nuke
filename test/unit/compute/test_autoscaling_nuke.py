"""Tests for the autoscaling group nuke class."""

import boto3
import time

from moto import mock_autoscaling, mock_ec2

from package.compute.autoscaling import NukeAutoscaling

from .utils import create_autoscaling


@mock_ec2
@mock_autoscaling
def test_autoscaling_nuke():
    """Verify autoscaling nuke class."""
    aws_region = "eu-west-1"
    client = boto3.client("autoscaling", region_name=aws_region)

    create_autoscaling(aws_region)
    asg = NukeAutoscaling(aws_region)
    asg.nuke(older_than_seconds=time.time())
    asg_list = client.describe_auto_scaling_groups()["AutoScalingGroups"]
    assert len(asg_list) == 0
