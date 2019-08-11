# -*- coding: utf-8 -*-

"""Module deleting all spot requests and spot fleets."""

import logging
import time

import boto3

from botocore.exceptions import ClientError


def nuke_all_spot(older_than_seconds):
    """Spot request and spot fleet deleting function.

    Deleting all Spot request and spot fleet deleting function with
    a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    ec2 = boto3.client("ec2")

    # Deletes spot requests
    for spot_request in spot_list_requests(time_delete):
        try:
            ec2.cancel_spot_instance_requests(
                SpotInstanceRequestIds=[spot_request]
            )
            print("Cancel spot instance request {0}".format(spot_request))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # Delete spot fleets
    for spot_fleet in spot_list_fleet(time_delete):
        try:
            ec2.cancel_spot_fleet_requests(SpotFleetRequestIds=[spot_fleet])
            print("Nuke spot fleet request {0}".format(spot_fleet))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def spot_list_requests(time_delete):
    """Spot Request list function.

    List IDs of all Spot Requests with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter spot requests
    :returns:
        List of  Spot requests IDs
    :rtype:
        [str]
    """
    spot_request_list = []
    ec2 = boto3.client("ec2")
    response = ec2.describe_spot_instance_requests(
        Filters=[{"Name": "state", "Values": ["active"]}]
    )

    for spot_request in response["SpotInstanceRequests"]:
        if spot_request["CreateTime"].timestamp() < time_delete:
            spot_request_list.append(spot_request["SpotInstanceRequestId"])
    return spot_request_list


def spot_list_fleet(time_delete):
    """Spot Fleet list function.

    List IDs of all Spot Fleets with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Spot Fleet
    :returns:
        List of Spot Fleet IDs
    :rtype:
        [str]
    """
    spot_fleet_list = []
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_spot_fleet_requests")

    for page in paginator.paginate():
        for fleet in page["SpotFleetRequestConfigs"]:
            if fleet["CreateTime"].timestamp() < time_delete:
                spot_fleet_list.append(fleet["SpotFleetRequestId"])
    return spot_fleet_list
