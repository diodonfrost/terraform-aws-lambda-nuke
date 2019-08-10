# -*- coding: utf-8 -*-

"""Module deleting all aws ebs volume and dlm policie resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError


def nuke_all_ebs(older_than_seconds):
    """Ebs and dlm policies deleting function.

    Deleting all ebs volumes and dlm policy resources with
    a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    ec2 = boto3.client("ec2")
    dlm = boto3.client("dlm")

    # Deletes ebs volumes
    for volume in ebs_list_volumes(time_delete):
        try:
            ec2.delete_volume(VolumeId=volume)
            print("Nuke EBS Volume {0}".format(volume))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "VolumeInUse":
                logging.info("volume %s is already used", volume)
            elif error_code == "InvalidVolume":
                logging.info("volume %s has already been deleted", volume)
            else:
                logging.error("Unexpected error: %s", e)

    # Deletes snpashot lifecyle policy
    for policy in dlm_list_policy(time_delete):
        try:
            dlm.delete_lifecycle_policy(PolicyId=policy)
            print("Nuke EBS Lifecycle Policy {0}".format(policy))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def ebs_list_volumes(time_delete):
    """Ebs volume list function.

    List the IDs of all ebs volumes with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter ebs volumes
    :returns:
        List of ebs volumes IDs
    :rtype:
        [str]
    """
    ebs_volumes_list = []
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_volumes")

    for page in paginator.paginate():
        for volume in page["Volumes"]:
            if volume["CreateTime"].timestamp() < time_delete:
                ebs_volume = volume["VolumeId"]
                ebs_volumes_list.insert(0, ebs_volume)
    return ebs_volumes_list


def dlm_list_policy(time_delete):
    """Data Lifecycle Policies list function.

    Returns the IDs of all Data Lifecycle Policies with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter Data Lifecycle policies
    :returns:
        List of Data Lifecycle policies IDs
    :rtype:
        [str]
    """
    dlm_policy_list = []
    dlm = boto3.client("dlm")
    response = dlm.get_lifecycle_policies()

    for policy in response["Policies"]:
        detailed = dlm.get_lifecycle_policy(PolicyId=policy["PolicyId"])
        if detailed["Policy"]["DateCreated"].timestamp() < time_delete:
            dlm_policy = policy["PolicyId"]
            dlm_policy_list.insert(0, dlm_policy)
    return dlm_policy_list
