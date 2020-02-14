# -*- coding: utf-8 -*-

"""Module deleting all aws eip."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.exceptions import nuke_exceptions


class NukeEip:
    """Abstract eip nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize eip nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

        try:
            self.ec2.describe_addresses()
        except EndpointConnectionError:
            print("Eip resource is not available in this aws region")
            return

    def nuke(self) -> None:
        """Eip deleting function.

        Delete all eip
        """
        for eip in self.list_eips():
            try:
                self.ec2.release_address(AllocationId=eip)
                print("Nuke elastic ip {0}".format(eip))
            except ClientError as exc:
                nuke_exceptions("eip", eip, exc)

    def list_eips(self) -> Iterator[str]:
        """Eip list function.

        List all eip Id

        :yield Iterator[str]:
            Eip Id
        """
        response = self.ec2.describe_addresses()

        for eip in response["Addresses"]:
            yield eip["AllocationId"]
