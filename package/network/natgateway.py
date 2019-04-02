"""This script nuke all nat_gateway resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError


def nuke_all_natgateway(older_than_seconds, logger):
    """
         ec2 function for destroy all ec2 nat gateway
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    ec2 = boto3.client('ec2')

    # Test if nat gateway services is present in current aws region
    try:
        ec2.describe_nat_gateways()
    except EndpointConnectionError:
        print('ec2 resource is not available in this aws region')
        return

    # List all ec2 nat gateway
    ec2_nat_gateway_list = ec2_list_nat_gateways(time_delete)

    # Nuke all ec2 nat gateway
    for nat_gw in ec2_nat_gateway_list:

        ec2.delete_nat_gateway(NatGatewayId=nat_gw)
        logger.info("Nuke nate gateway %s", nat_gw)


def ec2_list_nat_gateways(time_delete):
    """
       Aws ec2 list nat gateways, list name of
       all network nat gateway and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_nat_gateways')
    page_iterator = paginator.paginate()

    # Initialize ec2 nat gateway list
    ec2_nat_gateway_list = []

    # Retrieve all ec2 nat gateway Id
    for page in page_iterator:
        for nat_gateway in page['NatGateways']:
            if (nat_gateway['CreateTime'].timestamp() < time_delete and
                    nat_gateway['State'] != 'deleted'):

                ec2_nat_gateway = nat_gateway['NatGatewayId']
                ec2_nat_gateway_list.insert(0, ec2_nat_gateway)

    return ec2_nat_gateway_list
