# -*- coding: utf-8 -*-

"""Module deleting all aws Glacier resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeGlacier:
    """Abstract glacier nuke in a class."""

    def __init__(self):
        """Initialize glacier nuke."""
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

        :return list vault_list:
            List of Glacier vaults names
        """
        vault_list = []
        paginator = self.glacier.get_paginator("list_vaults")

        for page in paginator.paginate():
            for vault in page["VaultList"]:
                if vault["CreationDate"].timestamp() < time_delete:
                    vault_list.append(vault["VaultName"])
        return vault_list
