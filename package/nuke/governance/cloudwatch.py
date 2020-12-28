# -*- coding: utf-8 -*-

"""Module deleting all aws cloudwatch dashboards and alarms."""

from typing import Iterator

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeCloudwatch:
    """Abstract cloudwatch nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize cloudwatch nuke."""
        self.cloudwatch = AwsClient().connect("cloudwatch", region_name)

    def nuke(self, older_than_seconds: float) -> None:
        """Cloudwatch and dlm policies deleting function.

        Deleting all cloudwatch dashboards and alarms resources with
        a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for dashboard in self.list_dashboards(older_than_seconds):
            try:
                self.cloudwatch.delete_dashboards(DashboardNames=[dashboard])
                print("Nuke cloudwatch dashboard {0}".format(dashboard))
            except ClientError as exc:
                nuke_exceptions("cloudwatch dashboard", dashboard, exc)

        for alarm in self.list_alarms(older_than_seconds):
            try:
                self.cloudwatch.delete_alarms(AlarmNames=[alarm])
                print("Nuke cloudwatch alarm {0}".format(alarm))
            except ClientError as exc:
                nuke_exceptions("cloudwatch alarm", alarm, exc)

    def list_dashboards(self, time_delete: float) -> Iterator[str]:
        """Cloudwatch dashboard list function.

        List the names of all cloudwatch dashboards with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter cloudwatch dashboards

        :yield Iterator[str]:
            Cloudwatch dashboard names
        """
        paginator = self.cloudwatch.get_paginator("list_dashboards")

        for page in paginator.paginate():
            for dashboard in page["DashboardEntries"]:
                if dashboard["LastModified"].timestamp() < time_delete:
                    yield dashboard["DashboardName"]

    def list_alarms(self, time_delete: float) -> Iterator[str]:
        """Cloudwatch alarm list function.

        List the IDs of all cloudwatch alarms with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter cloudwatch alarms

        :yield Iterator[str]:
            Cloudwatch alarm IDs
        """
        paginator = self.cloudwatch.get_paginator("describe_alarms")

        for page in paginator.paginate():
            for alarm in page["MetricAlarms"]:
                if alarm["StateUpdatedTimestamp"].timestamp() < time_delete:
                    yield alarm["AlarmName"]
