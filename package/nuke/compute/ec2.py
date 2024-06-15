# -*- coding: utf-8 -*-

"""Module deleting all EC2 instances, placement groups, and launch templates."""

from typing import Iterator
from botocore.exceptions import ClientError, WaiterError
from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEc2:
    """Abstract EC2 nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize EC2 nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float, required_tags: dict = None) -> None:
        """EC2 instance, placement group and template deleting function.

        Deleting all EC2 instances, placement groups, and launch templates
        with a timestamp greater than older_than_seconds and not matching the required tags.

        :param older_than_seconds:
            The timestamp in seconds used from which the AWS resource will be deleted
        :param required_tags:
            A dictionary of required tags to exclude the EC2 instances
        """
        self.nuke_instances(older_than_seconds, required_tags)
        self.nuke_launch_templates(older_than_seconds)
        self.nuke_placement_groups()

    def nuke_instances(self, time_delete: float, required_tags: dict = None) -> None:
        """EC2 instance delete function.

        Delete EC2 instances with a timestamp greater than time_delete and not matching required tags.

        :param time_delete:
            The timestamp in seconds used from which the AWS resource will be deleted
        :param required_tags:
            A dictionary of required tags to exclude the EC2 instances
        """
        instance_terminating = []
        ec2_waiter = self.ec2.get_waiter("instance_terminated")

        for instance in self.list_instances(time_delete, required_tags):
            try:
                self.ec2.terminate_instances(InstanceIds=[instance])
                print(f"Terminate instances {instance}")
            except ClientError as exc:
                nuke_exceptions("instance", instance, exc)
            else:
                instance_terminating.append(instance)

        if instance_terminating:
            try:
                ec2_waiter.wait(
                    InstanceIds=instance_terminating,
                    WaiterConfig={"Delay": 10, "MaxAttempts": 30},
                )
            except WaiterError as exc:
                nuke_exceptions("instance waiter", instance_terminating, exc)

    def nuke_launch_templates(self, time_delete: float) -> None:
        """EC2 launch template delete function.

        Delete EC2 instances with a timestamp greater than time_delete

        :param time_delete:
            The timestamp in seconds used from which the AWS resource will be deleted
        """
        for template in self.list_templates(time_delete):
            try:
                self.ec2.delete_launch_template(LaunchTemplateId=template)
                print(f"Nuke Launch Template {template}")
            except ClientError as exc:
                nuke_exceptions("EC2 template", template, exc)

    def nuke_placement_groups(self) -> None:
        """EC2 placement group delete function."""
        for placement_group in self.list_placement_groups():
            try:
                self.ec2.delete_placement_group(GroupName=placement_group)
                print(f"Nuke Placement Group {placement_group}")
            except ClientError as exc:
                nuke_exceptions("placement group", placement_group, exc)

    def list_instances(self, time_delete: float, required_tags: dict = None) -> Iterator[str]:
        """EC2 instance list function.

        List IDs of all EC2 instances with a timestamp lower than time_delete and not matching required tags.

        :param time_delete:
            Timestamp in seconds used to filter EC2 instances
        :param required_tags:
            A dictionary of required tags to exclude the EC2 instances

        :yield Iterator[str]:
            EC2 instances IDs
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
                        if required_tags and self.instance_has_tags(instance["InstanceId"], required_tags):
                            continue
                        yield instance["InstanceId"]

    def list_templates(self, time_delete: float) -> Iterator[str]:
        """Launch Template list function.

        List IDs of all Launch Templates with a timestamp lower than time_delete.

        :param time_delete:
            Timestamp in seconds used to filter Launch Templates

        :yield Iterator[str]:
            Launch Templates IDs
        """
        response = self.ec2.describe_launch_templates()

        for template in response["LaunchTemplates"]:
            if template["CreateTime"].timestamp() < time_delete:
                yield template["LaunchTemplateId"]

    def list_placement_groups(self) -> Iterator[str]:
        """Placement Group list function.

        List names of all placement groups.

        :yield Iterator[str]:
            Placement groups names
        """
        response = self.ec2.describe_placement_groups()

        for placementgroup in response["PlacementGroups"]:
            yield placementgroup["GroupName"]

    def instance_has_tags(self, instance_id: str, required_tags: dict) -> bool:
        """Check if the instance has the required tags.

        :param instance_id:
            ID of the EC2 instance
        :param required_tags:
            A dictionary of required tags to filter the EC2 instances
        :return:
            True if the instance has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [instance_id]}]
            )
            instance_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if instance_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("EC2 instance tagging", instance_id, exc)
            return False
