# -*- coding: utf-8 -*-

"""Module deleting all neptune resources."""

import logging

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


class NukeNeptune:
    """Abstract neptune nuke in a class."""

    def __init__(self):
        """Initialize neptune nuke."""
        self.neptune = boto3.client("neptune")

        try:
            self.neptune.describe_db_clusters()
        except EndpointConnectionError:
            print("neptune resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds):
        """Neptune resources deleting function.

        Deleting all neptune resources with
        a timestamp greater than older_than_seconds.
        That include:
          - clusters
          - instances
          - snapshots
          - subnets
          - param groups
          - cluster params

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws
            resource will be deleted
        """
        self.nuke_instances(older_than_seconds)
        self.nuke_clusters(older_than_seconds)
        self.nuke_snapshots(older_than_seconds)
        self.nuke_subnets()
        self.nuke_cluster_params()
        self.nuke_group_params()

    def nuke_instances(self, time_delete):
        """Neptune resources deleting function.

        Deleting neptune instances with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for instance in self.list_instances(time_delete):
            try:
                self.neptune.delete_db_instance(
                    DBInstanceIdentifier=instance, SkipFinalSnapshot=True
                )
                print("Nuke neptune instance {0}".format(instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBInstanceState":
                    logging.info(
                        "neptune instance %s is already being deleted",
                        instance,
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_clusters(self, time_delete):
        """Neptune cluster deleting function.

        Deleting neptune clusters with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for cluster in self.list_clusters(time_delete):
            try:
                self.neptune.delete_db_cluster(
                    DBClusterIdentifier=cluster, SkipFinalSnapshot=True
                )
                print("Nuke neptune cluster {0}".format(cluster))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBClusterStateFault":
                    logging.info(
                        "neptune cluster %s is not in started state", cluster
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_snapshots(self, time_delete):
        """Neptune snapshot deleting function.

        Deleting neptune snapshots with a timestamp lower than
        time_delete.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        """
        for snapshot in self.list_snapshots(time_delete):
            try:
                self.neptune.delete_db_cluster_snapshot(
                    DBClusterSnapshotIdentifier=snapshot
                )
                print("Nuke neptune snapshot{0}".format(snapshot))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def nuke_subnets(self):
        """Neptune subnet deleting function."""
        for subnet in self.list_subnet():
            try:
                self.neptune.delete_db_subnet_group(DBSubnetGroupName=subnet)
                print("Nuke neptune subnet {0}".format(subnet))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBSubnetGroupStateFault":
                    logging.info(
                        "%s is reserved and cannot be modified.", subnet
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_cluster_params(self):
        """Neptune cluster params function."""
        for param in self.list_cluster_params():
            try:
                self.neptune.delete_db_cluster_parameter_group(
                    DBClusterParameterGroupName=param
                )
                print("Nuke neptune param {0}".format(param))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBParameterGroupState":
                    logging.info(
                        "%s is reserved and cannot be modified.", param
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def nuke_group_params(self):
        """Neptune group parameter function."""
        for param in self.list_params():
            try:
                self.neptune.delete_db_parameter_group(
                    DBParameterGroupName=param
                )
                print("Nuke neptune param {0}".format(param))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBParameterGroupState":
                    logging.info(
                        "%s is reserved and cannot be modified.", param
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    def list_instances(self, time_delete):
        """Neptune instance list function.

        List IDs of all neptune instances with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter neptune instances

        :return list instance_list:
            List of neptune instances IDs
        """
        instance_list = []
        response = self.neptune.describe_db_instances()

        for instance in response["DBInstances"]:
            if instance["InstanceCreateTime"].timestamp() < time_delete:
                instance_list.append(instance["DBInstanceIdentifier"])
        return instance_list

    def list_clusters(self, time_delete):
        """Neptune cluster list function.

        List IDs of all neptune clusters with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter neptune clusters

        :return list cluster_list:
            List of neptune clusters IDs
        """
        cluster_list = []
        response = self.neptune.describe_db_clusters()

        for cluster in response["DBClusters"]:
            if cluster["ClusterCreateTime"].timestamp() < time_delete:
                cluster_list.append(cluster["DBClusterIdentifier"])
        return cluster_list

    def list_snapshots(self, time_delete):
        """Neptune snapshot list function.

        List IDs of all neptune snapshots with a timestamp
        lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter neptune snapshots

        :return list snapshot_list:
            List of neptune snapshots IDs
        """
        snapshot_list = []
        response = self.neptune.describe_db_cluster_snapshots()

        for snapshot in response["DBClusterSnapshots"]:
            if snapshot["SnapshotCreateTime"].timestamp() < time_delete:
                snapshot_list.append(snapshot["DBClusterSnapshotIdentifier"])
        return snapshot_list

    def list_subnet(self):
        """Neptune subnet list function.

        List neptune subnet names

        :return list subnet_list:
            List of neptune subnet names
        """
        subnet_list = []
        paginator = self.neptune.get_paginator("describe_db_subnet_groups")

        for page in paginator.paginate():
            for subnet in page["DBSubnetGroups"]:
                subnet_list.append(subnet["DBSubnetGroupName"])
        return subnet_list

    def list_cluster_params(self):
        """Neptune cluster param list function.

        List neptune cluster param names

        :return list cluster_param_list:
            List of neptune cluster param names
        """
        cluster_param_list = []
        response = self.neptune.describe_db_cluster_parameter_groups()

        for param in response["DBClusterParameterGroups"]:
            cluster_param_list.append(param["DBClusterParameterGroupName"])
        return cluster_param_list

    def list_params(self):
        """Neptune parameter group list function.

        List neptune param names

        :return list param_group_list:
            List of neptune param names
        """
        param_list = []
        paginator = self.neptune.get_paginator("describe_db_parameter_groups")

        for page in paginator.paginate():
            for param in page["DBParameterGroups"]:
                param_list.append(param["DBParameterGroupName"])
        return param_list
