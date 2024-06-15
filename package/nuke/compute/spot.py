# -*- coding: utf-8 -*-

"""Module deleting all spot requests and spot fleets."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeSpot:
    """Abstract spot nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize spot nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Spot request and spot fleet deleting function.

        Deleting all Spot request and spot fleet deleting function with
        a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the spot requests and fleets to exclude from deletion
        """
        for spot_request in self.list_requests(older_than_seconds, required_tags):
            try:
                self.ec2.cancel_spot_instance_requests(
                    SpotInstanceRequestIds=[spot_request]
                )
                print("Cancel spot instance request {0}".format(spot_request))
            except ClientError as exc:
                nuke_exceptions("spot request", spot_request, exc)

        for spot_fleet in self.list_fleets(older_than_seconds, required_tags):
            try:
                self.ec2.cancel_spot_fleet_requests(
                    SpotFleetRequestIds=[spot_fleet]
                )
                print("Nuke spot fleet request {0}".format(spot_fleet))
            except ClientError as exc:
                nuke_exceptions("spot fleet", spot_fleet, exc)

    def list_requests(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Spot Request list function.

        List IDs of all Spot Requests with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter spot requests
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the spot requests to exclude from deletion

        :yield Iterator[str]:
            Spot requests IDs
        """
        response = self.ec2.describe_spot_instance_requests(
            Filters=[{"Name": "state", "Values": ["active", "open"]}]
        )

        for spot_request in response["SpotInstanceRequests"]:
            if spot_request["CreateTime"].timestamp() < time_delete:
                if required_tags and self._spot_request_has_required_tags(spot_request["SpotInstanceRequestId"], required_tags):
                    continue
                yield spot_request["SpotInstanceRequestId"]

    def list_fleets(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Spot Fleet list function.

        List IDs of all Spot Fleets with a timestamp
        lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter Spot Fleet
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the spot fleets to exclude from deletion

        :yield Iterator[str]:
            Spot Fleet IDs
        """
        paginator = self.ec2.get_paginator("describe_spot_fleet_requests")

        for page in paginator.paginate():
            for fleet in page["SpotFleetRequestConfigs"]:
                if fleet["CreateTime"].timestamp() < time_delete:
                    if required_tags and self._spot_fleet_has_required_tags(fleet["SpotFleetRequestId"], required_tags):
                        continue
                    yield fleet["SpotFleetRequestId"]

    def _spot_request_has_required_tags(self, spot_request_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the spot request has the required tags.

        :param str spot_request_id:
            The ID of the EC2 spot request
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the spot request has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [spot_request_id]}]
            )
            spot_request_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if spot_request_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("spot request tagging", spot_request_id, exc)
            return False

    def _spot_fleet_has_required_tags(self, spot_fleet_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the spot fleet has the required tags.

        :param str spot_fleet_id:
            The ID of the EC2 spot fleet
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the spot fleet has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [spot_fleet_id]}]
            )
            spot_fleet_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if spot_fleet_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("spot fleet tagging", spot_fleet_id, exc)
            return False
