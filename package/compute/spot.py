"""This script nuke all ec2 resources"""

import logging
import time
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


def nuke_all_spot(older_than_seconds):
    """
        Function for destroy all spot fleet
        and spot request resources
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define the connection
    ec2 = boto3.client('ec2')

    # List all spot requests
    spot_request_list = spot_list_requests(time_delete)

    # Nuke all aws spot instance request
    for spot_request in spot_request_list:
        try:
            ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[spot_request])
            print("Cancel spot instance request {0}".format(spot_request))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # List all spot fleet
    spot_fleet_list = spot_list_fleet(time_delete)

    # nuke all aws spot fleet request
    for spot_fleet in spot_fleet_list:
        try:
            ec2.cancel_spot_fleet_requests(SpotFleetRequestIds=[spot_fleet])
            print("Nuke spot fleet request {0}".format(spot_fleet))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def spot_list_requests(time_delete):
    """
       Aws spot request list function, list name of all spot request
    """
    # Define the connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_spot_instance_requests(
        Filters=[{'Name': 'state', 'Values': ['active']}])

    # Initialize spot request list
    spot_request_list = []

    # Retrieve ec2 instances
    for spot_request in response['SpotInstanceRequests']:
        if spot_request['CreateTime'].timestamp() < time_delete:

            # Retrieve spot request id and add in list
            spot_request_id = spot_request['SpotInstanceRequestId']
            spot_request_list.insert(0, spot_request_id)

    return spot_request_list


def spot_list_fleet(time_delete):
    """
       Aws spot fleet list function, list name of
       all spot fleet request and return it in list.
    """
    # Define the connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_spot_fleet_requests()

    # Initialize spot fleet list
    spot_fleet_list = []

    # Retrieve all spot fleet request
    for fleet in response['SpotFleetRequestConfigs']:
        if fleet['CreateTime'].timestamp() < time_delete:

            spot_fleet_list = fleet['SpotFleetRequestId']
            spot_fleet_list.insert(0, spot_fleet_list)

    return spot_fleet_list
