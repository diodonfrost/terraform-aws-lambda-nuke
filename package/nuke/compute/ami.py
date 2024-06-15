# -*- coding: utf-8 -*-

"""Module deleting all ec2 ami."""

from typing import Iterator, Dict
from botocore.exceptions import ClientError
from dateutil.parser import parse
from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions

class NukeAmi:
    """Abstract ec2 ami in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ec2 ami."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Ec2 ami deleting function.

        Deregister all ami present on the current aws account with a timestamp greater than
        older_than_seconds and not matching the required tags.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the AMIs to exclude from deletion
        """
        for ami_id in self.list_ami(older_than_seconds, required_tags):
            try:
                self.ec2.deregister_image(ImageId=ami_id)
                print(f"Nuke ami {ami_id}")
            except ClientError as exc:
                nuke_exceptions("ec2 ami", ami_id, exc)

    def list_ami(self, time_delete: float, required_tags: Dict[str, str] = None) -> Iterator[str]:
        """Ami volume list function.

        List the IDs of all AMI with a timestamp lower than time_delete and not matching required tags.

        :param int time_delete:
            Timestamp in seconds used to filter AMIs
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the AMIs to exclude from deletion

        :yield Iterator[str]:
            AMI IDs
        """
        amis_describe = self.ec2.describe_images(Owners=["self"])

        for ami in amis_describe["Images"]:
            get_date_obj = parse(ami["CreationDate"])
            date_obj = get_date_obj.replace(tzinfo=None).timestamp()
            if date_obj < time_delete:
                if required_tags and self._ami_has_required_tags(ami["ImageId"], required_tags):
                    continue
                yield ami["ImageId"]

    def _ami_has_required_tags(self, ami_id: str, required_tags: Dict[str, str]) -> bool:
        """Check if the AMI has the required tags.

        :param str ami_id:
            The ID of the AMI
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the AMI has all the required tags, False otherwise
        """
        try:
            response = self.ec2.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [ami_id]}]
            )
            ami_tags = {tag["Key"]: tag["Value"] for tag in response["Tags"]}
            for key, value in required_tags.items():
                if ami_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("ec2 ami tagging", ami_id, exc)
            return False

