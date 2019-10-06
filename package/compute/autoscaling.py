# -*- coding: utf-8 -*-

"""Module deleting all aws autoscaling resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeAutoscaling:
    """Abstract autoscaling nuke in a class."""

    def __init__(self):
        """Initialize autoscaling nuke."""
        self.asg = boto3.client("autoscaling")

        try:
            self.asg.describe_auto_scaling_groups()
        except EndpointConnectionError:
            print("Autoscaling resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """Autoscaling deleting function.

        Deleting all Autoscaling Groups and Launch Configurations
        resources with a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for scaling in self.list_asg(older_than_seconds):
            try:
                self.asg.delete_auto_scaling_group(
                    AutoScalingGroupName=scaling, ForceDelete=True
                )
                print("Nuke Autoscaling Group {0}".format(scaling))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for launch_conf in self.list_launch_confs(older_than_seconds):
            try:
                self.asg.delete_launch_configuration(
                    LaunchConfigurationName=launch_conf
                )
                print("Nuke Launch Configuration {0}".format(launch_conf))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_asg(self, time_delete):
        """Autoscaling Group list function.

        List the names of all Autoscaling Groups with a timestamp lower
        than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Autoscaling Groups

        :yield Iterator[str]:
            Autoscaling Groups names
        """
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate():
            for asg in page["AutoScalingGroups"]:
                if asg["CreatedTime"].timestamp() < time_delete:
                    yield asg["AutoScalingGroupName"]

    def list_launch_confs(self, time_delete):
        """Launch configuration list function.

        Returns the names of all Launch Configuration Groups with
        a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Launch Configuration Groups

        :yield Iterator[str]:
            Launch Configurations names
        """
        paginator = self.asg.get_paginator("describe_launch_configurations")

        for page in paginator.paginate():
            for launch_conf in page["LaunchConfigurations"]:
                if launch_conf["CreatedTime"].timestamp() < time_delete:
                    yield launch_conf["LaunchConfigurationName"]
