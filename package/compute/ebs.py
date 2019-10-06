# -*- coding: utf-8 -*-

"""Module deleting all aws ebs volume and dlm policie resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeEbs:
    """Abstract ebs nuke in a class."""

    def __init__(self):
        """Initialize ebs nuke."""
        self.ec2 = boto3.client("ec2")
        self.dlm = boto3.client("dlm")

        try:
            self.dlm.get_lifecycle_policies()
        except EndpointConnectionError:
            print("Dlm resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """Ebs and dlm policies deleting function.

        Deleting all ebs volumes and dlm policy resources with
        a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for volume in self.list_ebs(older_than_seconds):
            try:
                self.ec2.delete_volume(VolumeId=volume)
                print("Nuke EBS Volume {0}".format(volume))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "VolumeInUse":
                    logging.info("volume %s is already used", volume)
                elif error_code == "InvalidVolume":
                    logging.info("volume %s has already been deleted", volume)
                else:
                    logging.error("Unexpected error: %s", e)

        # Deletes snpashot lifecyle policy
        for policy in self.list_policy(older_than_seconds):
            try:
                self.dlm.delete_lifecycle_policy(PolicyId=policy)
                print("Nuke EBS Lifecycle Policy {0}".format(policy))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_ebs(self, time_delete):
        """Ebs volume list function.

        List the IDs of all ebs volumes with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter ebs volumes

        :yield Iterator[str]:
            Ebs volumes IDs
        """
        paginator = self.ec2.get_paginator("describe_volumes")

        for page in paginator.paginate():
            for volume in page["Volumes"]:
                if volume["CreateTime"].timestamp() < time_delete:
                    yield volume["VolumeId"]

    def list_policy(self, time_delete):
        """Data Lifecycle Policies list function.

        Returns the IDs of all Data Lifecycle Policies with
        a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Data Lifecycle policies

        :yield Iterator[str]:
            Data Lifecycle policies IDs
        """
        response = self.dlm.get_lifecycle_policies()

        for policy in response["Policies"]:
            detailed = self.dlm.get_lifecycle_policy(
                PolicyId=policy["PolicyId"]
            )
            if detailed["Policy"]["DateCreated"].timestamp() < time_delete:
                yield policy["PolicyId"]
