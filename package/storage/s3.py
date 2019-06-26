"""This script nuke all s3 bucket"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_s3(older_than_seconds, logger):
    """
         s3 function for nuke all s3 buckets
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    # Test if s3 is available
    try:
        s3.list_buckets()
    except EndpointConnectionError:
        print('s3 resource is not available in this aws region')
        return

    # List all s3 bucket names
    s3_bucket_list = s3_list_buckets(time_delete)

    # Nuke all s3 buckets
    for s3_bucket in s3_bucket_list:

        try:
            # Delete all objects in bucket
            bucket = s3_resource.Bucket(s3_bucket)
            for key in bucket.objects.all():
                key.delete()

            # Delete bucket
            s3.delete_bucket(Bucket=s3_bucket)
            print("Nuke s3 bucket {0}".format(s3_bucket))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDenied':
                logger.warning("Protected policy enable on %s", s3_bucket)
            else:
                logger.error("Unexpected error: %s" % e)


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
