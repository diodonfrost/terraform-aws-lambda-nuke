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

    def nuke(self, required_tags_str: str = None) -> None:
        """Keypair deleting function.

        Deleting all Keypair except those matching the required tags.

        :param str required_tags_str:
            Comma-separated list of required tags in the format key=value

        """
        required_tags = self._parse_required_tags(required_tags_str)

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
            keypair_name = keypair["KeyName"]
            keypair_tags = self._get_keypair_tags(keypair)

            print(f"Checking keypair: {keypair_name}")
            print(f"Tags for keypair: {keypair_tags}")
            print(f"Required tags: {required_tags}")

            if required_tags and self._keypair_has_required_tags(keypair_tags, required_tags):
                print(f"Skipping keypair {keypair_name} due to matching required tags.")
                continue
            yield keypair_name

    def _get_keypair_tags(self, keypair: dict) -> Dict[str, str]:
        """Get the tags for a specific key pair from the describe_key_pairs response."""
        try:
            response = self.ec2.describe_tags(
                Filters=[
                    {"Name": "resource-id", "Values": [keypair["KeyName"]]},
                    {"Name": "resource-type", "Values": ["key-pair"]}
                ]
            )
            tags = {tag['Key']: tag['Value'] for tag in response.get('Tags', [])}
            return tags
        except ClientError as exc:
            print(f"Failed to describe tags for keypair {keypair['KeyName']}: {str(exc)}")
            return {}

    def _keypair_has_required_tags(self, keypair_tags: Dict[str, str], required_tags: Dict[str, str]) -> bool:
        """Check if the key pair has the required tags."""
        for key, value in required_tags.items():
            if keypair_tags.get(key) != value:
                return False
        return True

    def _parse_required_tags(self, required_tags_str: str) -> Dict[str, str]:
        """Parse the required tags string into a dictionary.

        :param str required_tags_str:
            Comma-separated list of required tags in the format key=value

        :return dict:
            Dictionary of required tags
        """
        tags = {}
        if required_tags_str:
            for tag in required_tags_str.split(','):
                key, value = tag.split('=')
                tags[key.strip()] = value.strip()
        return tags
