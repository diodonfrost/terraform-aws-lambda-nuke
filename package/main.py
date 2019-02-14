"""Main entrypoint function for destroy all aws resources"""

import logging
import os
import ec2

aws_resources = os.getenv('AWS_RESOURCES', 'tostop')
aws_regions = os.getenv('AWS_REGIONS', '*')
older_than = os.getenv('OLDER_THAN', 'none')

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def lambda_handler(event, context):
    """ Main function entrypoint for lambda """

    if aws_resources == "*":
        ec2.nuke_all_ec2()
