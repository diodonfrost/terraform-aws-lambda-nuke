"""This script nuke all ebs resources"""

import time
import boto3
from botocore.exceptions import ClientError


def nuke_all_ebs(older_than_seconds, logger):
    """
         ebs function for destroy all snapshots,
         volumes and lifecycle manager
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    ec2 = boto3.client('ec2')
    dlm = boto3.client('dlm')

    # List all ebs volumes
    ebs_volume_list = ebs_list_volumes(time_delete)

    # Nuke all volumes
    for volume in ebs_volume_list:

        # Nuke all ebs volume
        try:
            ec2.delete_volume(VolumeId=volume)
            print("Nuke EBS Volume %s", volume)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'VolumeInUse':
                logger.info("volume %s is already used", volume)
            elif error_code == 'InvalidVolume':
                logger.info("volume %s has already been deleted", volume)
            else:
                logger.error("Unexpected error: %s" % e)

    # List all dlm policies
    dlm_policy_list = dlm_list_policy(time_delete)

    # Nuke all ebs lifecycle manager
    for policy in dlm_policy_list:

        # Nuke all dlm lifecycle policy
        try:
            dlm.delete_lifecycle_policy(PolicyId=policy)
            print("Nuke EBS Lifecycle Policy %s", policy)
        except ClientError as e:
            logger.error("Unexpected error: %s" % e)


def ebs_list_volumes(time_delete):
    """
       Aws ebs list function, list name of
       all ebs volumes and return it in list.
    """

    # Define connection
    ec2 = boto3.client('ec2')

    # Paginator volume list
    paginator = ec2.get_paginator('describe_volumes')
    page_iterator = paginator.paginate()

    # Initialize ebs volume list
    ebs_volumes_list = []

    # Retrieve all volume ID in available state
    for page in page_iterator:
        for volume in page['Volumes']:
            if volume['CreateTime'].timestamp() < time_delete:

                # Retrieve and add in list ebs volume ID
                ebs_volume = volume['VolumeId']
                ebs_volumes_list.insert(0, ebs_volume)

    return ebs_volumes_list


def dlm_list_policy(time_delete):
    """
       Aws dlm list function, list name of
       all data lifecycle manager and return it in list.
    """

    # Define connection
    dlm = boto3.client('dlm')
    response = dlm.get_lifecycle_policies()

    # Initialize data lifecycle manager list
    dlm_policy_list = []

    # Retrieve dlm policies
    for policy in response['Policies']:
        detailed = dlm.get_lifecycle_policy(PolicyId=policy['PolicyId'])
        if detailed['Policy']['DateCreated'].timestamp() < time_delete:

            dlm_policy = policy['PolicyId']
            dlm_policy_list.insert(0, dlm_policy)

    return dlm_policy_list
