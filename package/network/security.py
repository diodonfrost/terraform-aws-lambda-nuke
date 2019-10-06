# -*- coding: utf-8 -*-

"""Module deleting all security group and network acl."""

import logging

import boto3

from botocore.exceptions import ClientError


class NukeNetworksecurity:
    """Abstract endpoint nuke in a class."""

    def __init__(self):
        """Initialize endpoint nuke."""
        self.ec2 = boto3.client("ec2")

    def nuke(self):
        """Security groups delete function."""
        for sec_grp in self.list_security_groups():
            try:
                self.ec2.delete_security_group(GroupId=sec_grp)
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

        for net_acl in self.list_network_acls():
            try:
                self.ec2.delete_network_acl(NetworkAclId=net_acl)
                print("Nuke ec2 network acl {0}".format(net_acl))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidParameterValue":
                    logging.info("network acl %s cannot be deleted", net_acl)
                else:
                    logging.error("Unexpected error: %s", e)

    def list_security_groups(self):
        """Security groups list function.

        :yield Iterator[str]:
            Security group Id
        """
        paginator = self.ec2.get_paginator("describe_security_groups")

        for page in paginator.paginate():
            for security_group in page["SecurityGroups"]:
                yield security_group["GroupId"]

    def list_network_acls(self):
        """Network acl list function.

        :yield Iterator[str]:
            Network acl Id
        """
        response = self.ec2.describe_network_acls()

        for network_acl in response["NetworkAcls"]:
            yield network_acl["NetworkAclId"]
