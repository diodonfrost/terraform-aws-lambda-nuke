# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Beanstalk resources."""

from typing import Iterator

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeElasticbeanstalk:
    """Initialize elasticbeanstalk nuke."""

    def __init__(self, region_name=None) -> None:
        """Initialize elasticbeanstalk nuke."""
        self.elasticbeanstalk = AwsClient().connect(
            "elasticbeanstalk", region_name
        )

        try:
            self.elasticbeanstalk.describe_applications()
        except EndpointConnectionError:
            print(
                "elasticbeanstalk resource is not available in this aws region"
            )
            return

    def nuke(self, older_than_seconds: float) -> None:
        """Elastic Beanstalk deleting function.

        Deleting all Elastic Beanstalk with a timestamp greater than
        older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for app in self.list_apps(older_than_seconds):
            try:
                self.elasticbeanstalk.delete_application(
                    ApplicationName=app, TerminateEnvByForce=True
                )
                print("Nuke elasticbeanstalk application{0}".format(app))
            except ClientError as exc:
                nuke_exceptions("elasticbenstalk app", app, exc)

        for env in self.list_envs(older_than_seconds):
            try:
                self.elasticbeanstalk.terminate_environment(
                    EnvironmentId=env, ForceTerminate=True
                )
                print("Nuke elasticbeanstalk environment {0}".format(env))
            except ClientError as exc:
                nuke_exceptions("elasticbenstalk env", env, exc)

    def list_apps(self, time_delete: float) -> Iterator[str]:
        """Elastic Beanstalk Application list function.

        List the names of all Elastic Beanstalk Applications.

        :yield Iterator[str]:
            Elastic Beanstalk Application names
        """
        response = self.elasticbeanstalk.describe_applications()

        for app in response["Applications"]:
            if app["DateCreated"].timestamp() < time_delete:
                yield app["ApplicationName"]

    def list_envs(self, time_delete: float) -> Iterator[str]:
        """Elastic Beanstalk Environment list function.

        List the IDs of all Elastic Beanstalk Environments.

        :yield Iterator[str]:
            Elastic Beanstalk Environment IDs
        """
        response = self.elasticbeanstalk.describe_environments()

        for env in response["Environments"]:
            if env["DateCreated"].timestamp() < time_delete:
                yield env["EnvironmentId"]
