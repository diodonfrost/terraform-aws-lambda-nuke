
"""This script nuke all autoscaling resources"""

import time
import boto3

LOADBALANCING = boto3.client('elbv2')

def nuke_all_loadbalancing(older_than_seconds, logger):
    """
        Function for destroy every loadbalancer and
        target groups aws resources
    """

    #### Nuke all autoscaling group ####
    response = LOADBALANCING.describe_load_balancers()
    time_delete = time.time() - older_than_seconds

    for loadbalancing in response['LoadBalancers']:

        if loadbalancing['CreatedTime'].timestamp() < time_delete:

            # Nuke all load balancer
            LOADBALANCING.delete_load_balancer(\
            LoadBalancerArn=loadbalancing['LoadBalancerArn'])
            logger.info("Nuke Load Balancer %s", loadbalancing['LoadBalancerArn'])


    #### Nuke all target group ####
    response = LOADBALANCING.describe_target_groups()

    for targetgroup in response['TargetGroups']:

        # Nuke all target group
        LOADBALANCING.delete_target_group(\
        TargetGroupArn=targetgroup['TargetGroupArn'])
        logger.info("Nuke Target Group %s", targetgroup['TargetGroupArn'])
