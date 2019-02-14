
"""This script nuke all ec2 resources"""

import boto3

EC2 = boto3.client('ec2')

def nuke_all_ec2():
    """ ec2 function for destroy every ec2 resources """

    # Initialize instance list
    instance_list = []
    reservations = EC2.describe_instances()

    # list all instances
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:

            # Retrieve ec2 instance id and add in list
            instance_id = instance['InstanceId']
            instance_list.insert(0, instance_id)

    if instance_list:
        # Nuke all instances
        EC2.terminate_instances(InstanceIds=instance_list)
