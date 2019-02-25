"""This script nuke all s3 bucket"""

import time
import boto3

S3 = boto3.client('s3')

def nuke_all_s3(older_than_seconds, logger):
    """
         s3 function for nuke all s3 buckets
    """

    #### Nuke all s3 bucket ####
    response = S3.list_buckets()
    time_delete = time.time() - older_than_seconds

    for bucket in response['Buckets']:

        if bucket['CreationDate'].timestamp() < time_delete:

            # Delete Bucket policy
            S3.delete_bucket_policy(Bucket=bucket['Name'])

            # Nuke all ecr registry
            S3.delete_bucket(Bucket=bucket['Name'])
            logger.info("Nuke s3 bucket %s", bucket['Name'])
