# -*- coding: utf-8 -*-

"""Module deleting all aws endpoints."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_endpoint(older_than_seconds):
    """Endpoint deleting function.

    Deleting all aws endpoint with a timestamp
    greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    ec2 = boto3.client("ec2")

    # Test if endpoint services is present in current aws region
    try:
        ec2.describe_vpc_endpoints()
    except EndpointConnectionError:
        print("ec2 endpoint resource is not available in this aws region")
        return

    # List all ec2 endpoints
    ec2_endpoint_list = ec2_list_endpoints(time_delete)

    # Nuke all vpc endpoints
    try:
        ec2.delete_vpc_endpoints(VpcEndpointIds=ec2_endpoint_list)
        print("Nuke ec2 endpoint {0}".format(ec2_endpoint_list))
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "RequestLimitExceeded":
            logging.info("DeleteVpcEndpoints operation max retries reached")
        else:
            logging.error("Unexpected error: %s", e)


def ec2_list_endpoints(time_delete):
    """Aws enpoint list function.

    List IDs of all aws endpoints with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter aws endpoint
    :returns:
        List of Elastic aws endpoint IDs
    :rtype:
        [str]
    """
    # define connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_vpc_endpoints()

    # Initialize ec2 endpoint list
    ec2_endpoint_list = []

    # Retrieve all ec2 endpoint Id
    for endpoint in response["VpcEndpoints"]:
        if endpoint["CreationTimestamp"].timestamp() < time_delete:

            ec2_endpoint = endpoint["VpcEndpointId"]
            ec2_endpoint_list.insert(0, ec2_endpoint)

    return ec2_endpoint_list
