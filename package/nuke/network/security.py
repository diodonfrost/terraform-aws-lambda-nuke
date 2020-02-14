# -*- coding: utf-8 -*-

"""Module deleting all security group and network acl."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeNetworksecurity:
    """Abstract endpoint nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize endpoint nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def nuke(self) -> None:
        """Security groups delete function."""
        for sec_grp in self.list_security_groups():
            try:
                self.ec2.delete_security_group(GroupId=sec_grp)
                print("Nuke ec2 security group {0}".format(sec_grp))
            except ClientError as exc:
                nuke_exceptions("security group", sec_grp, exc)

        for net_acl in self.list_network_acls():
            try:
                self.ec2.delete_network_acl(NetworkAclId=net_acl)
                print("Nuke ec2 network acl {0}".format(net_acl))
            except ClientError as exc:
                nuke_exceptions("network acl", net_acl, exc)

    def list_security_groups(self) -> Iterator[str]:
        """Security groups list function.

        :yield Iterator[str]:
            Security group Id
        """
        paginator = self.ec2.get_paginator("describe_security_groups")

        for page in paginator.paginate():
            for security_group in page["SecurityGroups"]:
                yield security_group["GroupId"]

    def list_network_acls(self) -> Iterator[str]:
        """Network acl list function.

        :yield Iterator[str]:
            Network acl Id
        """
        response = self.ec2.describe_network_acls()

        for network_acl in response["NetworkAcls"]:
            yield network_acl["NetworkAclId"]
