"""This script nuke all s3 bucket"""

import time
import boto3


def nuke_all_s3(older_than_seconds, logger):
    """
         s3 function for nuke all s3 buckets
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    s3 = boto3.client('s3')

    # List all s3 bucket names
    s3_bucket_list = s3_list_buckets(time_delete)

    # Nuke all s3 buckets
    for bucket in s3_bucket_list:

        # Delete bucket policy
        s3.delete_bucket_policy(Bucket=bucket)

        # Delete bucket
        s3.delete_bucket(Bucket=bucket)
        logger.info("Nuke s3 bucket %s", bucket)


def s3_list_buckets(time_delete):
    """
       Aws s3 list bucket, list name of
       all s3 buckets and return it in list.
    """

    # Define the connection
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Initialize s3 bucket list
    s3_bucket_list = []

    # Retrieve all s3 bucket names
    for bucket in response['Buckets']:
        if bucket['CreationDate'].timestamp() < time_delete:

            s3_bucket = bucket['Name']
            s3_bucket_list.insert(0, s3_bucket)

    return s3_bucket_list
