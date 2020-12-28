# -*- coding: utf-8 -*-

"""Module deleting all aws autoscaling resources."""

from typing import Iterator

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeAutoscaling:
    """Abstract autoscaling nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize autoscaling nuke."""
        self.asg = AwsClient().connect("autoscaling", region_name)

        try:
            self.asg.describe_auto_scaling_groups()
        except EndpointConnectionError:
            print("Autoscaling resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
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
            except ClientError as exc:
                nuke_exceptions("autoscaling group", scaling, exc)

        for launch_conf in self.list_launch_confs(older_than_seconds):
            try:
                self.asg.delete_launch_configuration(
                    LaunchConfigurationName=launch_conf
                )
                print("Nuke Launch Configuration {0}".format(launch_conf))
            except ClientError as exc:
                nuke_exceptions("launch configuration", launch_conf, exc)

    def list_asg(self, time_delete: float) -> Iterator[str]:
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

    def list_launch_confs(self, time_delete: float) -> Iterator[str]:
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
