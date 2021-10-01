# -*- coding: utf-8 -*-
"""Module use by nuke unit tests."""

import boto3


def create_emr(region_name):
    """Create emr cluster."""
    client = boto3.client("emr", region_name=region_name)
    az = region_name + "a"
    client.run_job_flow(
        Instances={
            "InstanceCount": 3,
            "KeepJobFlowAliveWhenNoSteps": True,
            "MasterInstanceType": "c3.medium",
            "Placement": {"AvailabilityZone": az},
            "SlaveInstanceType": "c3.xlarge",
        },
        JobFlowRole="EMR_EC2_DefaultRole",
        LogUri="s3://mybucket/log",
        Name="cluster",
        ServiceRole="EMR_DefaultRole",
        VisibleToAllUsers=True,
    )
