# -*- coding: utf-8 -*-
"""Module use by nuke unit tests."""

import boto3


def create_glacier(region_name):
    """Create glacier vault."""
    client = boto3.client("glacier", region_name=region_name)
    client.create_vault(vaultName="glacier-test")


def create_s3(region_name):
    """Create s3 bucket."""
    client = boto3.client("s3", region_name=region_name)
    client_resource = boto3.resource('s3', region_name=region_name)
    client.create_bucket(Bucket="s3-test")
    file_content = b"This is a content file"
    s3_object = client_resource.Object("s3-test", "hello.txt")
    s3_object.put(Body=file_content)
