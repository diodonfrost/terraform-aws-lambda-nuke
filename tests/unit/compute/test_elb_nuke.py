"""Tests for the elb nuke class."""

import boto3
import time

from moto import mock_elb, mock_elbv2, mock_ec2

from package.nuke.compute.elb import NukeElb

from .utils import create_elb, create_elbv2

import pytest


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_ec2
@mock_elb
@mock_elbv2
def test_elb_nuke(aws_region, older_than_seconds, result_count):
    """Verify elb nuke function."""
    elb = boto3.client("elb", region_name=aws_region)

    create_elb(region_name=aws_region)
    lb = NukeElb(aws_region)
    lb.nuke(older_than_seconds=older_than_seconds)
    elb_list = elb.describe_load_balancers()["LoadBalancerDescriptions"]
    assert len(elb_list) == result_count


@pytest.mark.parametrize(
    "aws_region, older_than_seconds, result_count", [
        ("eu-west-1", time.time() + 43200, 0),
        ("eu-west-2", time.time() + 43200, 0),
        ("eu-west-2", 630720000, 1),
    ]
)
@mock_ec2
@mock_elb
@mock_elbv2
def test_elbv2_nuke(aws_region, older_than_seconds, result_count):
    """Verify elbv2 nuke function."""
    elbv2 = boto3.client("elbv2", region_name=aws_region)

    create_elbv2(region_name=aws_region)
    lb = NukeElb(aws_region)
    lb.nuke(older_than_seconds=older_than_seconds)
    elbv2_list = elbv2.describe_load_balancers()["LoadBalancers"]
    assert len(elbv2_list) == result_count
