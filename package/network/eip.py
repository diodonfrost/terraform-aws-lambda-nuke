# -*- coding: utf-8 -*-

"""Module deleting all aws eip."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeEip:
    """Abstract eip nuke in a class."""

    def __init__(self):
        """Initialize eip nuke."""
        self.ec2 = boto3.client("ec2")

        try:
            self.ec2.describe_addresses()
        except EndpointConnectionError:
            print("Eip resource is not available in this aws region")
            return

    def nuke(self):
        """Eip deleting function.

        Delete all eip
        """
        for eip in self.list_eips():
            try:
                self.ec2.release_address(AllocationId=eip)
                print("Nuke elastic ip {0}".format(eip))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_eips(self):
        """Eip list function.

        List all eip Id

        :yield Iterator[str]:
            Eip Id
        """
        response = self.ec2.describe_addresses()

        for eip in response["Addresses"]:
            yield eip["AllocationId"]
