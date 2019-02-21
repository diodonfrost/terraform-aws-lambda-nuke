
"""This script nuke all ecr resources"""

import boto3

ECS = boto3.client('ecs')

def nuke_all_ecs():
    """
         ecs function for destroy all ecs clusyers
         and task definitions
    """

    #### Nuke all ecs resources ####
    response = ECS.describe_clusters()

    for cluster in response['clusters']:

        # Nuke all ecs cluster
        ECS.delete_cluster(cluster=cluster['clusterName'])
