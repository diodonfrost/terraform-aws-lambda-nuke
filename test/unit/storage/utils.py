"""Module use by nuke unit tests."""

import boto3


def create_glacier(region_name):
    """Create glacier vault."""
    client = boto3.client("glacier", region_name=region_name)
    client.create_vault(vaultName="glacier-test")


def create_s3(region_name):
    """Create s3 bucket."""
    client = boto3.client("s3", region_name=region_name)
    client.create_bucket(Bucket="s3-test")
