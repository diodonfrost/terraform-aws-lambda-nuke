# -*- coding: utf-8 -*-

"""Module deleting all RDS resources."""

from typing import Iterator
from botocore.exceptions import ClientError, EndpointConnectionError
from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions
import boto3
import time


class NukeRds:
    """Abstract RDS nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize RDS nuke."""
        self.rds = AwsClient().connect("rds", region_name)
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')

        try:
            self.rds.describe_db_clusters()
        except EndpointConnectionError:
            print("RDS resource is not available in this AWS region")
            return

    def nuke(self, older_than_seconds: float, required_tags: dict = None) -> None:
        """RDS resources deleting function.

        Deleting all RDS resources with a timestamp greater than older_than_seconds.
        That include:
          - Aurora clusters
          - RDS instances
          - snapshots
          - subnets
          - param groups

        :param older_than_seconds:
            The timestamp in seconds used from which the AWS resource will be deleted
        :param required_tags:
            A dictionary of required tags to filter the RDS instances and clusters
        """
        for instance in self.list_instances(older_than_seconds, required_tags):
            try:
                self.rds.delete_db_instance(
                    DBInstanceIdentifier=instance, SkipFinalSnapshot=True
                )
                print(f"Deleted RDS instance {instance}")
            except ClientError as exc:
                if exc.response['Error']['Code'] == 'InvalidDBInstanceState':
                    print(f"RDS instance {instance} is already being deleted.")
                else:
                    nuke_exceptions("RDS instance", instance, exc)

        for cluster in self.list_clusters(older_than_seconds, required_tags):
            try:
                self.rds.delete_db_cluster(
                    DBClusterIdentifier=cluster, SkipFinalSnapshot=True
                )
                print(f"Deleted RDS cluster {cluster}")
            except ClientError as exc:
                if exc.response['Error']['Code'] == 'InvalidParameterCombination':
                    print(f"RDS cluster {cluster} has deletion protection enabled. Disabling protection.")
                    try:
                        self.rds.modify_db_cluster(
                            DBClusterIdentifier=cluster,
                            DeletionProtection=False
                        )
                        self.rds.delete_db_cluster(
                            DBClusterIdentifier=cluster, SkipFinalSnapshot=True
                        )
                        print(f"Deleted RDS cluster {cluster} after disabling deletion protection.")
                    except ClientError as inner_exc:
                        nuke_exceptions("RDS cluster", cluster, inner_exc)
                else:
                    nuke_exceptions("RDS cluster", cluster, exc)

    def list_instances(self, time_delete: float, required_tags: dict = None) -> Iterator[str]:
        """RDS instance list function.

        List IDs of all RDS instances with a timestamp lower than time_delete and not matching required tags.

        :param time_delete:
            Timestamp in seconds used to filter RDS instances
        :param required_tags:
            A dictionary of required tags to filter the RDS instances

        :yield Iterator[str]:
            RDS instances IDs
        """
        paginator = self.rds.get_paginator("describe_db_instances")

        for page in paginator.paginate():
            for instance in page["DBInstances"]:
                if "InstanceCreateTime" in instance and instance["InstanceCreateTime"].timestamp() < time_delete:
                    if required_tags and self.resource_has_tags(instance["DBInstanceIdentifier"], required_tags, "db-instance"):
                        continue
                    yield instance["DBInstanceIdentifier"]

    def list_clusters(self, time_delete: float, required_tags: dict = None) -> Iterator[str]:
        """Aurora cluster list function.

        List IDs of all Aurora clusters with a timestamp lower than time_delete and not matching required tags.

        :param time_delete:
            Timestamp in seconds used to filter Aurora clusters
        :param required_tags:
            A dictionary of required tags to filter the Aurora clusters

        :yield Iterator[str]:
            Aurora clusters IDs
        """
        paginator = self.rds.get_paginator("describe_db_clusters")

        for page in paginator.paginate():
            for cluster in page["DBClusters"]:
                if "ClusterCreateTime" in cluster and cluster["ClusterCreateTime"].timestamp() < time_delete:
                    if required_tags and self.resource_has_tags(cluster["DBClusterIdentifier"], required_tags, "db-cluster"):
                        continue
                    yield cluster["DBClusterIdentifier"]

    def resource_has_tags(self, resource_id: str, required_tags: dict, resource_type: str) -> bool:
        """Check if the resource has the required tags.

        :param resource_id:
            ID of the RDS resource
        :param required_tags:
            A dictionary of required tags to filter the RDS resources
        :param resource_type:
            The type of the RDS resource (either "db-instance" or "db-cluster")
        :return:
            True if the resource has any of the required tags, False otherwise
        """
        try:
            arn = f"arn:aws:rds:{self.rds.meta.region_name}:{self.account_id}:{resource_type}:{resource_id}"
            response = self.rds.list_tags_for_resource(ResourceName=arn)
            resource_tags = {tag["Key"]: tag["Value"] for tag in response["TagList"]}
            for key, value in required_tags.items():
                if resource_tags.get(key) == value:
                    return True
            return False
        except ClientError as exc:
            nuke_exceptions("RDS resource tagging", resource_id, exc)
            return False

