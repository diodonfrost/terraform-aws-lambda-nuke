"""This script nuke all dax resources"""

import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_dax(logger):
    """
         dax function for destroy all dax database
    """
    # define connection
    dax = boto3.client('dax')

    # Test if dax services is present in current aws region
    try:
        dax.describe_clusters()
    except EndpointConnectionError:
        print('dax resource is not available in this aws region')
        return

    # List all dax clusters
    dax_cluster_list = dax_list_clusters()

    # Nuke all dax clusters
    for cluster in dax_cluster_list:

        try:
            dax.delete_cluster(ClusterName=cluster)
            logger.info("Nuke dax cluster %s", cluster)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidDBInstanceState':
                logger.info("dax cluster %s is not in state started", cluster)
            else:
                print("Unexpected error: %s" % e)

    # List all dax subnets
    dax_subnet_list = dax_list_subnet()

    # Nuke all dax subnets
    for subnet in dax_subnet_list:

        try:
            dax.delete_subnet_group(SubnetGroupName=subnet)
            logger.info("Nuke dax subnet %s", subnet)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterValueException':
                logger.info("default is reserved and cannot be modified.")
            else:
                print("Unexpected error: %s" % e)

    # List all dax parameters
    dax_param_list = dax_list_params()

    # Nuke all dax parameters
    for param in dax_param_list:

        try:
            dax.delete_parameter_group(ParameterGroupName=param)
            logger.info("Nuke dax param %s", param)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterValueException':
                logger.info("%s cannot be modified.", param)
            else:
                print("Unexpected error: %s" % e)


def dax_list_clusters():
    """
       Aws dax list clusters, list name of
       all dax clusters and return it in list.
    """

    # define connection
    dax = boto3.client('dax')
    response = dax.describe_clusters()

    # Initialize dax cluster list
    dax_cluster_list = []

    # Retrieve all dax cluster name
    for cluster in response['Clusters']:

        dax_cluster = cluster['ClusterName']
        dax_cluster_list.insert(0, dax_cluster)

    return dax_cluster_list


def dax_list_subnet():
    """
       Aws dax list subnets, list name of
       all dax subnets and return it in list.
    """

    # define connection
    dax = boto3.client('dax')
    response = dax.describe_subnet_groups()

    # Initialize dax subnet list
    dax_subnet_list = []

    # Retrieve all dax subnet name
    for subnet in response['SubnetGroups']:

        dax_subnet = subnet['SubnetGroupName']
        dax_subnet_list.insert(0, dax_subnet)

    return dax_subnet_list


def dax_list_params():
    """
       Aws dax list parameters, list name of
       all dax parameters and return it in list.
    """

    # define connection
    dax = boto3.client('dax')
    response = dax.describe_parameter_groups()

    # Initialize dax parameters list
    dax_param_list = []

    # Retrieve all dax parameters name
    for param in response['ParameterGroups']:

        dax_param = param['ParameterGroupName']
        dax_param_list.insert(0, dax_param)

    return dax_param_list
