# -*- coding: utf-8 -*-

"""Module deleting all aws Classic Load Balancer resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_elb(older_than_seconds):
    """Classic Load Balancer deleting function.

    Deleting all classic lb with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    elb = boto3.client("elb")

    try:
        elb.describe_load_balancers()
    except EndpointConnectionError:
        print("elb resource is not available in this aws region")
        return

    # Deletes classic loadbalancer
    for loadbalancer in elb_list_loadbalancers(time_delete):
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
    """Elastic Load Balancer list function.

    List the names of all Elastic Load Balancer with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Elastic Load Balancer
    :returns:
        List of Elastic Load Balancer names
    :rtype:
        [str]
    """
    elb_loadbalancer_list = []
    elb = boto3.client("elb")
    paginator = elb.get_paginator("describe_load_balancers")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for loadbalancer in page["LoadBalancerDescriptions"]:
            if loadbalancer["CreatedTime"].timestamp() < time_delete:
                elb_loadbalancer = loadbalancer["LoadBalancerName"]
                elb_loadbalancer_list.insert(0, elb_loadbalancer)
    return elb_loadbalancer_list
