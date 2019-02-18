
"""This script nuke all autoscaling resources"""

#import datetime
import time
import boto3

AUTOSCALING = boto3.client('autoscaling')

def nuke_all_autoscaling(older_than_seconds):
    """
        Function for destroy every autoscaling,
        launch_configuration aws resources
    """

    #### Nuke all autoscaling group ####
    response = AUTOSCALING.describe_auto_scaling_groups()
    time_delete = time.time() - older_than_seconds

    for autoscaling in response['AutoScalingGroups']:

        if autoscaling['CreatedTime'].timestamp() < time_delete:

            # Nuke autoscaling group
            AUTOSCALING.delete_auto_scaling_group(\
            AutoScalingGroupName=autoscaling['AutoScalingGroupName'], ForceDelete=True)


    #### Nuke all launch configuration ####
    response = AUTOSCALING.describe_launch_configurations()

    for launchconfiguration in response['LaunchConfigurations']:

        if launchconfiguration['CreatedTime'].timestamp() < time_delete:

            # Nuke launch configuration
            AUTOSCALING.delete_launch_configuration(\
            LaunchConfigurationName=launchconfiguration['LaunchConfigurationName'])
