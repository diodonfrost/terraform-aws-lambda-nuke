
"""This script nuke all ecs resources"""

import boto3


def nuke_all_ecs(logger):
    """
         ecs function for destroy all ecs clusters
         and task definitions
    """

    # Define connection
    ecs = boto3.client('ecs')

    # List all ecs cluster
    ecs_cluster_list = ecs_list_clusters()

    # Nuke all ecs cluster
    for cluster in ecs_cluster_list:

        # Delete ecs cluster
        ecs.delete_cluster(cluster=cluster)
        logger.info("Nuke ECS Cluster %s", cluster)


def ecs_list_clusters():
    """
       Aws ecs container service, list name of
       all ecs cluster container and return it in list.
    """

    # Define the connection
    ecs = boto3.client('ecs')

    # Set paginator
    paginator = ecs.get_paginator('list_clusters')
    page_iterator = paginator.paginate()

    # Initialize ecs cluster list
    ecs_cluster_list = []

    # Retrieve all ecs cluster
    for page in page_iterator:
        for cluster in page['clusterArns']:

            ecs_cluster = cluster
            ecs_cluster_list.insert(0, ecs_cluster)

    return ecs_cluster_list
