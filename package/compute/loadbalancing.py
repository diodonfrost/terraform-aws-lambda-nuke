
"""This script nuke all autoscaling resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_loadbalancing(older_than_seconds, logger):
    """
        Function for destroy every loadbalancer and
        target groups aws resources
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    elbv2 = boto3.client('elbv2')

    try:
        elbv2.describe_load_balancers()
    except EndpointConnectionError:
        print('elbv2 resource is not available in this aws region')
        return

    # List all elbv2 load balaner arn
    elbv2_loadbalancer_list = elbv2_list_loadbalancers(time_delete)

    # Nuke all load balancers
    for loadbalancer in elbv2_loadbalancer_list:

        # Delete load balancer
        try:
            elbv2.delete_load_balancer(LoadBalancerArn=loadbalancer)
            print("Nuke Load Balancer %s", loadbalancer)
        except ClientError as e:
            logger.error("Unexpected error: %s" % e)

    # List all elbv2 target group arn
    elbv2_targetgroup_list = elbv2_list_target_groups()

    for targetgroup in elbv2_targetgroup_list:

        # Nuke all target group
        try:
            elbv2.delete_target_group(TargetGroupArn=targetgroup)
            print("Nuke Target Group %s", targetgroup)
        except ClientError as e:
            logger.error("Unexpected error: %s" % e)


def elbv2_list_loadbalancers(time_delete):
    """
       Aws elb list load balancer, list name of
       all elastic load balancers and return it in list.
    """

    # Define the connection
    elbv2 = boto3.client('elbv2')
    paginator = elbv2.get_paginator('describe_load_balancers')
    page_iterator = paginator.paginate()

    # Initialize elbv2 loadbalancer list
    elbv2_loadbalancer_list = []

    # Retrieve all elbv2 loadbalancers arn
    for page in page_iterator:
        for loadbalancer in page['LoadBalancers']:
            if loadbalancer['CreatedTime'].timestamp() < time_delete:

                elbv2_loadbalancer = loadbalancer['LoadBalancerArn']
                elbv2_loadbalancer_list.insert(0, elbv2_loadbalancer)

    return elbv2_loadbalancer_list


def elbv2_list_target_groups():
    """
       Aws elb list target group, list name of
       all target groups and return it in list.
    """

    # Define the connection
    elbv2 = boto3.client('elbv2')
    paginator = elbv2.get_paginator('describe_target_groups')
    page_iterator = paginator.paginate()

    # Initialize elbv2 target group list
    elbv2_targetgroup_list = []

    # Retrieve all elbv2 target groups arn
    for page in page_iterator:
        for targetgroup in page['TargetGroups']:

            elbv2_targetgroup = targetgroup['TargetGroupArn']
            elbv2_targetgroup_list.insert(0, elbv2_targetgroup)

    return elbv2_targetgroup_list
