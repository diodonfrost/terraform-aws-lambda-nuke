"""This script nuke all elasticache resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_elasticache(older_than_seconds, logger):
    """
         elasticache function for destroy all elasticache cluster
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    elasticache = boto3.client('elasticache')

    # Test if elasticache resources is present in current aws region
    try:
        elasticache.describe_cache_clusters()
    except EndpointConnectionError:
        print('elasticache resource is not available in this aws region')
        return

    # List all elasticache clusters
    elasticache_cluster_list = elasticache_list_cluster(time_delete)

    # Nuke all elasticache clusters
    for cluster in elasticache_cluster_list:

        try:
            elasticache.delete_cache_cluster(CacheClusterId=cluster)
            logger.info("Nuke elasticache cluster %s", cluster)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidCacheClusterState':
                logger.info("elasticache cluster %s is not in state available", cluster)
            else:
                print("Unexpected error: %s" % e)


def elasticache_list_cluster(time_delete):
    """
       Aws elasticache list clusters, list name of
       all elasticache clusters and return it in list.
    """

    # define connection
    elasticache = boto3.client('elasticache')

    # Define the connection
    paginator = elasticache.get_paginator('describe_cache_clusters')
    page_iterator = paginator.paginate()

    # Initialize elasticache file system list
    elasticache_cluster_list = []

    # Retrieve all elasticache file system Id
    for page in page_iterator:
        for cluster in page['CacheClusters']:
            if cluster['CacheClusterCreateTime'].timestamp() < time_delete:

                elasticache_cluster = cluster['CacheClusterId']
                elasticache_cluster_list.insert(0, elasticache_cluster)

    return elasticache_cluster_list
