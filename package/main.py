"""Main entrypoint function for destroy all aws resources"""

import logging
import os
import timeparse
import compute.ec2
import compute.autoscaling
import compute.loadbalancing
import compute.ebs
import compute.key_pair

exclude_resources = os.getenv('EXCLUDE_RESOURCES', 'none')
older_than = os.getenv('OLDER_THAN', 'none')

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def lambda_handler(event, context):
    """ Main function entrypoint for lambda """

    # Convert older_than variable to seconds
    older_than_seconds = timeparse.timeparse(older_than)

    if "ec2" not in exclude_resources:
        compute.ec2.nuke_all_ec2(older_than_seconds)

    if "autoscaling" not in exclude_resources:
        compute.autoscaling.nuke_all_autoscaling(older_than_seconds)

    if "loadbalancing" not in exclude_resources:
        compute.loadbalancing.nuke_all_loadbalancing(older_than_seconds)

    if "ebs" not in exclude_resources:
        compute.ebs.nuke_all_ebs(older_than_seconds)

    if "key_pair" not in exclude_resources:
        compute.key_pair.nuke_all_key_pair()
