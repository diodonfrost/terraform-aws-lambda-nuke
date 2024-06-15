# -*- coding: utf-8 -*-

"""Module deleting all keypairs."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeKeypair:
    """Abstract key pair nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize key pair nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, required_tags: Dict[str, str] = None) -> None:
        """Keypair deleting function.

        Deleting all Keypair except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the key pairs
            to exclude from deletion
        """
        for keypair in self.list_keypairs(required_tags):
            try:
                self.ec2.delete_key_pair(KeyName=keypair)
                print("Nuke Key Pair {0}".format(keypair))
            except ClientError as exc:
                nuke_exceptions("keypair", keypair, exc)

    def list_keypairs(self, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Keypair list function.

        List all keypair names except those matching the required tags.

        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the key pairs
            to exclude from deletion

        :yield Iterator[str]:
            Key pair name
        """
        response = self.ec2.describe_key_pairs()

        for keypair in response["KeyPairs"]:
            if required_tags and self._keypair_has_required_tags(keypair, required_tags):
                continue
            yield keypair["KeyName"]

    def _keypair_has_required_tags(self, keypair: dict, required_tags: Dict[str, str]) -> bool:
        """Check if the key pair has the required tags.

        :param dict keypair:
            The key pair dictionary object from describe_key_pairs response
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the key pair has all the required tags, False otherwise
        """
        if 'Tags' in keypair:
            tags_dict = {tag['Key']: tag['Value'] for tag in keypair['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        return False
