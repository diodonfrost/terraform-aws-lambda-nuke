"""Main entrypoint function for destroy all aws resources"""

import logging
import os
import timeparse

from compute.ec2 import nuke_all_ec2
from compute.autoscaling import nuke_all_autoscaling
from compute.loadbalancing import nuke_all_loadbalancing
from compute.ebs import nuke_all_ebs
from compute.key_pair import nuke_all_key_pair
from compute.ecr import nuke_all_ecr
from compute.ecs import nuke_all_ecs
from compute.eks import nuke_all_eks
from storage.s3 import nuke_all_s3
from storage.efs import nuke_all_efs
from storage.glacier import nuke_all_glacier
from database.rds import nuke_all_rds
from database.dynamodb import nuke_all_dynamodb

exclude_resources = os.getenv('EXCLUDE_RESOURCES', 'none')
older_than = os.getenv('OLDER_THAN', 'none')

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def lambda_handler(event, context):
    """ Main function entrypoint for lambda """

    # Convert older_than variable to seconds
    older_than_seconds = timeparse.timeparse(older_than, LOGGER)

    if "ec2" not in exclude_resources:
        nuke_all_ec2(older_than_seconds, LOGGER)

    if "autoscaling" not in exclude_resources:
        nuke_all_autoscaling(older_than_seconds, LOGGER)

    if "loadbalancing" not in exclude_resources:
        nuke_all_loadbalancing(older_than_seconds, LOGGER)

    if "ebs" not in exclude_resources:
        nuke_all_ebs(older_than_seconds, LOGGER)

    if "key_pair" not in exclude_resources:
        nuke_all_key_pair(LOGGER)

    if "ecr" not in exclude_resources:
        nuke_all_ecr(older_than_seconds, LOGGER)

    if "ecs" not in exclude_resources:
        nuke_all_ecs(LOGGER)

    if "eks" not in exclude_resources:
        nuke_all_eks(older_than_seconds, LOGGER)

    if "s3" not in exclude_resources:
        nuke_all_s3(older_than_seconds, LOGGER)

    if "efs" not in exclude_resources:
        nuke_all_efs(older_than_seconds, LOGGER)

    if "glacier" not in exclude_resources:
        nuke_all_glacier(LOGGER)

    if "rds" not in exclude_resources:
        nuke_all_rds(older_than_seconds, LOGGER)

    if "dynamodb" not in exclude_resources:
        nuke_all_dynamodb(older_than_seconds, LOGGER)
