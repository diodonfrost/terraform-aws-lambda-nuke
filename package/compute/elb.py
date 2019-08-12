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
    elbv2 = boto3.client("elbv2")

    try:
        elb.describe_load_balancers()
        elbv2.describe_load_balancers()
    except EndpointConnectionError:
        print("elb resource is not available in this aws region")
        return

    elb_nuke_loadbalancers(time_delete)
    elbv2_nuke_loadbalancers(time_delete)
    elbv2_nuke_target_groups()


def elb_nuke_loadbalancers(time_delete):
    """Classic loadbalancer delete function."""
    elb = boto3.client("elb")

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


def elbv2_nuke_loadbalancers(time_delete):
    """Elbv2 loadbalancer delete function."""
    elbv2 = boto3.client("elbv2")

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


def elbv2_nuke_target_groups():
    """Elbv2 Target group delete function."""
    elbv2 = boto3.client("elbv2")

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

    for page in paginator.paginate():
        for loadbalancer in page["LoadBalancerDescriptions"]:
            if loadbalancer["CreatedTime"].timestamp() < time_delete:
                elb_loadbalancer_list.append(loadbalancer["LoadBalancerName"])
    return elb_loadbalancer_list


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

    for page in paginator.paginate():
        for lb in page["LoadBalancers"]:
            if lb["CreatedTime"].timestamp() < time_delete:
                elbv2_loadbalancer_list.append(lb["LoadBalancerArn"])
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

    for page in paginator.paginate():
        for targetgroup in page["TargetGroups"]:
            elbv2_targetgroup_list.append(targetgroup["TargetGroupArn"])
    return elbv2_targetgroup_list
