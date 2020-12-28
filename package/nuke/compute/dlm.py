# -*- coding: utf-8 -*-

"""Module deleting all aws dlm policie resources."""

from typing import Iterator

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeDlm:
    """Abstract dlm nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize dlm nuke."""
        self.dlm = AwsClient().connect("dlm", region_name)

        try:
            self.dlm.get_lifecycle_policies()
        except EndpointConnectionError:
            print("Dlm resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
        """Dlm policies deleting function.

        Deleting all dlm policy resources with a timestamp greater
        than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for policy in self.list_policy(older_than_seconds):
            try:
                self.dlm.delete_lifecycle_policy(PolicyId=policy)
                print("Nuke dlm Lifecycle Policy {0}".format(policy))
            except ClientError as exc:
                nuke_exceptions("dlm policy", policy, exc)

    def list_policy(self, time_delete: float) -> Iterator[str]:
        """Data Lifecycle Policies list function.

        Returns the IDs of all Data Lifecycle Policies with
        a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Data Lifecycle policies

        :yield Iterator[str]:
            Data Lifecycle policies IDs
        """
        response = self.dlm.get_lifecycle_policies()

        for policy in response["Policies"]:
            detailed = self.dlm.get_lifecycle_policy(
                PolicyId=policy["PolicyId"]
            )
            if detailed["Policy"]["DateCreated"].timestamp() < time_delete:
                yield policy["PolicyId"]
