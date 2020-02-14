# -*- coding: utf-8 -*-

"""Module deleting all ec2 instances, placement groups and launch templates."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeEc2:
    """Abstract ec2 nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ec2 nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def nuke(self, older_than_seconds) -> None:
        """Ec2 instance, placement group and template deleting function.

        Deleting all ec2 instances, placement groups and launch
        templates with a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        self.nuke_instances(older_than_seconds)
        self.nuke_launch_templates(older_than_seconds)
        self.nuke_placement_groups()

    def nuke_instances(self, time_delete: float) -> None:
        """Ec2 instance delete function.

        Delete ec2 instances with a timestamp greater than time_delete

        :param int time_delete:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for instance in self.list_instances(time_delete):
            try:
                self.ec2.terminate_instances(InstanceIds=[instance])
                print("Terminate instances {0}".format(instance))
            except ClientError as exc:
                nuke_exceptions("instance", instance, exc)

    def nuke_launch_templates(self, time_delete: float) -> None:
        """Ec2 launche template delete function.

        Delete ec2 instances with a timestamp greater than time_delete

        :param int time_delete:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for template in self.list_templates(time_delete):
            try:
                self.ec2.delete_launch_template(LaunchTemplateId=template)
                print("Nuke Launch Template{0}".format(template))
            except ClientError as exc:
                nuke_exceptions("ec2 template", template, exc)

    def nuke_placement_groups(self) -> None:
        """Ec2 placement group delete function."""
        for placement_group in self.list_placement_groups():
            try:
                self.ec2.delete_placement_group(GroupName=placement_group)
                print("Nuke Placement Group {0}".format(placement_group))
            except ClientError as exc:
                nuke_exceptions("placement group", placement_group, exc)

    def list_instances(self, time_delete: float) -> Iterator[str]:
        """Ec2 instance list function.

        List IDs of all ec2 instances with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter ec2 instances

        :yield Iterator[str]:
            Ec2 instances IDs
        """
        paginator = self.ec2.get_paginator("describe_instances")
        page_iterator = paginator.paginate(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["pending", "running", "stopping", "stopped"],
                }
            ]
        )

        for page in page_iterator:
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    if instance["LaunchTime"].timestamp() < time_delete:
                        yield instance["InstanceId"]

    def list_templates(self, time_delete: float) -> Iterator[str]:
        """Launch Template list function.

        List Ids of all Launch Templates with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Launch Templates

        :yield Iterator[str]:
            Launch Templates Ids
        """
        response = self.ec2.describe_launch_templates()

        for template in response["LaunchTemplates"]:
            if template["CreateTime"].timestamp() < time_delete:
                yield template["LaunchTemplateId"]

    def list_placement_groups(self) -> Iterator[str]:
        """Placement Group list function.

        List name of all placement group.

        :yield Iterator[str]:
            Placement groups names
        """
        response = self.ec2.describe_placement_groups()

        for placementgroup in response["PlacementGroups"]:
            yield placementgroup["GroupName"]
