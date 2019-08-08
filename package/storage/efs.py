# -*- coding: utf-8 -*-

"""Module deleting all aws efs resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_efs(older_than_seconds):
    """EFS deleting function.

    Deleting all efs with a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    efs = boto3.client("efs")

    # Test if efs services is present in current aws region
    try:
        efs.describe_file_systems()
    except EndpointConnectionError:
        print("EFS resource is not available in this aws region")
        return

    # Delete efs
    for efs in efs_list_file_systems(time_delete):
        try:
            efs.delete_file_system(FileSystemId=efs)
            print("Nuke EFS share {0}".format(efs))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def efs_list_file_systems(time_delete):
    """EFS list function.

    List IDS of all efs with a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter efs
    :returns:
        List of efs IDs
    :rtype:
        [str]
    """
    efs_filesystem_list = []
    efs = boto3.client("efs")
    paginator = efs.get_paginator("describe_file_systems")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for filesystem in page["FileSystems"]:
            if efs["CreationTime"].timestamp() < time_delete:
                efs_filesystem = filesystem["FileSystemId"]
                efs_filesystem_list.insert(0, efs_filesystem)
    return efs_filesystem_list
