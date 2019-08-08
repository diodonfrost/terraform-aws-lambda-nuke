# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Load Balancer v2 resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_elbv2(older_than_seconds):
    """Elastic Load Balancer v2 deleting function.

    Deleting all elb v2 with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    elbv2 = boto3.client("elbv2")

    try:
        elbv2.describe_load_balancers()
    except EndpointConnectionError:
        print("elbv2 resource is not available in this aws region")
        return

    # Deletes elastic load balancer
    for loadbalancer in elbv2_list_loadbalancers(time_delete):
        try:
            elbv2.delete_load_balancer(LoadBalancerArn=loadbalancer)
            print("Nuke Load Balancer {0}".format(loadbalancer))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "OperationNotPermitted":
                logging.warning("Protected policy enable on %s", loadbalancer)
            else:
                logging.error("Unexpected error: %s", e)

    # Deletes elastic load balancer groups
    for targetgroup in elbv2_list_target_groups():
        try:
            elbv2.delete_target_group(TargetGroupArn=targetgroup)
            print("Nuke Target Group {0}".format(targetgroup))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceInUse":
                logging.warning("%s is use by listener or rule", targetgroup)
            else:
                logging.error("Unexpected error: %s", e)


def elbv2_list_loadbalancers(time_delete):
    """Elastic Load Balancer v2 list function.

    List ARN of all Elastic Load Balancer v2 with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter elbv2
    :returns:
        List of elbv2 ARN
    :rtype:
        [str]
    """
    elbv2_loadbalancer_list = []
    elbv2 = boto3.client("elbv2")
    paginator = elbv2.get_paginator("describe_load_balancers")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for loadbalancer in page["LoadBalancers"]:
            if loadbalancer["CreatedTime"].timestamp() < time_delete:
                elbv2_loadbalancer = loadbalancer["LoadBalancerArn"]
                elbv2_loadbalancer_list.insert(0, elbv2_loadbalancer)
    return elbv2_loadbalancer_list


def elbv2_list_target_groups():
    """Elastic Load Balancer Target Group list function.

    List ARN of all elbv2 Target Group with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter elbv2 Target Groups
    :returns:
        List of elbv2 ARN
    :rtype:
        [str]
    """
    elbv2_targetgroup_list = []
    elbv2 = boto3.client("elbv2")
    paginator = elbv2.get_paginator("describe_target_groups")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for targetgroup in page["TargetGroups"]:
            elbv2_targetgroup = targetgroup["TargetGroupArn"]
            elbv2_targetgroup_list.insert(0, elbv2_targetgroup)
    return elbv2_targetgroup_list
