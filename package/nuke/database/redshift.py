# -*- coding: utf-8 -*-

"""Module deleting all redshift resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeRedshift:
    """Abstract redshift nuke in a class."""

    def __init__(self, region_name=None):
        """Initialize redshift nuke."""
        if region_name:
            self.redshift = boto3.client("redshift", region_name=region_name)
        else:
            self.redshift = boto3.client("redshift")

        try:
            self.redshift.describe_clusters()
        except EndpointConnectionError:
            print("Redshift resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """Redshift resources deleting function.

        Deleting all redshift resources with
        a timestamp greater than older_than_seconds.
        That include:
          - clusters
          - snapshots
          - subnets
          - param groups

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        self.nuke_clusters(older_than_seconds)
        self.nuke_snapshots(older_than_seconds)
        self.nuke_subnets()
        self.nuke_param_groups()

    def nuke_clusters(self, time_delete):
        """Redshift cluster deleting function.

        Deleting redshift clusters with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for cluster in self.list_clusters(time_delete):
            try:
                self.redshift.delete_cluster(
                    ClusterIdentifier=cluster, SkipFinalClusterSnapshot=True
                )
                print("Nuke redshift cluster{0}".format(cluster))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidClusterStateFault":
                    logging.info(
                        "redshift cluster %s is not in state started", cluster
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_snapshots(self, time_delete):
        """Redshift snapshot deleting function.

        Deleting redshift snapshots with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for snapshot in self.list_snapshots(time_delete):
            try:
                self.redshift.delete_cluster_snapshot(
                    SnapshotIdentifier=snapshot
                )
                print("Nuke redshift snapshot {0}".format(snapshot))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidClusterSnapshotStateFault":
                    logging.info(
                        "redshift snap %s is not in state available", snapshot
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_subnets(self):
        """Redshift subnet deleting function.

        Deleting redshift subnets with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for subnet in self.list_subnet():
            try:
                self.redshift.delete_cluster_subnet_group(
                    ClusterSubnetGroupName=subnet
                )
                print("Nuke redshift subnet {0}".format(subnet))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidClusterSubnetGroupStateFault":
                    logging.info(
                        "redshift subnet %s is not in state available", subnet
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_param_groups(self):
        """Redshift parameter group deleting function.

        Deleting redshift parameter groups with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for param in self.list_cluster_params():
            try:
                self.redshift.delete_cluster_parameter_group(
                    ParameterGroupName=param
                )
                print("Nuke redshift param {0}".format(param))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidClusterParameterGroupStateFault":
                    logging.info(
                        "redshift param %s is not in state available", param
                    )
                elif error_code == "InvalidParameterValue":
                    logging.info(
                        "default %s parameter group cannot be deleted", param
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def list_clusters(self, time_delete):
        """Redshift cluster list function.

        List IDs of all redshift cluster with a timestamp lower than
        time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter redshift cluster

        :yield Iterator[str]:
            Redshift cluster IDs
        """
        paginator = self.redshift.get_paginator("describe_clusters")

        for page in paginator.paginate():
            for cluster in page["Clusters"]:
                if cluster["ClusterCreateTime"].timestamp() < time_delete:
                    yield cluster["ClusterIdentifier"]

    def list_snapshots(self, time_delete):
        """Redshift snapshot list function.

        List IDs of all redshift snapshots with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter redshift snapshots

        :yield Iterator[str]:
            Redshift snapshots IDs
        """
        paginator = self.redshift.get_paginator("describe_cluster_snapshots")

        for page in paginator.paginate():
            for snapshot in page["Snapshots"]:
                if snapshot["SnapshotCreateTime"].timestamp() < time_delete:
                    yield snapshot["SnapshotIdentifier"]

    def list_subnet(self):
        """Redshift subnet list function.

        :yield Iterator[str]:
            Redshift subnet names
        """
        paginator = self.redshift.get_paginator(
            "describe_cluster_subnet_groups"
        )

        for page in paginator.paginate():
            for subnet in page["ClusterSubnetGroups"]:
                yield subnet["ClusterSubnetGroupName"]

    def list_cluster_params(self):
        """Redshift cluster parameter list function.

        :yield Iterator[str]:
            Redshift cluster parameter names
        """
        paginator = self.redshift.get_paginator(
            "describe_cluster_parameter_groups"
        )

        for page in paginator.paginate():
            for param in page["ParameterGroups"]:
                yield param["ParameterGroupName"]
