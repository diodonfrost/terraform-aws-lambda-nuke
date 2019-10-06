# -*- coding: utf-8 -*-

"""Module deleting all spot requests and spot fleets."""

import logging

import boto3

from botocore.exceptions import ClientError


class NukeSpot:
    """Abstract spot nuke in a class."""

    def __init__(self):
        """Initialize spot nuke."""
        self.ec2 = boto3.client("ec2")

    def nuke(self, older_than_seconds):
        """Spot request and spot fleet deleting function.

        Deleting all Spot request and spot fleet deleting function with
        a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for spot_request in self.list_requests(older_than_seconds):
            try:
                self.ec2.cancel_spot_instance_requests(
                    SpotInstanceRequestIds=[spot_request]
                )
                print("Cancel spot instance request {0}".format(spot_request))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for spot_fleet in self.list_fleet(older_than_seconds):
            try:
                self.ec2.cancel_spot_fleet_requests(
                    SpotFleetRequestIds=[spot_fleet]
                )
                print("Nuke spot fleet request {0}".format(spot_fleet))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_requests(self, time_delete):
        """Spot Request list function.

        List IDs of all Spot Requests with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter spot requests

        :yield Iterator[str]:
            Spot requests IDs
        """
        response = self.ec2.describe_spot_instance_requests(
            Filters=[{"Name": "state", "Values": ["active"]}]
        )

        for spot_request in response["SpotInstanceRequests"]:
            if spot_request["CreateTime"].timestamp() < time_delete:
                yield spot_request["SpotInstanceRequestId"]

    def list_fleet(self, time_delete):
        """Spot Fleet list function.

        List IDs of all Spot Fleets with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Spot Fleet

        :yield Iterator[str]:
            Spot Fleet IDs
        """
        paginator = self.ec2.get_paginator("describe_spot_fleet_requests")

        for page in paginator.paginate():
            for fleet in page["SpotFleetRequestConfigs"]:
                if fleet["CreateTime"].timestamp() < time_delete:
                    yield fleet["SpotFleetRequestId"]
