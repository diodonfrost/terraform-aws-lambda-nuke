# -*- coding: utf-8 -*-

"""Module deleting all aws dlm policy resources."""

from typing import Iterator, Dict

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

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Dlm policies deleting function.

        Deleting all dlm policy resources with a timestamp greater
        than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the policies to exclude from deletion
        """
        for policy_id in self.list_policy(older_than_seconds, required_tags):
            try:
                self.dlm.delete_lifecycle_policy(PolicyId=policy_id)
                print("Nuke dlm Lifecycle Policy {0}".format(policy_id))
            except ClientError as exc:
                nuke_exceptions("dlm policy", policy_id, exc)

    def list_policy(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Data Lifecycle Policies list function.

        Returns the IDs of all Data Lifecycle Policies with
        a timestamp lower than time_delete and matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering Data Lifecycle policies
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the policies to exclude from deletion

        :yield Iterator[str]:
            Data Lifecycle policies IDs
        """
        response = self.dlm.get_lifecycle_policies()

        for policy in response["Policies"]:
            detailed = self.dlm.get_lifecycle_policy(PolicyId=policy["PolicyId"])
            if detailed["Policy"]["DateCreated"].timestamp() < time_delete:
                if required_tags and not self._policy_has_required_tags(policy["PolicyId"], required_tags):
                    continue
                yield policy["PolicyId"]

    def _policy_has_required_tags(self, policy_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the DLM policy has the required tags.

        :param str policy_id:
            The ID of the DLM policy
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the policy has all the required tags, False otherwise
        """
        try:
            response = self.dlm.list_tags_for_resource(ResourceArn=policy_id)
            tags = response["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("DLM policy tagging", policy_id, exc)
            return False
