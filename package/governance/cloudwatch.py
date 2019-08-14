# -*- coding: utf-8 -*-

"""Module deleting all aws cloudwatch dashboards and alarms."""

import logging
import time

import boto3

from botocore.exceptions import ClientError


def nuke_all_cloudwatch(older_than_seconds):
    """Cloudwatch and dlm policies deleting function.

    Deleting all cloudwatch dashboards and alarms resources with
    a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    cloudwatch = boto3.client("cloudwatch")

    # Deletes cloudwatch dashboards
    for dashboard in cloudwatch_list_dashboards(time_delete):
        try:
            cloudwatch.delete_dashboards(DashboardNames=[dashboard])
            print("Nuke cloudwatch dashboard {0}".format(dashboard))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # Deletes cloudwatch alarms
    for alarm in cloudwatch_list_alarms(time_delete):
        try:
            cloudwatch.delete_alarms(AlarmNames=[alarm])
            print("Nuke cloudwatch alarm {0}".format(alarm))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def cloudwatch_list_dashboards(time_delete):
    """Cloudwatch dashboard list function.

    List the names of all cloudwatch dashboards with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter cloudwatch dashboards
    :returns:
        List of cloudwatch dashboard names
    :rtype:
        [str]
    """
    cloudwatch_dashboard_list = []
    cloudwatch = boto3.client("cloudwatch")
    paginator = cloudwatch.get_paginator("list_dashboards")

    for page in paginator.paginate():
        for dashboard in page["DashboardEntries"]:
            if dashboard["LastModified"].timestamp() < time_delete:
                cloudwatch_dashboard_list.append(dashboard["DashboardName"])
    return cloudwatch_dashboard_list


def cloudwatch_list_alarms(time_delete):
    """Cloudwatch alarm list function.

    List the IDs of all cloudwatch alarms with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter cloudwatch alarms
    :returns:
        List of cloudwatch alarm IDs
    :rtype:
        [str]
    """
    cloudwatch_alarm_list = []
    cloudwatch = boto3.client("cloudwatch")
    paginator = cloudwatch.get_paginator("describe_alarms")

    for page in paginator.paginate():
        for alarm in page["MetricAlarms"]:
            if alarm["StateUpdatedTimestamp"].timestamp() < time_delete:
                cloudwatch_alarm_list.append(alarm["AlarmName"])
    return cloudwatch_alarm_list
