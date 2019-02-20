
"""This script nuke all ebs resources"""

#import datetime
import time
import boto3

EC2 = boto3.client('ec2')
DLM = boto3.client('dlm')

def nuke_all_ebs(older_than_seconds):
    """
         ebs function for destroy all snapshots,
         volumes and lifecycle manager
    """

    #### Nuke all volumes ####
    response = EC2.describe_volumes()
    time_delete = time.time() - older_than_seconds

    for volume in response['Volumes']:

        if volume['CreateTime'].timestamp() < time_delete:

            # Nuke all ebs volume
            EC2.delete_volume(VolumeId=volume['VolumeId'])

    #### Nuke all snapshots ####
#    response = EC2.describe_snapshots()

#
#    for snapshot in response['Snapshots']:
#        print(snapshot)
#        if snapshot['StartTime'].timestamp() < time_delete and \
#        snapshot['OwnerAlias'] == 'self':
#
#            # Nuke all ebs volume
#            EC2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

    #### Nuke all ebs lifecycle manager ####
    response = DLM.get_lifecycle_policies()

    for ebslifecycle in response['Policies']:

        detailedresponse = DLM.get_lifecycle_policy(PolicyId=ebslifecycle['PolicyId'])

        if detailedresponse['Policy']['DateCreated'].timestamp() < time_delete:

            # Nuke all ebs volume
            DLM.delete_lifecycle_policy(PolicyId=detailedresponse['Policy']['PolicyId'])
