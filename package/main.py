# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all aws resources."""
import os

from compute.autoscaling import nuke_all_autoscaling
from compute.ebs import nuke_all_ebs
from compute.ec2 import nuke_all_ec2
from compute.ecr import nuke_all_ecr
from compute.eks import nuke_all_eks
from compute.elasticbeanstalk import nuke_all_elasticbeanstalk
from compute.elb import nuke_all_elb
from compute.key_pair import nuke_all_key_pair
from compute.spot import nuke_all_spot

from database.dynamodb import nuke_all_dynamodb
from database.elasticache import nuke_all_elasticache
from database.neptune import nuke_all_neptune
from database.rds import nuke_all_rds
from database.redshift import nuke_all_redshift

from network.eip import nuke_all_eip
from network.endpoint import nuke_all_endpoint
from network.security import nuke_all_network_security

from storage.efs import nuke_all_efs
from storage.glacier import nuke_all_glacier
from storage.s3 import nuke_all_s3

import timeparse

exclude_resources = os.getenv("EXCLUDE_RESOURCES", "none")
older_than = os.getenv("OLDER_THAN", "none")


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    # Convert older_than variable to seconds
    older_than_seconds = timeparse.timeparse(older_than)

    aws_services = [
        "endpoint",
        "ec2",
        "spot",
        "autoscaling",
        "elb",
        "ecr",
        "eks",
        "elasticbeanstalk",
        "s3",
        "efs",
        "glacier",
        "rds",
        "dynamodb",
        "elasticache",
        "neptune",
        "redshift",
        "ebs",
    ]

    aws_service_with_no_date = ["key_pair", "network_security", "eip"]

    for service in aws_services:
        if service not in exclude_resources:
            globals()["nuke_all_" + service](older_than_seconds)

    for service in aws_service_with_no_date:
        if service not in exclude_resources:
            globals()["nuke_all_" + service]()
