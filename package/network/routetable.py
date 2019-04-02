"""This script nuke all route_table resources"""

import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_routetable(logger):
    """
         ec2 function for destroy all route table and
         network acl resources
    """
    # define connection
    ec2 = boto3.client('ec2')

    # Test if route table services is present in current aws region
    try:
        ec2.describe_route_tables()
    except EndpointConnectionError:
        print('ec2 resource is not available in this aws region')
        return

    # List all ec2 route table
    ec2_route_table_list = ec2_list_route_tables()

    # Nuke all ec2 route table
    for route_table in ec2_route_table_list:

        try:
            # Nuke ec2 route table
            ec2.delete_route_table(RouteTableId=route_table)
            logger.info("Nuke route table %s", route_table)
        except ClientError as e:
            if e.response['Error']['Code'] == 'DependencyViolation':
                logger.info("route %s cannot be deleted", route_table)
            else:
                print("Unexpected error: %s" % e)


def ec2_list_route_tables():
    """
       Aws ec2 list route tables, list name of
       all network route table and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_route_tables')
    page_iterator = paginator.paginate()

    # Initialize ec2 route table list
    ec2_route_table_list = []

    # Retrieve all ec2 route table Id
    for page in page_iterator:
        for route_table in page['RouteTables']:

            ec2_route_table = route_table['RouteTableId']
            ec2_route_table_list.insert(0, ec2_route_table)

    return ec2_route_table_list
