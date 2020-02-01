# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all aws resources."""
import os

from compute.autoscaling import NukeAutoscaling
from compute.dlm import NukeDlm
from compute.ebs import NukeEbs
from compute.ec2 import NukeEc2
from compute.ecr import NukeEcr
from compute.eks import NukeEks
from compute.elasticbeanstalk import NukeElasticbeanstalk
from compute.elb import NukeElb
from compute.key_pair import NukeKeypair
from compute.spot import NukeSpot

from database.dynamodb import NukeDynamodb
from database.elasticache import NukeElasticache
from database.rds import NukeRds
from database.redshift import NukeRedshift

from governance.cloudwatch import NukeCloudwatch

from network.eip import NukeEip
from network.endpoint import NukeEndpoint
from network.security import NukeNetworksecurity

from storage.efs import NukeEfs
from storage.glacier import NukeGlacier
from storage.s3 import NukeS3

import timeparse
import time


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    exclude_resources = os.getenv("EXCLUDE_RESOURCES", "no_value")
    # Older than date
    older_than = os.getenv("OLDER_THAN")
    # Convert older_than date to seconds
    older_than_seconds = time.time() - timeparse.timeparse(older_than)

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
