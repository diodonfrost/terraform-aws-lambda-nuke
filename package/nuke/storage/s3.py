# -*- coding: utf-8 -*-

"""Module deleting all aws s3 bucket resources."""

from typing import Iterator

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.client_connections import AwsResource
from nuke.exceptions import nuke_exceptions


class NukeS3:
    """Abstract s3 nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize s3 nuke."""
        self.s3 = AwsClient().connect("s3", region_name)
        self.s3_resource = AwsResource().connect("s3", region_name)

        try:
            self.s3.list_buckets()
        except EndpointConnectionError:
            print("s3 resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float) -> None:
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
            except ClientError as exc:
                nuke_exceptions("s3 object", s3_bucket, exc)

            try:
                # Delete bucket
                self.s3.delete_bucket(Bucket=s3_bucket)
                print("Nuke s3 bucket {0}".format(s3_bucket))
            except ClientError as exc:
                nuke_exceptions("s3 bucket", s3_bucket, exc)

    def list_buckets(self, time_delete: float) -> Iterator[str]:
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
