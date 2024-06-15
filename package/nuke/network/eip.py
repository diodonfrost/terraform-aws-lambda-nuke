# -*- coding: utf-8 -*-

"""Module deleting all aws eip."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEip:
    """Abstract eip nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize eip nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

        try:
            self.ec2.describe_addresses()
        except EndpointConnectionError:
            print("Eip resource is not available in this aws region")
            return

    def nuke(self, required_tags: Dict[str, str] = None) -> None:
        """Eip deleting function.

        Delete all eip except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EIPs
            to exclude from deletion
        """
        for eip in self.list_eips(required_tags):
            try:
                self.ec2.release_address(AllocationId=eip)
                print("Nuke elastic ip {0}".format(eip))
            except ClientError as exc:
                nuke_exceptions("eip", eip, exc)

    def list_eips(self, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Eip list function.

        List all eip Id except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EIPs
            to exclude from deletion

        :yield Iterator[str]:
            Eip Id
        """
        response = self.ec2.describe_addresses()

        for eip in response["Addresses"]:
            if required_tags and self._eip_has_required_tags(eip, required_tags):
                continue
            yield eip["AllocationId"]

    def _eip_has_required_tags(self, eip: dict, required_tags: Dict[str, str]) -> bool:
        """Check if the EIP has the required tags.

        :param dict eip:
            The EIP dictionary object from describe_addresses response
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the EIP has all the required tags, False otherwise
        """
        if 'Tags' in eip:
            tags_dict = {tag['Key']: tag['Value'] for tag in eip['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        return False

if __name__ == "__main__":
    nuke_eip = NukeEip(region_name="ap-south-1")
    nuke_eip.nuke(required_tags={"Environment": "develop"})
