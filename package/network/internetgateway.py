"""This script nuke all internet_gateway resources"""

import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_internetgateway(logger):
    """
         ec2 function for destroy all internet gateway
    """
    # define connection
    ec2 = boto3.client('ec2')

    # Test if internet gateway services is present in current aws region
    try:
        ec2.describe_internet_gateways()
        ec2.describe_egress_only_internet_gateways()
    except EndpointConnectionError:
        print('ec2 resource is not available in this aws region')
        return

    # List all ec2 internet gateway
    ec2_internet_gateway_list = ec2_list_internet_gateways()

    # Nuke all ec2 internet gateway
    for internet_gateway in ec2_internet_gateway_list:

        # Delete ec2 internet gateway
        try:
            ec2.delete_internet_gateway(
                InternetGatewayId=internet_gateway)
            print("Nuke internet gateway {0}".format(internet_gateway))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DependencyViolation':
                logger.info("internet gw %s cannot be deleted", internet_gateway)
            else:
                logger.error("Unexpected error: %s" % e)

    # List all ec2 egress internet gateway
    ec2_egress_gateway_list = ec2_list_egress_gateways()

    # Nuke all ec2 egress internet gateway
    for egress_gateway in ec2_egress_gateway_list:

        # Delete ec2 egress internet gateway
        try:
            ec2.delete_egress_only_internet_gateway(
                EgressOnlyInternetGatewayId=egress_gateway)
            print("Nuke egress gateway {0}".format(egress_gateway))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DependencyViolation':
                logger.info("egress gw %s cannot be deleted", egress_gateway)
            else:
                logger.error("Unexpected error: %s" % e)


def ec2_list_internet_gateways():
    """
       Aws ec2 list internet gateways, list name of
       all network internet gateway and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_internet_gateways()

    # Initialize ec2 internet gateway list
    ec2_internet_gateway_list = []

    # Retrieve all ec2 internet gateway Id
    for internet_gateway in response['InternetGateways']:

        ec2_internet_gateway = internet_gateway['InternetGatewayId']
        ec2_internet_gateway_list.insert(0, ec2_internet_gateway)

    return ec2_internet_gateway_list


def ec2_list_egress_gateways():
    """
       Aws ec2 list egress internet gateways, list name of
       all network egress internet gateway and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_egress_only_internet_gateways()

    # Initialize ec2 egress internet gateway list
    ec2_egress_gateway_list = []

    # Retrieve all ec2 egress internet gateway Id
    for egress_gateway in response['EgressOnlyInternetGateways']:

        ec2_egress_gateway = egress_gateway['EgressOnlyInternetGatewayId']
        ec2_egress_gateway_list.insert(0, ec2_egress_gateway)

    return ec2_egress_gateway_list
