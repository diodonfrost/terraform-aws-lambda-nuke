# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all AWS resources."""
import os
import time

from nuke.analytic.emr import NukeEmr
from nuke.analytic.kafka import NukeKafka
from nuke.compute.ami import NukeAmi
from nuke.compute.autoscaling import NukeAutoscaling
from nuke.compute.dlm import NukeDlm
from nuke.compute.ebs import NukeEbs
from nuke.compute.ec2 import NukeEc2
from nuke.compute.ecr import NukeEcr
from nuke.compute.eks import NukeEks
from nuke.compute.elasticbeanstalk import NukeElasticbeanstalk
from nuke.compute.elb import NukeElb
from nuke.compute.key_pair import NukeKeypair
from nuke.compute.snapshot import NukeSnapshot
from nuke.compute.spot import NukeSpot
from nuke.database.dynamodb import NukeDynamodb
from nuke.database.elasticache import NukeElasticache
from nuke.database.rds import NukeRds
from nuke.database.redshift import NukeRedshift
from nuke.governance.cloudwatch import NukeCloudwatch
from nuke.network.eip import NukeEip
from nuke.network.endpoint import NukeEndpoint
from nuke.network.network_acl import NukeNetworkAcl
from nuke.network.security_group import NukeSecurityGroup
from nuke.storage.efs import NukeEfs
from nuke.storage.glacier import NukeGlacier
from nuke.storage.s3 import NukeS3
from nuke.timeparse import timeparse


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    exclude_resources = os.getenv("EXCLUDE_RESOURCES", "no_value")
    target_resource = os.getenv("TARGET_RESOURCE", "").lower()
    if not target_resource:
        raise ValueError("TARGET_RESOURCE environment variable is not set")

    # Older than date
    older_than = os.getenv("OLDER_THAN")
    # Convert older_than date to seconds
    older_than_seconds = time.time() - timeparse(older_than)

    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")

    _strategy = {
        "ami": NukeAmi,
        "ebs": NukeEbs,
        "snapshot": NukeSnapshot,
        "ec2": NukeEc2,
        "spot": NukeSpot,
        "endpoint": NukeEndpoint,
        "ecr": NukeEcr,
        "emr": NukeEmr,
        "kafka": NukeKafka,
        "autoscaling": NukeAutoscaling,
        "dlm": NukeDlm,
        "eks": NukeEks,
        "elasticbeanstalk": NukeElasticbeanstalk,
        "elb": NukeElb,
        "dynamodb": NukeDynamodb,
        "elasticache": NukeElasticache,
        "rds": NukeRds,
        "redshift": NukeRedshift,
        "cloudwatch": NukeCloudwatch,
        "efs": NukeEfs,
        "glacier": NukeGlacier,
        "s3": NukeS3,
    }

    _strategy_with_no_date = {
        "eip": NukeEip,
        "key_pair": NukeKeypair,
        "security_group": NukeSecurityGroup,
        "network_acl": NukeNetworkAcl,
    }

    # Process target resource
    if target_resource in _strategy:
        for aws_region in aws_regions:
            strategy = _strategy[target_resource](region_name=aws_region)
            strategy.nuke(older_than_seconds)
    elif target_resource in _strategy_with_no_date:
        if older_than_seconds <= 0:
            for aws_region in aws_regions:
                strategy = _strategy_with_no_date[target_resource](region_name=aws_region)
                strategy.nuke()
    else:
        raise ValueError(f"Unknown TARGET_RESOURCE: {target_resource}")
# -*- coding: utf-8 -*-

"""Main entrypoint function for destroy all AWS resources."""
import os
import time

from nuke.analytic.emr import NukeEmr
from nuke.analytic.kafka import NukeKafka
from nuke.compute.ami import NukeAmi
from nuke.compute.autoscaling import NukeAutoscaling
from nuke.compute.dlm import NukeDlm
from nuke.compute.ebs import NukeEbs
from nuke.compute.ec2 import NukeEc2
from nuke.compute.ecr import NukeEcr
from nuke.compute.eks import NukeEks
from nuke.compute.elasticbeanstalk import NukeElasticbeanstalk
from nuke.compute.elb import NukeElb
from nuke.compute.key_pair import NukeKeypair
from nuke.compute.snapshot import NukeSnapshot
from nuke.compute.spot import NukeSpot
from nuke.database.dynamodb import NukeDynamodb
from nuke.database.elasticache import NukeElasticache
from nuke.database.rds import NukeRds
from nuke.database.redshift import NukeRedshift
from nuke.governance.cloudwatch import NukeCloudwatch
from nuke.network.eip import NukeEip
from nuke.network.endpoint import NukeEndpoint
from nuke.network.network_acl import NukeNetworkAcl
from nuke.network.security_group import NukeSecurityGroup
from nuke.storage.efs import NukeEfs
from nuke.storage.glacier import NukeGlacier
from nuke.storage.s3 import NukeS3
from nuke.timeparse import timeparse


def lambda_handler(event, context):
    """Main function entrypoint for lambda."""
    exclude_resources = os.getenv("EXCLUDE_RESOURCES", "no_value")
    target_resource = os.getenv("TARGET_RESOURCE", "").lower()
    if not target_resource:
        raise ValueError("TARGET_RESOURCE environment variable is not set")

    # Older than date
    older_than = os.getenv("OLDER_THAN")
    # Convert older_than date to seconds
    older_than_seconds = time.time() - timeparse(older_than)

    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")

    _strategy = {
        "ami": NukeAmi,
        "ebs": NukeEbs,
        "snapshot": NukeSnapshot,
        "ec2": NukeEc2,
        "spot": NukeSpot,
        "endpoint": NukeEndpoint,
        "ecr": NukeEcr,
        "emr": NukeEmr,
        "kafka": NukeKafka,
        "autoscaling": NukeAutoscaling,
        "dlm": NukeDlm,
        "eks": NukeEks,
        "elasticbeanstalk": NukeElasticbeanstalk,
        "elb": NukeElb,
        "dynamodb": NukeDynamodb,
        "elasticache": NukeElasticache,
        "rds": NukeRds,
        "redshift": NukeRedshift,
        "cloudwatch": NukeCloudwatch,
        "efs": NukeEfs,
        "glacier": NukeGlacier,
        "s3": NukeS3,
    }

    _strategy_with_no_date = {
        "eip": NukeEip,
        "key_pair": NukeKeypair,
        "security_group": NukeSecurityGroup,
        "network_acl": NukeNetworkAcl,
    }

    # Process target resource
    if target_resource in _strategy:
        for aws_region in aws_regions:
            strategy = _strategy[target_resource](region_name=aws_region)
            strategy.nuke(older_than_seconds)
    elif target_resource in _strategy_with_no_date:
        if older_than_seconds <= 0:
            for aws_region in aws_regions:
                strategy = _strategy_with_no_date[target_resource](region_name=aws_region)
                strategy.nuke()
    else:
        raise ValueError(f"Unknown TARGET_RESOURCE: {target_resource}")
