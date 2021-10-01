# -*- coding: utf-8 -*-
"""Module use by nuke unit tests."""

import boto3


def create_dynamodb(region_name):
    """Create dynamodb table."""
    client = boto3.client("dynamodb", region_name=region_name)

    client.create_table(
        TableName="table-test",
        KeySchema=[
            {"AttributeName": "UserId", "KeyType": "HASH"},
            {"AttributeName": "GameTitle", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "UserId", "AttributeType": "S"},
            {"AttributeName": "GameTitle", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 20,
            "WriteCapacityUnits": 20,
        },
    )


def create_redshift(region_name):
    """Create redshift cluster."""
    client = boto3.client("redshift", region_name=region_name)

    client.create_cluster(
        DBName="db-test",
        ClusterIdentifier="redshift-test",
        ClusterType="single-node",
        NodeType="ds2.xlarge",
        MasterUsername="user",
        MasterUserPassword="IamNotHere",
    )
