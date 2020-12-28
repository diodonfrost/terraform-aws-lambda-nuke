# -*- coding: utf-8 -*-

"""Module deleting all ec2 ami."""

from typing import Iterator

from botocore.exceptions import ClientError

from dateutil.parser import parse

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeAmi:
    """Abstract ec2 ami in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ec2 ami."""
        self.ec2 = AwsClient().connect("ec2", region_name)

    def nuke(self, older_than_seconds) -> None:
        """Ec2 ami deleting function.

        Deregister all ami present on the current aws account.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for ami_id in self.list_ami(older_than_seconds):
            try:
                self.ec2.deregister_image(ImageId=ami_id)
                print("Nuke ami {0}".format(ami_id))
            except ClientError as exc:
                nuke_exceptions("ec2 ami", ami_id, exc)

    def list_ami(self, time_delete: float) -> Iterator[str]:
        """Ami volume list function.

        List the IDs of all AMI with a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter AMI

        :yield Iterator[str]:
            AMI IDs
        """
        amis_describe = self.ec2.describe_images(Owners=["self"])

        for ami in amis_describe["Images"]:
            get_date_obj = parse(ami["CreationDate"])
            date_obj = get_date_obj.replace(tzinfo=None).timestamp()
            if date_obj < time_delete:
                yield ami["ImageId"]
