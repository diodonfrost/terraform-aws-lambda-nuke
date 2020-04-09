# -*- coding: utf-8 -*-

"""Module deleting all security groups."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeSecurityGroup:
    """Abstract security group nuke in a class."""

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
                self.revoke_all_rules_in_security_group(sec_grp)
            except ClientError as exc:
                nuke_exceptions("security group rule", sec_grp, exc)

        for sec_grp in self.list_security_groups():
            try:
                self.ec2.delete_security_group(GroupId=sec_grp)
                print("Nuke ec2 security group {0}".format(sec_grp))
            except ClientError as exc:
                nuke_exceptions("security group", sec_grp, exc)

    def revoke_all_rules_in_security_group(self, security_group_id) -> None:
        """Revoke all rules in specific security group.

        :param str security_group_id:
            The security group to apply this rule to.
        """
        sg_desc = self.ec2.describe_security_groups(
            GroupIds=[security_group_id]
        )
        try:
            self.ec2.revoke_security_group_egress(
                GroupId=security_group_id,
                IpPermissions=sg_desc["SecurityGroups"][0]["IpPermissions"],
            )
            self.ec2.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=sg_desc["SecurityGroups"][0][
                    "IpPermissionsEgress"
                ],
            )
        except ClientError as exc:
            nuke_exceptions("security group rule", security_group_id, exc)

    def list_security_groups(self) -> Iterator[str]:
        """Security groups list function.

        :yield Iterator[str]:
            Security group Id
        """
        paginator = self.ec2.get_paginator("describe_security_groups")

        for page in paginator.paginate():
            for security_group in page["SecurityGroups"]:
                yield security_group["GroupId"]
