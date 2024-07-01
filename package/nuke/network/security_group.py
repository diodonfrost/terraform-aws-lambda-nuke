# -*- coding: utf-8 -*-

"""Module deleting all security groups."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeSecurityGroup:
    """Abstract security group nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize endpoint nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, required_tags: Dict[str, str] = None) -> None:
        """Security groups delete function.

        Deletes all security groups except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the security groups
            to exclude from deletion
        """
        for sec_grp in self.list_security_groups(required_tags):
            try:
                self.revoke_all_rules_in_security_group(sec_grp)
            except ClientError as exc:
                nuke_exceptions("security group rule", sec_grp, exc)

        for sec_grp in self.list_security_groups(required_tags):
            try:
                self.ec2.delete_security_group(GroupId=sec_grp)
                print("Nuke ec2 security group {0}".format(sec_grp))
            except ClientError as exc:
                nuke_exceptions("security group", sec_grp, exc)

    def revoke_all_rules_in_security_group(self, security_group_id) -> None:
        """Revoke all egress rules in a specific security group.

        :param str security_group_id:
            The security group to revoke egress rules from.
        """
        sg_desc = self.ec2.describe_security_groups(
            GroupIds=[security_group_id]
        )
        try:
            if 'IpPermissionsEgress' in sg_desc['SecurityGroups'][0]:
                self.ec2.revoke_security_group_egress(
                    GroupId=security_group_id,
                    IpPermissions=[],  # Empty list since we're only revoking egress
                    SecurityGroupRuleIds=[  # Fetching all egress rule IDs
                        rule['GroupId'] for rule in sg_desc['SecurityGroups'][0]['IpPermissionsEgress']
                    ],
                )
        except ClientError as exc:
            nuke_exceptions("security group rule", security_group_id, exc)

    def list_security_groups(self, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Security groups list function.

        List all security group IDs except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the security groups
            to exclude from deletion

        :yield Iterator[str]:
            Security group ID
        """
        paginator = self.ec2.get_paginator("describe_security_groups")

        for page in paginator.paginate():
            for security_group in page["SecurityGroups"]:
                if required_tags and not self._security_group_has_required_tags(security_group, required_tags):
                    continue
                yield security_group["GroupId"]

    def _security_group_has_required_tags(self, security_group: dict, required_tags: Dict[str, str]) -> bool:
        """Check if the security group has the required tags.

        :param dict security_group:
            The security group dictionary object from describe_security_groups response
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the security group has all the required tags, False otherwise
        """
        if 'Tags' in security_group:
            tags_dict = {tag['Key']: tag['Value'] for tag in security_group['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        return False

# Additional imports and setup might be required based on your actual implementation context.
# Ensure you have necessary imports and configurations from `nuke.client_connections` and `nuke.exceptions`.
