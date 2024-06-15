# -*- coding: utf-8 -*-

"""Module deleting all aws cloudwatch dashboards and alarms."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeCloudwatch:
    """Abstract cloudwatch nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize cloudwatch nuke."""
        self.cloudwatch = AwsClient().connect("cloudwatch", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Cloudwatch and dlm policies deleting function.

        Deleting all cloudwatch dashboards and alarms resources with
        a timestamp greater than older_than_seconds and not matching
        the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the CloudWatch resources to exclude from deletion
        """
        for dashboard in self.list_dashboards(older_than_seconds, required_tags):
            try:
                self.cloudwatch.delete_dashboards(DashboardNames=[dashboard])
                print("Nuke cloudwatch dashboard {0}".format(dashboard))
            except ClientError as exc:
                nuke_exceptions("cloudwatch dashboard", dashboard, exc)

        for alarm in self.list_alarms(older_than_seconds, required_tags):
            try:
                self.cloudwatch.delete_alarms(AlarmNames=[alarm])
                print("Nuke cloudwatch alarm {0}".format(alarm))
            except ClientError as exc:
                nuke_exceptions("cloudwatch alarm", alarm, exc)

    def list_dashboards(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Cloudwatch dashboard list function.

        List the names of all cloudwatch dashboards with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter cloudwatch dashboards
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the CloudWatch dashboards to exclude from deletion

        :yield Iterator[str]:
            Cloudwatch dashboard names
        """
        paginator = self.cloudwatch.get_paginator("list_dashboards")

        for page in paginator.paginate():
            for dashboard in page["DashboardEntries"]:
                if dashboard["LastModified"].timestamp() < time_delete:
                    if required_tags and self._dashboard_has_required_tags(dashboard["DashboardName"], required_tags):
                        continue
                    yield dashboard["DashboardName"]

    def list_alarms(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Cloudwatch alarm list function.

        List the IDs of all cloudwatch alarms with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter cloudwatch alarms
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the CloudWatch alarms to exclude from deletion

        :yield Iterator[str]:
            Cloudwatch alarm IDs
        """
        paginator = self.cloudwatch.get_paginator("describe_alarms")

        for page in paginator.paginate():
            for alarm in page["MetricAlarms"]:
                if alarm["StateUpdatedTimestamp"].timestamp() < time_delete:
                    if required_tags and self._alarm_has_required_tags(alarm["AlarmName"], required_tags):
                        continue
                    yield alarm["AlarmName"]

    def _dashboard_has_required_tags(self, dashboard_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the dashboard has the required tags.

        :param str dashboard_name:
            The name of the CloudWatch dashboard
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the dashboard has all the required tags, False otherwise
        """
        try:
            response = self.cloudwatch.list_tags_for_resource(ResourceARN=dashboard_name)
            tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if tags.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for cloudwatch dashboard {dashboard_name}: {e}")
            return False

    def _alarm_has_required_tags(self, alarm_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the alarm has the required tags.

        :param str alarm_name:
            The name of the CloudWatch alarm
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the alarm has all the required tags, False otherwise
        """
        try:
            response = self.cloudwatch.list_tags_for_resource(ResourceARN=alarm_name)
            tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if tags.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for cloudwatch alarm {alarm_name}: {e}")
            return False
