# -*- coding: utf-8 -*-
"""Module deleting all aws s3 bucket resources."""

from typing import Iterator, Dict
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import time

class NukeS3:
    """Abstract s3 nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize s3 nuke."""
        self.s3 = boto3.client("s3", region_name=region_name)
        self.s3_resource = boto3.resource("s3", region_name=region_name)

        try:
            self.s3.list_buckets()
        except EndpointConnectionError:
            print("s3 resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """S3 bucket deleting function.

        Deleting all s3 buckets with a timestamp greater than
        older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the S3 buckets to exclude from deletion
        """
        for s3_bucket in self.list_buckets(older_than_seconds, required_tags):
            try:
                # Delete all objects in bucket
                bucket = self.s3_resource.Bucket(s3_bucket)
                bucket.object_versions.delete()
                bucket.objects.delete()
            except ClientError as exc:
                print(f"Failed to delete objects in s3 bucket {s3_bucket}: {exc}")
                continue

            try:
                # Delete bucket
                self.s3.delete_bucket(Bucket=s3_bucket)
                print(f"Nuke s3 bucket {s3_bucket}")
            except ClientError as exc:
                print(f"Failed to delete s3 bucket {s3_bucket}: {exc}")

    def list_buckets(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """S3 bucket list function.

        List the names of all S3 buckets with
        a timestamp lower than time_delete and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filtering S3 buckets
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the S3 buckets to exclude from deletion

        :yield Iterator[str]:
            S3 buckets names
        """
        response = self.s3.list_buckets()

        for bucket in response["Buckets"]:
            bucket_name = bucket["Name"]
            if bucket["CreationDate"].timestamp() < time_delete:
                if required_tags and self._bucket_has_required_tags(bucket_name, required_tags):
                    continue
                yield bucket_name

    def _bucket_has_required_tags(self, bucket_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the bucket has the required tags.

        :param str bucket_name:
            The name of the S3 bucket
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the bucket has all the required tags, False otherwise
        """
        try:
            tags = self.s3.get_bucket_tagging(Bucket=bucket_name)
            tag_set = {tag['Key']: tag['Value'] for tag in tags.get('TagSet', [])}
            for key, value in required_tags.items():
                if tag_set.get(key) == value:
                    return True
            return False
        except ClientError as e:
            # If no tags found or any other error, return False
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                return False
            else:
                print(f"Failed to get tags for s3 bucket {bucket_name}: {e}")
                return False

# def main():
#     region_name = "ap-south-1"
#     older_than_seconds = time.time() - 60 
#     required_tags = {"dev": "develop"}

#     nuke_s3 = NukeS3(region_name)
#     nuke_s3.nuke(older_than_seconds, required_tags)

# if __name__ == "__main__":
#     main()
