# -*- coding: utf-8 -*-

"""This script nuke all eip resources"""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_eip():
    """
         ec2 function for destroy all elastic
    """
    # define connection
    ec2 = boto3.client("ec2")

    # Test if Elastic ip services is present in current aws region
    try:
        ec2.describe_addresses()
    except EndpointConnectionError:
        print("ec2 resource is not available in this aws region")
        return

    # List all ec2 elastic ip
    ec2_eip_list = ec2_list_eips()

    # Nuke all ec2 elastic ip
    for eip in ec2_eip_list:

        # Delete elastic ip
        try:
            ec2.release_address(AllocationId=eip)
            print("Nuke elastic ip {0}".format(eip))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def ec2_list_eips():
    """
       Aws ec2 list elastic ips, list name of
       all network elastic ip and return it in list.
    """

    # define connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_addresses()

    # Initialize ec2 elastic ip list
    ec2_eip_list = []

    # Retrieve all ec2 elastic ip Id
    for eip in response["Addresses"]:

        ec2_eip = eip["AllocationId"]
        ec2_eip_list.insert(0, ec2_eip)

    return ec2_eip_list
