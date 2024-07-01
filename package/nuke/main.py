# -- coding: utf-8 --

"""Main entrypoint function for destroy all AWS resources."""
import os
import time
import sys
from inspect import signature

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

if 1:
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

    def call_nuke(strategy, older_than_seconds, tag_dict):
        """Call the nuke method with the appropriate arguments."""
        nuke_method = strategy.nuke
        sig = signature(nuke_method)
        if 'required_tags' in sig.parameters:
            nuke_method(older_than_seconds, required_tags=tag_dict)
        else:
            nuke_method(older_than_seconds)

    def lambda_handler(event=None, context=None):
        """Main function entrypoint for lambda."""
        exclude_resources = os.getenv("EXCLUDE_RESOURCES", "").replace(" ", "").split(",")
        include_resources = os.getenv("INCLUDE_RESOURCES", "").replace(" ", "").split(",")
        
        older_than = os.getenv("OLDER_THAN", "0d")
        older_than_seconds = time.time() - timeparse(older_than)

        aws_regions = os.getenv("AWS_REGIONS", "").replace(" ", "").split(",")
        if not aws_regions:
            raise ValueError("AWS_REGIONS environment variable is not set or empty.")
        
        required_tags = os.getenv("REQUIRED_TAGS", "")
        tag_dict = dict(tag.split("=") for tag in required_tags.split(",") if "=" in tag)

        _strategy = {
            "ami": NukeAmi,
            "ebs": NukeEbs,
            "snapshot": NukeSnapshot,
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
            "redshift": NukeRedshift,
            "cloudwatch": NukeCloudwatch,
            "efs": NukeEfs,
            "glacier": NukeGlacier,
            "ec2": NukeEc2,
            "rds": NukeRds,
            "s3": NukeS3,
        }

        _strategy_with_no_date = {
            "eip": NukeEip,
            "key_pair": NukeKeypair,
            "security_group": NukeSecurityGroup,
            "network_acl": NukeNetworkAcl,
        }

        # Ensure lists are not empty or contain empty strings
        include_resources = [res for res in include_resources if res]
        exclude_resources = [res for res in exclude_resources if res]

        if include_resources:
            for aws_region in aws_regions:
                for key, value in _strategy.items():
                    if key in include_resources:
                        strategy = value(region_name=aws_region)
                        call_nuke(strategy, older_than_seconds, tag_dict)

            no_older_than = any(s == "0" for s in older_than)
            for aws_region in aws_regions:
                for key, value in _strategy_with_no_date.items():
                    if key in include_resources and no_older_than:
                        strategy = value(region_name=aws_region)
                        strategy.nuke()

        elif exclude_resources:
            for aws_region in aws_regions:
                for key, value in _strategy.items():
                    if key not in exclude_resources:
                        strategy = value(region_name=aws_region)
                        call_nuke(strategy, older_than_seconds, tag_dict)

            no_older_than = any(s == "0" for s in older_than)
            for aws_region in aws_regions:
                for key, value in _strategy_with_no_date.items():
                    if key not in exclude_resources and no_older_than:
                        strategy = value(region_name=aws_region)
                        strategy.nuke()
