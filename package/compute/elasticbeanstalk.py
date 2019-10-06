# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Beanstalk resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeElasticbeanstalk:
    """Initialize elasticbeanstalk nuke."""

    def __init__(self):
        """Initialize elasticbeanstalk nuke."""
        self.elasticbeanstalk = boto3.client("elasticbeanstalk")

        try:
            self.elasticbeanstalk.describe_applications()
        except EndpointConnectionError:
            print(
                "elasticbeanstalk resource is not available in this aws region"
            )
            return

    def nuke(self, older_than_seconds):
        """Elastic Beanstalk deleting function.

        Deleting all Elastic Beanstalk with a timestamp greater than
        older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for app in self.list_apps(older_than_seconds):
            if app["DateCreated"].timestamp() < older_than_seconds:
                try:
                    self.elasticbeanstalk.delete_application(
                        ApplicationName=app, TerminateEnvByForce=True
                    )
                    print("Nuke elasticbeanstalk application{0}".format(app))
                except ClientError as e:
                    logging.error("Unexpected error: %s", e)

        for env in self.list_envs(older_than_seconds):
            if env["DateCreated"].timestamp() < older_than_seconds:
                try:
                    self.elasticbeanstalk.terminate_environment(
                        EnvironmentId=env, ForceTerminate=True
                    )
                    print("Nuke elasticbeanstalk environment {0}".format(env))
                except ClientError as e:
                    logging.error("Unexpected error: %s", e)

    def list_apps(self, time_delete):
        """Elastic Beanstalk Application list function.

        List the names of all Elastic Beanstalk Applications.

        :yield Iterator[str]:
            Elastic Beanstalk Application names
        """
        response = self.elasticbeanstalk.describe_applications()

        for app in response["Applications"]:
            if app["DateCreated"].timestamp() < time_delete:
                yield app["ApplicationName"]

    def list_envs(self, time_delete):
        """Elastic Beanstalk Environment list function.

        List the IDs of all Elastic Beanstalk Environments.

        :yield Iterator[str]:
            Elastic Beanstalk Environment IDs
        """
        response = self.elasticbeanstalk.describe_environments()

        for env in response["Environments"]:
            if env["DateCreated"].timestamp() < time_delete:
                yield env["EnvironmentId"]
