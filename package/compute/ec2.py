
"""This script nuke all ec2 resources"""

import logging
import time
import boto3
from botocore.exceptions import ClientError

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def nuke_all_ec2(older_than_seconds, logger):
    """
        ec2 function for destroy all ec2 instances
        and launchtemplate resources
    """

    # Define the connection
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        Filters=[{'Name': 'instance-state-name', 'Values': ['pending',
                                                            'running',
                                                            'stopping',
                                                            'stopped']}])
    time_delete = time.time() - older_than_seconds

    # Initialize instance list
    instance_list = []

    # list all instances
    for page in page_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                if instance['LaunchTime'].timestamp() < time_delete:
                    # Retrieve ec2 instance id and add in list
                    instance_id = instance['InstanceId']
                    instance_list.insert(0, instance_id)

        if instance_list:
            # Nuke all instances
            try:
                ec2.terminate_instances(InstanceIds=instance_list)
                LOGGER.info("Terminate instances %s", instance_list)
            except ClientError:
                print('No instance found')

    # Nuke all launch templates
    response = ec2.describe_launch_templates()

    for launchtemplate in response['LaunchTemplates']:
        if launchtemplate['CreateTime'].timestamp() < time_delete:

            # Nuke all launch template
            ec2.delete_launch_template(LaunchTemplateId=launchtemplate['LaunchTemplateId'])
            logger.info("Nuke Launch Template %s", launchtemplate['LaunchTemplateId'])

    # Nuke all placement group
    response = ec2.describe_placement_groups()

    for placementgroup in response['PlacementGroups']:
        # Nuke all launch template
        ec2.delete_placement_group(GroupName=placementgroup['GroupName'])
        logger.info("Nuke Placement Group %s", placementgroup['GroupName'])
