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

    elasticbeanstalk_nuke_app(time_delete)
    elasticbeanstalk_nuke_env(time_delete)


def elasticbeanstalk_nuke_app(time_delete):
    """Elastic Beanstalk Application nuke function."""
    elasticbeanstalk = boto3.client("elasticbeanstalk")

    for app in elasticbeanstalk_list_apps(time_delete):
        if app["DateCreated"].timestamp() < time_delete:
            try:
                elasticbeanstalk.delete_application(
                    ApplicationName=app, TerminateEnvByForce=True
                )
                print("Nuke elasticbeanstalk application{0}".format(app))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)


def elasticbeanstalk_nuke_env(time_delete):
    """Elastic Beanstalk Env nuke function."""
    elasticbeanstalk = boto3.client("elasticbeanstalk")

    for env in elasticbeanstalk_list_envs(time_delete):
        if env["DateCreated"].timestamp() < time_delete:
            try:
                elasticbeanstalk.terminate_environment(
                    EnvironmentId=env, ForceTerminate=True
                )
                print("Nuke elasticbeanstalk environment {0}".format(env))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)


def elasticbeanstalk_list_apps(time_delete):
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

    for page in paginator.paginate():
        for app in page["Applications"]:
            if app["DateCreated"].timestamp() < time_delete:
                elasticbeanstalk_app_list.append(app["ApplicationName"])
    return elasticbeanstalk_app_list


def elasticbeanstalk_list_envs(time_delete):
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

    for page in paginator.paginate():
        for env in page["Environments"]:
            if env["DateCreated"].timestamp() < time_delete:
                elasticbeanstalk_env_list.append(env["EnvironmentId"])
    return elasticbeanstalk_env_list
