
"""This script nuke all ecr resources"""

import time
import boto3

ECR = boto3.client('ecr')

def nuke_all_ecr(older_than_seconds, logger):
    """
         ecr function for destroy all ecr registry
    """

    #### Nuke all ecr repository ####
    response = ECR.describe_repositories()
    time_delete = time.time() - older_than_seconds

    for registry in response['repositories']:

        if registry['createdAt'].timestamp() < time_delete:

            # Nuke all ecr registry
            ECR.delete_repository(repositoryName=registry['repositoryName'], force=True)
            logger.info("Nuke ECR Registry %s", registry['repositoryName'])
