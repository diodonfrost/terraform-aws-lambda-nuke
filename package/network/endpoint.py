"""This script nuke all endpoint resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_endpoint(older_than_seconds, logger):
    """
         ec2 function for destroy all endpoint and
         network acl resources
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    ec2 = boto3.client('ec2')

    # Test if endpoint services is present in current aws region
    try:
        ec2.describe_vpc_endpoints()
    except EndpointConnectionError:
        print('ec2 endpoint resource is not available in this aws region')
        return

    # List all ec2 endpoints
    ec2_endpoint_list = ec2_list_endpoints(time_delete)

    try:
        # Nuke all ec2 endpoints
        ec2.delete_vpc_endpoints(
            VpcEndpointIds=ec2_endpoint_list)
        logger.info("Nuke ec2 endpoint %s", ec2_endpoint_list)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ClientError':
            logger.info("DeleteVpcEndpoints operation max retries reached")
        else:
            print("Unexpected error: %s" % e)


    # List all ec2 endpoint services
    ec2_endpoint_service_list = ec2_list_endpoint_services()

    try:
        # Nuke all ec2 endpoints
        ec2.delete_vpc_endpoint_service_configurations(
            ServiceIds=ec2_endpoint_service_list)
        logger.info("Nuke ec2 endpoint %s", ec2_endpoint_service_list)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ClientError':
            logger.info("DeleteVpcEndpoints operation max retries reached")
        else:
            print("Unexpected error: %s" % e)


def ec2_list_endpoints(time_delete):
    """
       Aws ec2 list endpoints, list name of
       all network endpoint and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpc_endpoints()

    # Initialize ec2 endpoint list
    ec2_endpoint_list = []

    # Retrieve all ec2 endpoint Id
    for endpoint in response['VpcEndpoints']:
        if endpoint['CreationTimestamp'].timestamp() < time_delete:

            ec2_endpoint = endpoint['VpcEndpointId']
            ec2_endpoint_list.insert(0, ec2_endpoint)

    return ec2_endpoint_list


def ec2_list_endpoint_services():
    """
       Aws ec2 list endpoint service, list name of
       all  endpoint services and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpc_endpoint_service_configurations()

    # Initialize ec2 endpoint list
    ec2_endpoint_service_list = []

    # Retrieve all ec2 endpoint Id
    for endpoint in response['ServiceConfigurations']:

        ec2_endpoint_service = endpoint['ServiceId']
        ec2_endpoint_service_list.insert(0, ec2_endpoint_service)

    return ec2_endpoint_service_list
