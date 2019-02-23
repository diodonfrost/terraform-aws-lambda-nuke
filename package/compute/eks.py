
"""This script nuke all eks resources"""

import time
import boto3

EKS = boto3.client('eks')

def nuke_all_eks(older_than_seconds, logger):
    """
         eks function for destroy all kubernetes clusters
    """

    #### Nuke all ecr repository ####
    response = EKS.list_clusters()
    time_delete = time.time() - older_than_seconds

    for kubernetes in response['clusters']:

        cluster = EKS.describe_cluster(name=kubernetes)
        if cluster['cluster']['createdAt'].timestamp() < time_delete:

            # Nuke all ecr registry
            EKS.delete_cluster(name=cluster['cluster']['name'])
            logger.info("Nuke EKS Cluster %s", cluster['cluster']['name'])
