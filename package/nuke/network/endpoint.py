# -*- coding: utf-8 -*-

"""Module deleting all aws endpoints."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeEndpoint:
    """Abstract endpoint nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize endpoint nuke."""
        self.ec2 = AwsClient().connect("ec2", region_name)

        try:
            self.ec2.describe_vpc_endpoints()
        except EndpointConnectionError:
            print("EC2 endpoint resource is not available in this AWS region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Endpoint deleting function.

        Deleting all AWS endpoints with a timestamp greater than
        older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the AWS resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the endpoints to exclude from deletion
        """
        for endpoint in self.list_endpoints(older_than_seconds, required_tags):
            try:
                self.ec2.delete_vpc_endpoints(VpcEndpointIds=[endpoint])
                print("Nuke EC2 endpoint {0}".format(endpoint))
            except ClientError as exc:
                nuke_exceptions("VPC endpoint", endpoint, exc)

    def list_endpoints(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """AWS endpoint list function.

        List IDs of all AWS endpoints with a timestamp lower than
        time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering AWS endpoints
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the endpoints to exclude from deletion

        :yield Iterator[str]:
            Elastic AWS endpoint IDs
        """
        response = self.ec2.describe_vpc_endpoints()

        for endpoint in response["VpcEndpoints"]:
            if endpoint["CreationTimestamp"].timestamp() < time_delete:
                if required_tags and self._endpoint_has_required_tags(endpoint["VpcEndpointId"], required_tags):
                    continue
                yield endpoint["VpcEndpointId"]

    def _endpoint_has_required_tags(self, endpoint_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the endpoint has the required tags.

        :param str endpoint_id:
            The ID of the VPC endpoint
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the endpoint has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [endpoint_id]}]
            )
            endpoint_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if endpoint_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("VPC endpoint tagging", endpoint_id, exc)
            return False
