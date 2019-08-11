# -*- coding: utf-8 -*-

"""Module deleting all security group and network acl."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_network_security():
    """Security group and network acl deleting function."""
    ec2 = boto3.client("ec2")

    # Test if security_group services is present in current aws region
    try:
        ec2.describe_security_groups()
    except EndpointConnectionError:
        print("ec2 resource is not available in this aws region")
        return

    security_groups_nuke()
    network_acl_nuke()


def security_groups_nuke():
    """Security groups delete function."""
    ec2 = boto3.client("ec2")

    for sec_grp in ec2_list_security_groups():
        try:
            ec2.delete_security_group(GroupId=sec_grp)
            print("Nuke ec2 security group {0}".format(sec_grp))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "CannotDelete":
                logging.info("security grp %s cannot be deleted", sec_grp)
            elif error_code == "DependencyViolation":
                logging.info(
                    "security grp %s has a dependent object", sec_grp
                )
            else:
                logging.error("Unexpected error: %s", e)


def network_acl_nuke():
    """Network acl delete function."""
    ec2 = boto3.client("ec2")

    for net_acl in ec2_list_network_acls():
        try:
            ec2.delete_network_acl(NetworkAclId=net_acl)
            print("Nuke ec2 network acl {0}".format(net_acl))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidParameterValue":
                logging.info("network acl %s cannot be deleted", net_acl)
            else:
                logging.error("Unexpected error: %s", e)


def ec2_list_security_groups():
    """Security groups list function."""
    ec2_security_group_list = []
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_security_groups")

    for page in paginator.paginate():
        for security_group in page["SecurityGroups"]:
            ec2_security_group_list.append(security_group["GroupId"])
    return ec2_security_group_list


def ec2_list_network_acls():
    """Network acl list function."""
    ec2_network_acl_list = []
    ec2 = boto3.client("ec2")
    response = ec2.describe_network_acls()

    for network_acl in response["NetworkAcls"]:
        ec2_network_acl_list.append(network_acl["NetworkAclId"])
    return ec2_network_acl_list
