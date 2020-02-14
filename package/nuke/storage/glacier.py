# -*- coding: utf-8 -*-

"""Module deleting all aws Glacier resources."""

import datetime
from typing import Iterator

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.exceptions import nuke_exceptions


class NukeGlacier:
    """Abstract glacier nuke in a class."""

    def __init__(self, region_name=None) -> None:
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

    def nuke(self, older_than_seconds) -> None:
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
            except ClientError as exc:
                nuke_exceptions("glacier vault", vault, exc)

    def list_vaults(self, time_delete: float) -> Iterator[str]:
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
