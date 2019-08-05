# -*- coding: utf-8 -*-

"""This script nuke all autoscaling resources"""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_elb(older_than_seconds):
    """
        Function for destroy every elb and
        target groups aws resources
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    elb = boto3.client("elb")

    try:
        elb.describe_load_balancers()
    except EndpointConnectionError:
        print("elb resource is not available in this aws region")
        return

    # List all elb load balaner arn
    elb_loadbalancer_list = elb_list_loadbalancers(time_delete)

    # Nuke all load balancers
    for loadbalancer in elb_loadbalancer_list:

        # Delete load balancer
        try:
            elb.delete_load_balancer(LoadBalancerName=loadbalancer)
            print("Nuke Load Balancer {0}".format(loadbalancer))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "OperationNotPermitted":
                logging.warning("Protected policy enable on %s", loadbalancer)
            else:
                logging.error("Unexpected error: %s", e)


def elb_list_loadbalancers(time_delete):
    """
       Aws elb list load balancer, list name of
       all elastic load balancers and return it in list.
    """

    # Define the connection
    elb = boto3.client("elb")
    paginator = elb.get_paginator("describe_load_balancers")
    page_iterator = paginator.paginate()

    # Initialize elb loadbalancer list
    elb_loadbalancer_list = []

    # Retrieve all elb loadbalancers arn
    for page in page_iterator:
        for loadbalancer in page["LoadBalancerDescriptions"]:
            if loadbalancer["CreatedTime"].timestamp() < time_delete:

                elb_loadbalancer = loadbalancer["LoadBalancerName"]
                elb_loadbalancer_list.insert(0, elb_loadbalancer)

    return elb_loadbalancer_list
