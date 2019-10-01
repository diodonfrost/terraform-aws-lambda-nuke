# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all aws resources."""
import os

from compute.autoscaling import NukeAutoscaling
from compute.ebs import NukeEbs
from compute.ec2 import NukeEc2
from compute.ecr import NukeEcr
from compute.eks import NukeEks
from compute.elasticbeanstalk import NukeElasticbeanstalk
from compute.elb import nuke_all_elb
from compute.key_pair import nuke_all_key_pair
from compute.spot import nuke_all_spot

from database.dynamodb import nuke_all_dynamodb
from database.elasticache import nuke_all_elasticache
from database.neptune import nuke_all_neptune
from database.rds import nuke_all_rds
from database.redshift import nuke_all_redshift

from governance.cloudwatch import nuke_all_cloudwatch

from network.eip import nuke_all_eip
from network.endpoint import nuke_all_endpoint
from network.security import nuke_all_network_security

from storage.efs import nuke_all_efs
from storage.glacier import nuke_all_glacier
from storage.s3 import nuke_all_s3

import timeparse
import time


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    exclude_resources = os.getenv("EXCLUDE_RESOURCES")
    # Older than date
    older_than = os.getenv("OLDER_THAN")
    # Convert older_than date to seconds
    older_than_seconds = time.time() - timeparse.timeparse(older_than)

    _strategy = {
        "autoscaling": NukeAutoscaling,
        "ebs": NukeEbs,
        "ec2": NukeEc2,
        "ecr": NukeEcr,
        "eks": NukeEks,
        "elasticbeanstalk": NukeElasticbeanstalk,
    }

    for key, value in _strategy.items():
        if key not in exclude_resources:
            strategy = value()
            strategy.nuke(older_than_seconds)

    aws_services = [
        "endpoint",
        "spot",
        "elb",
        "s3",
        "efs",
        "glacier",
        "rds",
        "dynamodb",
        "elasticache",
        "neptune",
        "redshift",
        "cloudwatch",
    ]

    aws_service_with_no_date = ["key_pair", "network_security", "eip"]

    for service in aws_services:
        if service not in exclude_resources:
            globals()["nuke_all_" + service](timeparse.timeparse(older_than))

    for service in aws_service_with_no_date:
        if service not in exclude_resources:
            globals()["nuke_all_" + service]()
