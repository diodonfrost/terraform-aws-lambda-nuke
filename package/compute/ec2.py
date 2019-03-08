
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
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define the connection
    ec2 = boto3.client('ec2')

    # List all ec2 instances
    ec2_instance_list = ec2_list_instances(time_delete)

    try:
        ec2.terminate_instances(InstanceIds=ec2_instance_list)
        LOGGER.info("Terminate instances %s", ec2_instance_list)
    except ClientError:
        print('No instance found')

    # List all ec2 template
    ec2_template_list = ec2_list_templates(time_delete)

    # nuke all ec2 template Id
    for template in ec2_template_list:

        # Delete launch template
        ec2.delete_launch_template(LaunchTemplateId=template)
        logger.info("Nuke Launch Template %s", template)

    # List all ec2 placement group
    ec2_placement_group_list = ec2_list_placement_group()

    # Nuke all ec2 placement group
    for placementgroup in ec2_placement_group_list:

        # Delete ec2 placement group
        ec2.delete_placement_group(GroupName=placementgroup)
        logger.info("Nuke Placement Group %s", placementgroup)


def ec2_list_instances(time_delete):
    """
       Aws ec2 instance list function, list name of all ec2 instances
       all ec2 instances with specific tag and return it in list.
    """

    # Define the connection
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        Filters=[{'Name': 'instance-state-name', 'Values': ['pending',
                                                            'running',
                                                            'stopping',
                                                            'stopped']}])

    # Initialize instance list
    ec2_instance_list = []

    # Retrieve ec2 instances
    for page in page_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                if instance['LaunchTime'].timestamp() < time_delete:

                    # Retrieve ec2 instance id and add in list
                    ec2_instance_id = instance['InstanceId']
                    ec2_instance_list.insert(0, ec2_instance_id)

    return ec2_instance_list


def ec2_list_templates(time_delete):
    """
       Aws ec2 template list function, list name of
       all ec2 templates and return it in list.
    """

    # Define the connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_launch_templates()

    # Initialize ec2 template list
    ec2_template_list = []

    # Retrieve all ec2 template
    for template in response['LaunchTemplates']:
        if template['CreateTime'].timestamp() < time_delete:

            ec2_template = template['LaunchTemplateId']
            ec2_template_list.insert(0, ec2_template)

    return ec2_template_list


def ec2_list_placement_group():
    """
       Aws ec2 placement group list function, list name of
       all ec2 placement group and return it in list.
    """

    # Define the connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_placement_groups()

    # Initialize ec2 placement group list
    ec2_placement_group_list = []

    # Retrieve all ec2 placement groups
    for placementgroup in response['PlacementGroups']:

        ec2_placement_group = placementgroup['GroupName']
        ec2_placement_group_list.insert(0, ec2_placement_group)

    return ec2_placement_group_list
