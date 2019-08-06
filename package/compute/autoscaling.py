# -*- coding: utf-8 -*-

"""Module deleting all aws autoscaling resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_autoscaling(older_than_seconds):
    """Autoscaling deleting function.

    Deleting all Autoscaling Groups and Launch
    Configurations resources with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    autoscaling = boto3.client("autoscaling")

    try:
        autoscaling.describe_auto_scaling_groups()
    except EndpointConnectionError:
        print("autoscaling resource is not available in this aws region")
        return

    # List all autoscaling groups
    autoscaling_group_list = autoscaling_list_groups(time_delete)

    # Nuke all autoscaling groups
    for scaling in autoscaling_group_list:

        # Delete autoscaling group
        try:
            autoscaling.delete_auto_scaling_group(
                AutoScalingGroupName=scaling, ForceDelete=True
            )
            print("Nuke Autoscaling Group {0}".format(scaling))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # List all launch configurations
    launch_list_configuration = autoscaling_list_launch_confs(time_delete)

    # Nuke all autoscaling launch configurations
    for launchconfiguration in launch_list_configuration:

        # Delete launch configuration
        try:
            autoscaling.delete_launch_configuration(
                LaunchConfigurationName=launchconfiguration
            )
            print("Nuke Launch Configuration {0}".format(launchconfiguration))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def autoscaling_list_groups(time_delete):
    """Autoscaling Group list function.

    List the names of all Autoscaling Groups with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Autoscaling Groups
    :returns:
        List of Autoscaling Groups names
    :rtype:
        [str]
    """
    # Define connection with paginator
    autoscaling = boto3.client("autoscaling")
    paginator = autoscaling.get_paginator("describe_auto_scaling_groups")
    page_iterator = paginator.paginate()

    # Initialize autoscaling group list
    autoscaling_group_list = []

    # Retrieve ec2 autoscalinggroup tags
    for page in page_iterator:
        for group in page["AutoScalingGroups"]:
            if group["CreatedTime"].timestamp() < time_delete:

                # Retrieve and add in list autoscaling name
                autoscaling_group = group["AutoScalingGroupName"]
                autoscaling_group_list.insert(0, autoscaling_group)

    return autoscaling_group_list


def autoscaling_list_launch_confs(time_delete):
    """Launch configuration list function.

    Returns the names of all Launch Configuration Groups with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Launch Configuration Groups
    :returns:
        List of Launch Configurations names
    :rtype:
        [str]
    """
    # Define connection with paginator
    autoscaling = boto3.client("autoscaling")
    paginator = autoscaling.get_paginator("describe_launch_configurations")
    page_iterator = paginator.paginate()

    # Initialize autoscaling launch configuration list
    autoscaling_launch_conf_list = []

    # Retrieve autoscaling launch configuration names
    for page in page_iterator:
        for launchconf in page["LaunchConfigurations"]:
            if launchconf["CreatedTime"].timestamp() < time_delete:

                launch_configuration = launchconf["LaunchConfigurationName"]
                autoscaling_launch_conf_list.insert(0, launch_configuration)

    return autoscaling_launch_conf_list
