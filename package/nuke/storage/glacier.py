# -*- coding: utf-8 -*-

"""Module deleting all aws Glacier resources."""

import datetime
from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeGlacier:
    """Abstract glacier nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize glacier nuke."""
        self.glacier = AwsClient().connect("glacier", region_name)

        try:
            self.glacier.list_vaults()
        except EndpointConnectionError:
            print("Glacier resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Glacier deleting function.

        Deleting all Glacier vaults with a timestamp greater than older_than_seconds
        and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Glacier
            vaults to exclude from deletion
        """
        for vault in self.list_vaults(older_than_seconds, required_tags):
            try:
                self.glacier.delete_vault(vaultName=vault)
                print("Nuke glacier vault {0}".format(vault))
            except ClientError as exc:
                nuke_exceptions("glacier vault", vault, exc)

    def list_vaults(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Glacier vault list function.

        List the names of all Glacier vaults with a timestamp lower
        than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter Glacier vaults
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the Glacier
            vaults to exclude from deletion

        :yield Iterator[str]:
            Glacier vault names
        """
        paginator = self.glacier.get_paginator("list_vaults")

        for page in paginator.paginate():
            for vault in page["VaultList"]:
                creation_date = datetime.datetime.strptime(
                    vault["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if creation_date.timestamp() < time_delete:
                    if required_tags and self._vault_has_required_tags(vault["VaultName"], required_tags):
                        continue
                    yield vault["VaultName"]

    def _vault_has_required_tags(self, vault_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Glacier vault has the required tags.

        :param str vault_name:
            The name of the Glacier vault
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the Glacier vault has all the required tags, False otherwise
        """
        try:
            tags = self.glacier.list_tags_for_vault(vaultName=vault_name)
            tags_dict = {tag['Key']: tag['Value'] for tag in tags['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for Glacier vault {vault_name}: {e}")
            return False