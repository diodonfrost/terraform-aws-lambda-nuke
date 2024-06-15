# -*- coding: utf-8 -*-

"""Module deleting all network acl."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeNetworkAcl:
    """Abstract network acl nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize endpoint nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, required_tags: Dict[str, str] = None) -> None:
        """Network acl delete function.

        Deletes all network ACLs except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the network ACLs
            to exclude from deletion
        """
        for net_acl in self.list_network_acls(required_tags):
            try:
                self.ec2.delete_network_acl(NetworkAclId=net_acl)
                print("Nuke ec2 network acl {0}".format(net_acl))
            except ClientError as exc:
                nuke_exceptions("network acl", net_acl, exc)

    def list_network_acls(self, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Network acl list function.

        List all network ACL IDs except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the network ACLs
            to exclude from deletion

        :yield Iterator[str]:
            Network ACL ID
        """
        response = self.ec2.describe_network_acls()

        for network_acl in response["NetworkAcls"]:
            if required_tags and not self._network_acl_has_required_tags(network_acl, required_tags):
                continue
            yield network_acl["NetworkAclId"]

    def _network_acl_has_required_tags(self, network_acl: dict, required_tags: Dict[str, str]) -> bool:
        """Check if the network ACL has the required tags.

        :param dict network_acl:
            The network ACL dictionary object from describe_network_acls response
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the network ACL has all the required tags, False otherwise
        """
        if 'Tags' in network_acl:
            tags_dict = {tag['Key']: tag['Value'] for tag in network_acl['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        return False
