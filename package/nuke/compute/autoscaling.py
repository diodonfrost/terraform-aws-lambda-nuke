# -*- coding: utf-8 -*-

"""Module deleting all aws autoscaling resources."""

from typing import Iterator, Dict

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

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Autoscaling deleting function.

        Deleting all Autoscaling Groups and Launch Configurations
        resources with a timestamp greater than older_than_seconds
        and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the ASGs and LCs to exclude from deletion
        """
        for scaling in self.list_asg(older_than_seconds, required_tags):
            try:
                self.asg.delete_auto_scaling_group(
                    AutoScalingGroupName=scaling, ForceDelete=True
                )
                print("Nuke Autoscaling Group {0}".format(scaling))
            except ClientError as exc:
                nuke_exceptions("autoscaling group", scaling, exc)

        for launch_conf in self.list_launch_confs(older_than_seconds, required_tags):
            try:
                self.asg.delete_launch_configuration(
                    LaunchConfigurationName=launch_conf
                )
                print("Nuke Launch Configuration {0}".format(launch_conf))
            except ClientError as exc:
                nuke_exceptions("launch configuration", launch_conf, exc)

    def list_asg(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Autoscaling Group list function.

        List the names of all Autoscaling Groups with a timestamp lower
        than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering Autoscaling Groups
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the ASGs to exclude from deletion

        :yield Iterator[str]:
            Autoscaling Groups names
        """
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate():
            for asg in page["AutoScalingGroups"]:
                if asg["CreatedTime"].timestamp() < time_delete:
                    if required_tags and not self._asg_has_required_tags(asg["AutoScalingGroupName"], required_tags):
                        continue
                    yield asg["AutoScalingGroupName"]

    def list_launch_confs(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Launch configuration list function.

        Returns the names of all Launch Configurations with
        a timestamp lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering Launch Configurations
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the LCs to exclude from deletion

        :yield Iterator[str]:
            Launch Configurations names
        """
        paginator = self.asg.get_paginator("describe_launch_configurations")

        for page in paginator.paginate():
            for launch_conf in page["LaunchConfigurations"]:
                if launch_conf["CreatedTime"].timestamp() < time_delete:
                    if required_tags and not self._launch_conf_has_required_tags(launch_conf["LaunchConfigurationName"], required_tags):
                        continue
                    yield launch_conf["LaunchConfigurationName"]

    def _asg_has_required_tags(self, asg_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Autoscaling Group has the required tags.

        :param str asg_name:
            The name of the Autoscaling Group
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the Autoscaling Group has all the required tags, False otherwise
        """
        try:
            response = self.asg.describe_tags(
                Filters=[{"Name": "auto-scaling-group", "Values": [asg_name]}]
            )
            tags = response["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Autoscaling group tagging", asg_name, exc)
            return False

    def _launch_conf_has_required_tags(self, launch_conf_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Launch Configuration has the required tags.

        :param str launch_conf_name:
            The name of the Launch Configuration
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the Launch Configuration has all the required tags, False otherwise
        """
        try:
            response = self.asg.describe_tags(
                Filters=[{"Name": "key", "Values": [launch_conf_name]}]
            )
            tags = response["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Launch configuration tagging", launch_conf_name, exc)
            return False
