# -*- coding: utf-8 -*-

"""Module deleting all keypairs."""

import logging

import boto3

from botocore.exceptions import ClientError


class NukeKeypair:
    """Abstract key pair nuke in a class."""

    def __init__(self):
        """Initialize key pair nuke."""
        self.ec2 = boto3.client("ec2")

    def nuke(self):
        """Keypair deleting function.

        Deleting all Keypair
        """
        for keypair in self.list_keypair():
            try:
                self.ec2.delete_key_pair(KeyName=keypair)
                print("Nuke Key Pair {0}".format(keypair))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_keypair(self):
        """Keypair list function.

         List all keypair names

        :yield Iterator[str]:
            Key pair name
        """
        response = self.ec2.describe_key_pairs()

        for keypair in response["KeyPairs"]:
            yield keypair["KeyName"]
