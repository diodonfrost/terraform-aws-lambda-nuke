"""Module use by nuke unit tests."""

import boto3


def create_eip(region_name):
    """Create eip."""
    client = boto3.client("ec2", region_name=region_name)
    client.allocate_address(Domain="vpc", Address="127.38.43.222")


def create_security(region_name):
    """Create security group and network acl."""
    client = boto3.client("ec2", region_name=region_name)

    client.create_security_group(GroupName="sg-test", Description="sg test")
    client.create_network_acl(VpcId=client.describe_vpcs()["Vpcs"][0]["VpcId"])
