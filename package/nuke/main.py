# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all aws resources."""
import os
import time

from nuke.compute.autoscaling import NukeAutoscaling
from nuke.compute.dlm import NukeDlm
from nuke.compute.ebs import NukeEbs
from nuke.compute.ec2 import NukeEc2
from nuke.compute.ecr import NukeEcr
from nuke.compute.eks import NukeEks
from nuke.compute.elasticbeanstalk import NukeElasticbeanstalk
from nuke.compute.elb import NukeElb
from nuke.compute.key_pair import NukeKeypair
from nuke.compute.spot import NukeSpot
from nuke.database.dynamodb import NukeDynamodb
from nuke.database.elasticache import NukeElasticache
from nuke.database.rds import NukeRds
from nuke.database.redshift import NukeRedshift
from nuke.governance.cloudwatch import NukeCloudwatch
from nuke.network.eip import NukeEip
from nuke.network.endpoint import NukeEndpoint
from nuke.network.security import NukeNetworksecurity
from nuke.storage.efs import NukeEfs
from nuke.storage.glacier import NukeGlacier
from nuke.storage.s3 import NukeS3
from nuke.timeparse import timeparse


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    exclude_resources = os.getenv("EXCLUDE_RESOURCES", "no_value")
    # Older than date
    older_than = os.getenv("OLDER_THAN")
    # Convert older_than date to seconds
    older_than_seconds = time.time() - timeparse(older_than)

    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")

    _strategy = {
        "autoscaling": NukeAutoscaling,
        "dlm": NukeDlm,
        "ebs": NukeEbs,
        "ec2": NukeEc2,
        "ecr": NukeEcr,
        "eks": NukeEks,
        "elasticbeanstalk": NukeElasticbeanstalk,
        "elb": NukeElb,
        "spot": NukeSpot,
        "dynamodb": NukeDynamodb,
        "elasticache": NukeElasticache,
        "rds": NukeRds,
        "redshift": NukeRedshift,
        "cloudwatch": NukeCloudwatch,
        "endpoint": NukeEndpoint,
        "efs": NukeEfs,
        "glacier": NukeGlacier,
        "s3": NukeS3,
    }

    _strategy_with_no_date = {
        "eip": NukeEip,
        "key_pair": NukeKeypair,
        "network_security": NukeNetworksecurity,
    }

    for key, value in _strategy.items():
        if key not in exclude_resources:
            for aws_region in aws_regions:
                strategy = value(region_name=aws_region)
                strategy.nuke(older_than_seconds)

    for key, value in _strategy_with_no_date.items():
        if key not in exclude_resources:
            for aws_region in aws_regions:
                strategy = value(region_name=aws_region)
                strategy.nuke()
