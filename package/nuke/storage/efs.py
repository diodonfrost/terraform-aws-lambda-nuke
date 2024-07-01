from typing import Iterator, Dict
from botocore.exceptions import ClientError, EndpointConnectionError
from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions
import time

class NukeEfs:
    """Abstract efs nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize efs nuke."""
        self.efs = AwsClient().connect("efs", region_name)

        try:
            self.efs.describe_file_systems()
        except EndpointConnectionError:
            print("EFS resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """EFS deleting function.

        Deleting all efs with a timestamp greater than older_than_seconds
        and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EFS
            resources to exclude from deletion
        """
        for efs_file_system in self.list_file_systems(older_than_seconds, required_tags):
            try:
                self.retry_delete_mount_targets(efs_file_system)
                self.efs.delete_file_system(FileSystemId=efs_file_system)
                print("Nuke EFS share {0}".format(efs_file_system))
            except ClientError as exc:
                nuke_exceptions("efs filesystem", efs_file_system, exc)

    def list_file_systems(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """EFS list function.

        List IDs of all efs with a timestamp lower than time_delete
        and not matching the required tags.

        :param int time_delete:
            Timestamp in seconds used for filter efs
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the EFS
            resources to exclude from deletion

        :yield Iterator[str]:
            EFS IDs
        """
        paginator = self.efs.get_paginator("describe_file_systems")

        for page in paginator.paginate():
            for filesystem in page["FileSystems"]:
                if filesystem["CreationTime"].timestamp() < time_delete:
                    if required_tags and self._filesystem_has_required_tags(filesystem["FileSystemId"], required_tags):
                        continue
                    yield filesystem["FileSystemId"]

    def _filesystem_has_required_tags(self, filesystem_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the EFS filesystem has the required tags.

        :param str filesystem_id:
            The ID of the EFS filesystem
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the EFS filesystem has all the required tags, False otherwise
        """
        try:
            tags = self.efs.describe_tags(FileSystemId=filesystem_id)
            tags_dict = {tag['Key']: tag['Value'] for tag in tags['Tags']}
            for key, value in required_tags.items():
                if tags_dict.get(key) != value:
                    return False
            return True
        except ClientError as e:
            print(f"Failed to get tags for EFS filesystem {filesystem_id}: {e}")
            return False

    def delete_mount_targets(self, filesystem_id: str) -> None:
        """Delete all mount targets for the given EFS filesystem.

        :param str filesystem_id:
            The ID of the EFS filesystem
        """
        try:
            mount_targets = self.efs.describe_mount_targets(FileSystemId=filesystem_id)
            for mount_target in mount_targets["MountTargets"]:
                self.efs.delete_mount_target(MountTargetId=mount_target["MountTargetId"])
                print(f"Deleted mount target {mount_target['MountTargetId']} for EFS filesystem {filesystem_id}")
        except ClientError as e:
            print(f"Failed to delete mount targets for EFS filesystem {filesystem_id}: {e}")

    def retry_delete_mount_targets(self, filesystem_id: str, retries: int = 3, delay: int = 5) -> None:
        """Retry deleting mount targets for a given EFS filesystem.

        :param str filesystem_id:
            The ID of the EFS filesystem
        :param int retries:
            Number of retries
        :param int delay:
            Delay between retries in seconds
        """
        for _ in range(retries):
            self.delete_mount_targets(filesystem_id)
            time.sleep(delay)
            mount_targets = self.efs.describe_mount_targets(FileSystemId=filesystem_id)
            if not mount_targets["MountTargets"]:
                return
        raise Exception(f"Failed to delete all mount targets for EFS filesystem {filesystem_id} after {retries} retries")
