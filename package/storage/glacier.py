# -*- coding: utf-8 -*-

"""Module deleting all aws Glacier resources."""

import datetime
import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeGlacier:
    """Abstract glacier nuke in a class."""

    def __init__(self, region_name=None):
        """Initialize glacier nuke."""
        if region_name:
            self.glacier = boto3.client("glacier", region_name=region_name)
        else:
            self.glacier = boto3.client("glacier")

        try:
            self.glacier.list_vaults()
        except EndpointConnectionError:
            print("Glacier resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """Glacier deleting function.

        Deleting all Glacier with a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for vault in self.list_vaults(older_than_seconds):
            try:
                self.glacier.delete_vault(vaultName=vault)
                print("Nuke glacier vault {0}".format(vault))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_vaults(self, time_delete):
        """Glacier vault list function.

        List the names of all Glacier vaults with a timestamp lower
        than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Glacier vaults

        :yield Iterator[str]:
            Glacier vaults names
        """
        paginator = self.glacier.get_paginator("list_vaults")

        for page in paginator.paginate():
            for vault in page["VaultList"]:
                creation_date = datetime.datetime.strptime(
                    vault["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if creation_date.timestamp() < time_delete:
                    yield vault["VaultName"]
