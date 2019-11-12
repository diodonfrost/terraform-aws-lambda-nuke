"""Tests for the elb nuke class."""

import boto3
import time

from moto import mock_elb, mock_elbv2, mock_ec2

from package.compute.elb import NukeElb

from .utils import create_elb

@mock_ec2
@mock_elb
@mock_elbv2
def test_elb_nuke():
    """Verify elb nuke class."""
    aws_region = "eu-west-1"
    elb = boto3.client("elb", region_name=aws_region)
    elbv2 = boto3.client("elbv2", region_name=aws_region)

    create_elb(region_name=aws_region)
    lb = NukeElb(aws_region)
    lb.nuke(older_than_seconds=time.time())
    elb_list = elb.describe_load_balancers()["LoadBalancerDescriptions"]
    elbv2_list = elbv2.describe_load_balancers()["LoadBalancers"]
    assert len(elb_list) == 0
    assert len(elbv2_list) == 0
