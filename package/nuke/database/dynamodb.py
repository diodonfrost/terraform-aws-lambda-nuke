from typing import Iterator, Dict
from botocore.exceptions import ClientError, EndpointConnectionError
from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions

class NukeDynamodb:
    """Abstract dynamodb nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize dynamodb nuke."""
        self.dynamodb = AwsClient().connect("dynamodb", region_name)

        try:
            self.dynamodb.list_tables()
        except EndpointConnectionError:
            print("Dynamodb resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Dynamodb table and backup deleting function.

        Deleting all dynamodb table and backup with a timestamp greater
        than older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the DynamoDB tables to exclude from deletion
        """
        for table in self.list_tables(older_than_seconds):
            if required_tags and self._table_has_required_tags(table, required_tags):
                continue
            try:
                self.dynamodb.delete_table(TableName=table)
                print(f"Nuke dynamodb table {table}")
            except ClientError as exc:
                nuke_exceptions("dynamodb table", table, exc)

        for backup in self.list_backups(older_than_seconds):
            if required_tags and self._backup_has_required_tags(backup, required_tags):
                continue
            try:
                self.dynamodb.delete_backup(BackupArn=backup)
                print(f"Nuke dynamodb backup {backup}")
            except ClientError as exc:
                nuke_exceptions("dynamodb backup", backup, exc)

    def list_tables(self, time_delete: float) -> Iterator[str]:
        """Dynamodb table list function.

        List names of all dynamodb tables with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter dynamodb tables

        :yield Iterator[str]:
            Dynamodb tables names
        """
        paginator = self.dynamodb.get_paginator("list_tables")

        for page in paginator.paginate():
            for table in page["TableNames"]:
                table_desc = self.dynamodb.describe_table(TableName=table)
                date_table = table_desc["Table"]["CreationDateTime"]
                if date_table.timestamp() < time_delete:
                    yield table

    def list_backups(self, time_delete: float) -> Iterator[str]:
        """Dynamodb backup list function.

        List arn of all dynamodb backup with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter dynamodb backup

        :yield Iterator[str]:
            Dynamodb backup arn
        """
        paginator = self.dynamodb.get_paginator("list_backups")

        for page in paginator.paginate():
            for backup in page["BackupSummaries"]:
                backup_desc = self.dynamodb.describe_backup(BackupArn=backup["BackupArn"])
                desc = backup_desc["BackupDetails"]
                if desc["BackupCreationDateTime"].timestamp() < time_delete:
                    yield backup["BackupArn"]

    def _table_has_required_tags(self, table_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the DynamoDB table has the required tags.

        :param str table_name:
            The name of the DynamoDB table
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the table has all the required tags, False otherwise
        """
        try:
            tags = self.dynamodb.list_tags_of_resource(ResourceArn=f"arn:aws:dynamodb:*:*:table/{table_name}")
            tag_map = {tag["Key"]: tag["Value"] for tag in tags.get("Tags", [])}
            for key, value in required_tags.items():
                if tag_map.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for DynamoDB table {table_name}: {e}")
            return False

    def _backup_has_required_tags(self, backup_arn: str, required_tags: Dict[str, str]) -> bool:
        """Check if the DynamoDB backup has the required tags.

        :param str backup_arn:
            The ARN of the DynamoDB backup
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the backup has all the required tags, False otherwise
        """
        try:
            tags = self.dynamodb.list_tags_of_resource(ResourceArn=backup_arn)
            tag_map = {tag["Key"]: tag["Value"] for tag in tags.get("Tags", [])}
            for key, value in required_tags.items():
                if tag_map.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for DynamoDB backup {backup_arn}: {e}")
            return False
