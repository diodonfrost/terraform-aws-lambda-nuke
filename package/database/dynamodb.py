"""This script nuke all dynamodb resources"""

import time
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError


def nuke_all_dynamodb(older_than_seconds, logger):
    """
         dynamodb function for destroy all dynamodb database
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # define connection
    dynamodb = boto3.client('dynamodb')

    # Test if dynamodb services is present in current aws region
    try:
        dynamodb.list_tables()
    except EndpointConnectionError:
        print('dynamodb resource is not available in this aws region')
        return

    # List all dynamodb tables
    dynamodb_table_list = dynamodb_list_tables(time_delete)

    # Nuke all dynamodb tables
    for table in dynamodb_table_list:

        dynamodb.delete_table(TableName=table)
        logger.info("Nuke rds table %s", table)

    # List all dynamodb backup
    dynamodb_table_backup = dynamodb_list_backups(time_delete)

    # Nuke all dynamodb backup
    for backup in dynamodb_table_backup:

        dynamodb.delete_backup(BackupArn=backup)
        logger.info("Nuke rds backup %s", backup)


def dynamodb_list_tables(time_delete):
    """
       Aws dynamodb list tables, list name of
       all dynamodb tables and return it in list.
    """

    # define connection
    dynamodb = boto3.client('dynamodb')

    # Define the connection
    paginator = dynamodb.get_paginator('list_tables')
    page_iterator = paginator.paginate()

    # Initialize dynamodb table list
    dynamodb_table_list = []

    # Retrieve all dynamodb table name
    for page in page_iterator:
        for table in page['TableNames']:
            table_desc = dynamodb.describe_table(TableName=table)
            if table_desc['Table']['CreationDateTime'].timestamp() < time_delete:

                dynamodb_table = table
                dynamodb_table_list.insert(0, dynamodb_table)

    return dynamodb_table_list


def dynamodb_list_backups(time_delete):
    """
       Aws dynamodb list backups, list name of
       all dynamodb backups and return it in list.
    """

    # define connection
    dynamodb = boto3.client('dynamodb')

    # Define the connection
    paginator = dynamodb.get_paginator('list_backups')
    page_iterator = paginator.paginate()

    # Initialize dynamodb backup list
    dynamodb_backup_list = []

    # Retrieve all dynamodb backup name
    for page in page_iterator:
        for backup in page['BackupSummaries']:
            backup_desc = dynamodb.describe_backup(BackupArn=backup['BackupArn'])
            if backup_desc['BackupDescription']['BackupDetails']['BackupCreationDateTime'].timestamp() < time_delete:

                dynamodb_backup = backup['BackupArn']
                dynamodb_backup_list.insert(0, dynamodb_backup)

    return dynamodb_backup_list
