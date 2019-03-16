
"""This script nuke all elasticbeanstalk resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError


def nuke_all_elasticbeanstalk(older_than_seconds, logger):
    """
         elasticbeanstalk function for nuke all
         elasticbeanstalk stack
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    elasticbeanstalk = boto3.client('elasticbeanstalk')

    try:
        elasticbeanstalk.describe_applications()
    except EndpointConnectionError:
        print('elasticbeanstalk resource is not available in this aws region')
        return

    # List all elastic beanstalk app
    elasticbeanstalk_app_list = elasticbeanstalk_list_apps()

    # Nuke elasticbeanstalk application
    for app in elasticbeanstalk_app_list:
        if app['DateCreated'].timestamp() < time_delete:

            # Delete elasticbeanstalk app
            elasticbeanstalk.delete_application(
                ApplicationName=app,
                TerminateEnvByForce=True)
            logger.info("Nuke elasticbeanstalk application %s", app)

    # List all elastic beanstalk env
    elasticbeanstalk_env_list = elasticbeanstalk_list_envs()

    # Nuke elasticbeanstalk application
    for env in elasticbeanstalk_env_list:
        if env['DateCreated'].timestamp() < time_delete:

            # Delete elasticbeanstalk env
            elasticbeanstalk.terminate_environment(
                EnvironmentId=env,
                ForceTerminate=True)
            logger.info("Nuke elasticbeanstalk environment %s", env)


def elasticbeanstalk_list_apps():
    """
       Aws elastic beanstalk list application, list name of
       all application in elastic beanstalk and return it in list.
    """

    # Define the connection
    elasticbeanstalk = boto3.client('elasticbeanstalk')
    paginator = elasticbeanstalk.get_paginator('describe_applications')
    page_iterator = paginator.paginate()

    # Initialize elastic beanstalk app list
    elasticbeanstalk_app_list = []

    # Retrieve all elastic beanstalk apps
    for page in page_iterator:
        for app in page['Applications']:

            elasticbeanstalk_app = app['ApplicationName']
            elasticbeanstalk_app_list.insert(0, elasticbeanstalk_app)

    return elasticbeanstalk_app_list


def elasticbeanstalk_list_envs():
    """
       Aws eks elastic beanstalk list environment, list name of
       all environment in elastic beanstalk and return it in list.
    """

    # Define the connection
    elasticbeanstalk = boto3.client('elasticbeanstalk')
    paginator = elasticbeanstalk.get_paginator('describe_environments')
    page_iterator = paginator.paginate()

    # Initialize elastic beanstalk env list
    elasticbeanstalk_env_list = []

    # Retrieve all elastic beanstalk envs
    for page in page_iterator:
        for env in page['Environments']:

            elasticbeanstalk_env = env['EnvironmentId']
            elasticbeanstalk_env_list.insert(0, elasticbeanstalk_env)

    return elasticbeanstalk_env_list
