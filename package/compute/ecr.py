"""This script nuke all ecr resources"""

import logging
import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_ecr(older_than_seconds):
    """
         ecr function for destroy all ecr registry
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define the connection
    ecr = boto3.client('ecr')

    try:
        ecr.describe_repositories()
    except EndpointConnectionError:
        print('ecr resource is not available in this aws region')
        return

    # List all ecr registry
    ecr_registry_list = ecr_list_registry(time_delete)

    # Nuke all ecr registry
    for registry in ecr_registry_list:

        # Delete ecr registry
        try:
            ecr.delete_repository(repositoryName=registry, force=True)
            print("Nuke ECR Registry{0}".format(registry))
        except ClientError as e:
            logging.error("Unexpected error: %s" % e)


def ecr_list_registry(time_delete):
    """
       Aws ecr registry, list name of
       all ecr container registries and return it in list.
    """

    # Define the connection
    ecr = boto3.client('ecr')
    paginator = ecr.get_paginator('describe_repositories')
    page_iterator = paginator.paginate()

    # Initialize ecr registry list
    ecr_registry_list = []

    # Retrieve all ecr registry
    for page in page_iterator:
        for registry in page['repositories']:
            if registry['createdAt'].timestamp() < time_delete:

                ecr_registry = registry['repositoryName']
                ecr_registry_list.insert(0, ecr_registry)

    return ecr_registry_list
