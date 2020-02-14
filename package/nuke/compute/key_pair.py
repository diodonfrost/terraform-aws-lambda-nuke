# -*- coding: utf-8 -*-

"""Module deleting all keypairs."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeKeypair:
    """Abstract key pair nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize key pair nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def nuke(self) -> None:
        """Keypair deleting function.

        Deleting all Keypair
        """
        for keypair in self.list_keypair():
            try:
                self.ec2.delete_key_pair(KeyName=keypair)
                print("Nuke Key Pair {0}".format(keypair))
            except ClientError as exc:
                nuke_exceptions("keypair", keypair, exc)

    def list_keypair(self) -> Iterator[str]:
        """Keypair list function.

         List all keypair names

        :yield Iterator[str]:
            Key pair name
        """
        response = self.ec2.describe_key_pairs()

        for keypair in response["KeyPairs"]:
            yield keypair["KeyName"]
