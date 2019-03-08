
"""This script nuke all ebs resources"""

import time
import boto3


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
        ec2.delete_volume(VolumeId=volume)
        logger.info("Nuke EBS Volume %s", volume)

    # Nuke all snapshots
#    response = ec2.describe_snapshots()

#
#    for snapshot in response['Snapshots']:
#        print(snapshot)
#        if snapshot['StartTime'].timestamp() < time_delete and \
#        snapshot['OwnerAlias'] == 'self':
#
#            # Nuke all ebs volume
#            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

    # List all dlm policies
    dlm_policy_list = dlm_list_policy(time_delete)

    # Nuke all ebs lifecycle manager
    for policy in dlm_policy_list:

        # Nuke all ebs volume
        dlm.delete_lifecycle_policy(PolicyId=policy)
        logger.info("Nuke EBS Lifecycle Policy %s", policy)


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
            if volume['State'] == 'available':
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

    # Paginator dlm list
    response = dlm.get_lifecycle_policies()

    # Initialize data lifecycle manager list
    dlm_policy_list = []

    # Retrieve dlm policies
    for policy in response['Policies']:
        detailed = dlm.get_lifecycle_policy(PolicyId=policy)
        if detailed['Policy']['DateCreated'].timestamp() < time_delete:

            dlm_policy = dlm['PolicyId']
            dlm_policy_list.insert(0, dlm_policy)

    return dlm_policy_list
