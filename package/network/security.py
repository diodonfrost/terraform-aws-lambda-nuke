# -*- coding: utf-8 -*-

"""Module deleting all security group and network acl."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_network_security():
    """Security group and network acl deleting function."""
    # define connection
    ec2 = boto3.client("ec2")

    # Test if security_group services is present in current aws region
    try:
        ec2.describe_security_groups()
    except EndpointConnectionError:
        print("ec2 resource is not available in this aws region")
        return

    # List all ec2 security groups
    ec2_security_group_list = ec2_list_security_groups()

    # Nuke all ec2 security groups
    for sec_grp in ec2_security_group_list:

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

    # List all ec2 network acl
    ec2_network_acl_list = ec2_list_network_acls()

    # Nuke all ec2 network acl
    for net_acl in ec2_network_acl_list:

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
    # define connection
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_security_groups")
    page_iterator = paginator.paginate()

    # Initialize ec2 security group list
    ec2_security_group_list = []

    # Retrieve all ec2 security group Id
    for page in page_iterator:
        for security_group in page["SecurityGroups"]:

            ec2_security_group = security_group["GroupId"]
            ec2_security_group_list.insert(0, ec2_security_group)

    return ec2_security_group_list


def ec2_list_network_acls():
    """Network acl list function."""
    # define connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_network_acls()

    # Initialize ec2 network acl list
    ec2_network_acl_list = []

    # Retrieve all ec2 network acl Id
    for network_acl in response["NetworkAcls"]:

        ec2_network_acl = network_acl["NetworkAclId"]
        ec2_network_acl_list.insert(0, ec2_network_acl)

    return ec2_network_acl_list
