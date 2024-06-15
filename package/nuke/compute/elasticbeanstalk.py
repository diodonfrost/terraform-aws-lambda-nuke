# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Beanstalk resources."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeElasticbeanstalk:
    """Initialize elasticbeanstalk nuke."""

    def __init__(self, region_name=None) -> None:
        """Initialize elasticbeanstalk nuke."""
        self.elasticbeanstalk = AwsClient().connect("elasticbeanstalk", region_name)

        try:
            self.elasticbeanstalk.describe_applications()
        except EndpointConnectionError:
            print("elasticbeanstalk resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Elastic Beanstalk deleting function.

        Deleting all Elastic Beanstalk applications and environments with a timestamp greater than older_than_seconds
        and optionally matching required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the applications/environments to exclude from deletion
        """
        for app_name in self.list_apps(older_than_seconds, required_tags):
            try:
                self.elasticbeanstalk.delete_application(ApplicationName=app_name, TerminateEnvByForce=True)
                print("Nuke elasticbeanstalk application {0}".format(app_name))
            except ClientError as exc:
                nuke_exceptions("elasticbeanstalk app", app_name, exc)

        for env_id in self.list_envs(older_than_seconds, required_tags):
            try:
                self.elasticbeanstalk.terminate_environment(EnvironmentId=env_id, ForceTerminate=True)
                print("Nuke elasticbeanstalk environment {0}".format(env_id))
            except ClientError as exc:
                nuke_exceptions("elasticbeanstalk env", env_id, exc)

    def list_apps(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Elastic Beanstalk Application list function.

        List the names of all Elastic Beanstalk Applications with a timestamp lower than time_delete
        and optionally matching required tags.

        :param int time_delete:
            Timestamp in seconds used for filter Elastic Beanstalk applications
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the applications to exclude from deletion

        :yield Iterator[str]:
            Elastic Beanstalk Application names
        """
        response = self.elasticbeanstalk.describe_applications()

        for app in response["Applications"]:
            if app["DateCreated"].timestamp() < time_delete:
                if required_tags and not self._app_has_required_tags(app["ApplicationName"], required_tags):
                    continue
                yield app["ApplicationName"]

    def list_envs(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Elastic Beanstalk Environment list function.

        List the IDs of all Elastic Beanstalk Environments with a timestamp lower than time_delete
        and optionally matching required tags.

        :param int time_delete:
            Timestamp in seconds used for filter Elastic Beanstalk environments
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the environments to exclude from deletion

        :yield Iterator[str]:
            Elastic Beanstalk Environment IDs
        """
        response = self.elasticbeanstalk.describe_environments()

        for env in response["Environments"]:
            if env["DateCreated"].timestamp() < time_delete:
                if required_tags and not self._env_has_required_tags(env["EnvironmentId"], required_tags):
                    continue
                yield env["EnvironmentId"]

    def _app_has_required_tags(self, app_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Elastic Beanstalk application has the required tags.

        :param str app_name:
            The name of the Elastic Beanstalk application
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the application has all the required tags, False otherwise
        """
        try:
            response = self.elasticbeanstalk.list_tags_for_resource(ResourceArn=app_name)
            tags = response["ResourceTags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Elastic Beanstalk app tagging", app_name, exc)
            return False

    def _env_has_required_tags(self, env_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Elastic Beanstalk environment has the required tags.

        :param str env_id:
            The ID of the Elastic Beanstalk environment
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the environment has all the required tags, False otherwise
        """
        try:
            response = self.elasticbeanstalk.list_tags_for_resource(ResourceArn=env_id)
            tags = response["ResourceTags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Elastic Beanstalk env tagging", env_id, exc)
            return False
