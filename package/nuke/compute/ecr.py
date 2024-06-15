# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Container Registry resources."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEcr:
    """Abstract ecr nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ecr nuke."""
        self.ecr = AwsClient().connect("ecr", region_name)

        try:
            self.ecr.describe_repositories()
        except EndpointConnectionError:
            print("ECR resource is not available in this AWS region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Elastic Container Registry deleting function.

        Deleting all Elastic Container Registry with a timestamp greater
        than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the AWS
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the ECR repositories to exclude from deletion
        """
        for registry in self.list_registry(older_than_seconds, required_tags):
            try:
                self.ecr.delete_repository(repositoryName=registry, force=True)
                print("Nuke ECR Registry {0}".format(registry))
            except ClientError as exc:
                nuke_exceptions("ECR registry", registry, exc)

    def list_registry(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Elastic Container Registry list function.

        List the names of all Elastic Container Registry with
        a timestamp lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering ECR
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the ECR repositories to exclude from deletion

        :yield Iterator[str]:
            Elastic Container Registry names
        """
        paginator = self.ecr.get_paginator("describe_repositories")

        for page in paginator.paginate():
            for registry in page["repositories"]:
                if registry["createdAt"].timestamp() < time_delete:
                    if required_tags and self._registry_has_required_tags(registry["repositoryName"], required_tags):
                        continue
                    yield registry["repositoryName"]

    def _registry_has_required_tags(self, registry_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the ECR repository has the required tags.

        :param str registry_name:
            The name of the ECR repository
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the ECR repository has all the required tags, False otherwise
        """
        try:
            response = self.ecr.list_tags_for_resource(resourceArn=f"arn:aws:ecr:{self.ecr.meta.region_name}:{self.ecr.meta.account_id}:repository/{registry_name}")
            repository_tags = {tag["Key"]: tag["Value"] for tag in response["tags"]}
            for key, value in required_tags.items():
                if repository_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("ECR registry tagging", registry_name, exc)
            return False
