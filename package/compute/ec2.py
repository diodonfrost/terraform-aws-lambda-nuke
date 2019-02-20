
"""This script nuke all ec2 resources"""

#import datetime
import time
import boto3

EC2 = boto3.client('ec2')

def nuke_all_ec2(older_than_seconds):
    """
        ec2 function for destroy all ec2 instances
        and launchtemplate resources
    """

    #### Nuke all ec2 instances ####
    # Initialize instance list
    instance_list = []
    reservations = EC2.describe_instances()
    time_delete = time.time() - older_than_seconds

    # list all instances
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:

            if instance['LaunchTime'].timestamp() < time_delete:

                # Retrieve ec2 instance id and add in list
                instance_id = instance['InstanceId']
                instance_list.insert(0, instance_id)

    if instance_list:
        # Nuke all instances
        EC2.terminate_instances(InstanceIds=instance_list)

    #### Nuke all launch templates ####
    response = EC2.describe_launch_templates()

    for launchtemplate in response['LaunchTemplates']:

        if launchtemplate['CreateTime'].timestamp() < time_delete:

            # Nuke all launch template
            EC2.delete_launch_template(LaunchTemplateId=launchtemplate['LaunchTemplateId'])

    #### Nuke all placement group ####
    response = EC2.describe_placement_groups()

    for placementgroup in response['PlacementGroups']:

        # Nuke all launch template
        EC2.delete_placement_group(GroupName=placementgroup['GroupName'])
