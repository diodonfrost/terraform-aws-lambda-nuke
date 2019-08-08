# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Beanstalk resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_elasticbeanstalk(older_than_seconds):
    """Elastic Beanstalk deleting function.

    Deleting all Elastic Beanstalk with a timestamp
    greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    elasticbeanstalk = boto3.client("elasticbeanstalk")

    try:
        elasticbeanstalk.describe_applications()
    except EndpointConnectionError:
        print("elasticbeanstalk resource is not available in this aws region")
        return

    # Delete elasticbeanstalk apps
    for app in elasticbeanstalk_list_apps():
        if app["DateCreated"].timestamp() < time_delete:
            try:
                elasticbeanstalk.delete_application(
                    ApplicationName=app, TerminateEnvByForce=True
                )
                print("Nuke elasticbeanstalk application{0}".format(app))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    # Delete elasticbeanstalk envs
    for env in elasticbeanstalk_list_envs():
        if env["DateCreated"].timestamp() < time_delete:
            try:
                elasticbeanstalk.terminate_environment(
                    EnvironmentId=env, ForceTerminate=True
                )
                print("Nuke elasticbeanstalk environment {0}".format(env))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)


def elasticbeanstalk_list_apps():
    """Elastic Beanstalk Application list function.

    List the names of all Elastic Beanstalk Applications.

    :returns:
        List of Elastic Beanstalk Application names
    :rtype:
        [str]
    """
    elasticbeanstalk_app_list = []
    elasticbeanstalk = boto3.client("elasticbeanstalk")
    paginator = elasticbeanstalk.get_paginator("describe_applications")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for app in page["Applications"]:
            elasticbeanstalk_app = app["ApplicationName"]
            elasticbeanstalk_app_list.insert(0, elasticbeanstalk_app)
    return elasticbeanstalk_app_list


def elasticbeanstalk_list_envs():
    """Elastic Beanstalk Environment list function.

    List the IDs of all Elastic Beanstalk Environments.

    :returns:
        List of Elastic Beanstalk Environment IDs
    :rtype:
        [str]
    """
    elasticbeanstalk_env_list = []
    elasticbeanstalk = boto3.client("elasticbeanstalk")
    paginator = elasticbeanstalk.get_paginator("describe_environments")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for env in page["Environments"]:
            elasticbeanstalk_env = env["EnvironmentId"]
            elasticbeanstalk_env_list.insert(0, elasticbeanstalk_env)
    return elasticbeanstalk_env_list
