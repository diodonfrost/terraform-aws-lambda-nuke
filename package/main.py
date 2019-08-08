# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all aws resources."""
import os

from compute.autoscaling import nuke_all_autoscaling
from compute.ebs import nuke_all_ebs
from compute.ec2 import nuke_all_ec2
from compute.ecr import nuke_all_ecr
from compute.eks import nuke_all_eks
from compute.elb import nuke_all_elb
from compute.elbv2 import nuke_all_elbv2
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

    if "endpoint" not in exclude_resources:
        nuke_all_endpoint(older_than_seconds)

    if "ec2" not in exclude_resources:
        nuke_all_ec2(older_than_seconds)

    if "spot" not in exclude_resources:
        nuke_all_spot(older_than_seconds)

    if "autoscaling" not in exclude_resources:
        nuke_all_autoscaling(older_than_seconds)

    if "elb" not in exclude_resources:
        nuke_all_elb(older_than_seconds)
        nuke_all_elbv2(older_than_seconds)

    if "key_pair" not in exclude_resources:
        nuke_all_key_pair()

    if "ecr" not in exclude_resources:
        nuke_all_ecr(older_than_seconds)

    if "eks" not in exclude_resources:
        nuke_all_eks(older_than_seconds)

    if "s3" not in exclude_resources:
        nuke_all_s3(older_than_seconds)

    if "efs" not in exclude_resources:
        nuke_all_efs(older_than_seconds)

    if "glacier" not in exclude_resources:
        nuke_all_glacier(older_than_seconds)

    if "rds" not in exclude_resources:
        nuke_all_rds(older_than_seconds)

    if "dynamodb" not in exclude_resources:
        nuke_all_dynamodb(older_than_seconds)

    if "elasticache" not in exclude_resources:
        nuke_all_elasticache(older_than_seconds)

    if "neptune" not in exclude_resources:
        nuke_all_neptune(older_than_seconds)

    if "redshift" not in exclude_resources:
        nuke_all_redshift(older_than_seconds)

    if "ebs" not in exclude_resources:
        nuke_all_ebs(older_than_seconds)

    if "network_security" not in exclude_resources:
        nuke_all_network_security()

    if "eip" not in exclude_resources:
        nuke_all_eip()
