# -*- coding: utf-8 -*-

"""Module deleting all aws s3 bucket resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeS3:
    """Abstract s3 nuke in a class."""

    def __init__(self, region_name=None):
        """Initialize s3 nuke."""
        if region_name:
            self.s3 = boto3.client("s3", region_name=region_name)
            self.s3_resource = boto3.resource("s3", region_name=region_name)
        else:
            self.s3 = boto3.client("s3")
            self.s3_resource = boto3.resource("s3")

        try:
            self.s3.list_buckets()
        except EndpointConnectionError:
            print("s3 resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """S3 bucket deleting function.

        Deleting all s3 buckets with a timestamp greater than
        older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        for s3_bucket in self.list_buckets(older_than_seconds):
            try:
                # Delete all objects in bucket
                bucket = self.s3_resource.Bucket(s3_bucket)
                bucket.object_versions.delete()
                bucket.objects.delete()
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

            try:
                # Delete bucket
                self.s3.delete_bucket(Bucket=s3_bucket)
                print("Nuke s3 bucket {0}".format(s3_bucket))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "AccessDenied":
                    logging.warning("Protected policy enable on %s", s3_bucket)
                else:
                    logging.error("Unexpected error: %s", e)

    def list_buckets(self, time_delete):
        """S3 bucket list function.

        List the names of all S3 buckets with
        a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter S3 buckets

        :yield Iterator[str]:
            S3 buckets names
        """
        response = self.s3.list_buckets()

        for bucket in response["Buckets"]:
            if bucket["CreationDate"].timestamp() < time_delete:
                yield bucket["Name"]
