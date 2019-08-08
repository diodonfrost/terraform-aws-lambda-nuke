# -*- coding: utf-8 -*-

"""Module deleting all dynamodb tables and backups."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_dynamodb(older_than_seconds):
    """Dynamodb table and backup deleting function.

    Deleting all dynamodb table and backup with
    a timestamp greater than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    dynamodb = boto3.client("dynamodb")

    # Test if dynamodb services is present in current aws region
    try:
        dynamodb.list_tables()
    except EndpointConnectionError:
        print("dynamodb resource is not available in this aws region")
        return

    # List all dynamodb tables
    dynamodb_table_list = dynamodb_list_tables(time_delete)

    # Nuke all dynamodb tables
    for table in dynamodb_table_list:

        # Delete dynamodb table
        try:
            dynamodb.delete_table(TableName=table)
            print("Nuke rds table{0}".format(table))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # List all dynamodb backup
    dynamodb_table_backup = dynamodb_list_backups(time_delete)

    # Nuke all dynamodb backup
    for backup in dynamodb_table_backup:

        # Delete dynamodb backup
        try:
            dynamodb.delete_backup(BackupArn=backup)
            print("Nuke rds backup {0}".format(backup))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def dynamodb_list_tables(time_delete):
    """Dynamodb table list function.

    List names of all dynamodb tables with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter dynamodb tables
    :returns:
        List of dynamodb tables names
    :rtype:
        [str]
    """
    # define connection
    dynamodb = boto3.client("dynamodb")

    # Define the connection
    paginator = dynamodb.get_paginator("list_tables")
    page_iterator = paginator.paginate()

    # Initialize dynamodb table list
    dynamodb_table_list = []

    # Retrieve all dynamodb table name
    for page in page_iterator:
        for table in page["TableNames"]:
            table_desc = dynamodb.describe_table(TableName=table)
            if (
                    table_desc["Table"][
                        "CreationDateTime"].timestamp() < time_delete
            ):

                dynamodb_table = table
                dynamodb_table_list.insert(0, dynamodb_table)

    return dynamodb_table_list


def dynamodb_list_backups(time_delete):
    """Dynamodb backup list function.

    List arn of all dynamodb backup with a timestamp
    lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter dynamodb backup
    :returns:
        List of dynamodb backup arn
    :rtype:
        [str]
    """
    # define connection
    dynamodb = boto3.client("dynamodb")

    # Define the connection
    paginator = dynamodb.get_paginator("list_backups")
    page_iterator = paginator.paginate()

    # Initialize dynamodb backup list
    dynamodb_backup_list = []

    # Retrieve all dynamodb backup name
    for page in page_iterator:
        for backup in page["BackupSummaries"]:
            backup_desc = dynamodb.describe_backup(
                BackupArn=backup["BackupArn"]
            )
            if (
                    backup_desc["BackupDescription"]["BackupDetails"][
                        "BackupCreationDateTime"].timestamp() < time_delete
            ):

                dynamodb_backup = backup["BackupArn"]
                dynamodb_backup_list.insert(0, dynamodb_backup)

    return dynamodb_backup_list
