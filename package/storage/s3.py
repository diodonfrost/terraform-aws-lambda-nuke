# -*- coding: utf-8 -*-

"""Module deleting all aws s3 bucket resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_s3(older_than_seconds):
    """S3 bucket deleting function.

    Deleting all s3 buckets with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds
    s3 = boto3.client("s3")
    s3_resource = boto3.resource("s3")

    # Test if s3 is available
    try:
        s3.list_buckets()
    except EndpointConnectionError:
        print("s3 resource is not available in this aws region")
        return

    for s3_bucket in s3_list_buckets(time_delete):
        try:
            # Delete all objects in bucket
            bucket = s3_resource.Bucket(s3_bucket)
            for key in bucket.objects.all():
                key.delete()

            # Delete bucket
            s3.delete_bucket(Bucket=s3_bucket)
            print("Nuke s3 bucket {0}".format(s3_bucket))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDenied":
                logging.warning("Protected policy enable on %s", s3_bucket)
            else:
                logging.error("Unexpected error: %s", e)


def s3_list_buckets(time_delete):
    """S3 bucket list function.

    List the names of all S3 buckets with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter S3 buckets
    :returns:
        List of S3 buckets names
    :rtype:
        [str]
    """
    s3_bucket_list = []
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    for bucket in response["Buckets"]:
        if bucket["CreationDate"].timestamp() < time_delete:
            s3_bucket_list.append(bucket["Name"])
    return s3_bucket_list
