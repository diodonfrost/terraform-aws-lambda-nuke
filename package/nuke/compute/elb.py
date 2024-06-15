# -*- coding: utf-8 -*-

"""Module deleting all aws Classic Load Balancer resources."""

from typing import Iterator, Dict

from botocore.exceptions import ClientError, EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import nuke_exceptions


class NukeElb:
    """Abstract elb nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize elb nuke."""
        self.elb = AwsClient().connect("elb", region_name)
        self.elbv2 = AwsClient().connect("elbv2", region_name)

        try:
            self.elb.describe_load_balancers()
            self.elbv2.describe_load_balancers()
        except EndpointConnectionError:
            print("elb resource is not available in this aws region")
            return

    def nuke(self, older_than_seconds: float, required_tags: Dict[str, str] = None) -> None:
        """Main nuke entrypoint function for elb and elbv2.

        Entrypoint function

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource
            will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the load balancers to exclude from deletion
        """
        self.nuke_loadbalancers(older_than_seconds, required_tags)
        self.nuke_target_groups()

    def nuke_loadbalancers(self, time_delete: float, required_tags: Dict[str, str] = None) -> None:
        """Loadbalancer delete function.

        Deleting all elbv and elbv2 with a timestamp greater than older_than_seconds.

        :param int older_than_seconds:
            The timestamp in seconds used from which the aws resource will be deleted
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) for the load balancers to exclude from deletion
        """
        for elb in self.list_elb(time_delete):
            if required_tags and not self._elb_has_required_tags(elb, required_tags):
                continue
            try:
                self.elb.delete_load_balancer(LoadBalancerName=elb)
                print("Nuke Load Balancer {0}".format(elb))
            except ClientError as exc:
                nuke_exceptions("elb", elb, exc)

        for elbv2 in self.list_elbv2(time_delete):
            if required_tags and not self._elbv2_has_required_tags(elbv2, required_tags):
                continue
            try:
                self.elbv2.delete_load_balancer(LoadBalancerArn=elbv2)
                print("Nuke Load Balancer {0}".format(elbv2))
            except ClientError as exc:
                nuke_exceptions("elbv2", elbv2, exc)

    def nuke_target_groups(self) -> None:
        """Elbv2 Target group delete function.

        Deleting all elbv2 target groups
        """
        for target_group in self.list_target_groups():
            try:
                self.elbv2.delete_target_group(TargetGroupArn=target_group)
                print("Nuke Target Group {0}".format(target_group))
            except ClientError as exc:
                nuke_exceptions("lb target group", target_group, exc)

    def list_elb(self, time_delete: float) -> Iterator[str]:
        """Elastic Load Balancer list function.

        List the names of all Elastic Load Balancer with a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter Elastic Load Balancer

        :yield Iterator[str]:
            Load Balancer names
        """
        paginator = self.elb.get_paginator("describe_load_balancers")

        for page in paginator.paginate():
            for loadbalancer in page["LoadBalancerDescriptions"]:
                if loadbalancer["CreatedTime"].timestamp() < time_delete:
                    yield loadbalancer["LoadBalancerName"]

    def list_elbv2(self, time_delete: float) -> Iterator[str]:
        """Elastic Load Balancer v2 list function.

        List ARN of all Elastic Load Balancer v2 with a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter elbv2

        :yield Iterator[str]:
            Elbv2 ARN
        """
        paginator = self.elbv2.get_paginator("describe_load_balancers")

        for page in paginator.paginate():
            for lb in page["LoadBalancers"]:
                if lb["CreatedTime"].timestamp() < time_delete:
                    yield lb["LoadBalancerArn"]

    def list_target_groups(self) -> Iterator[str]:
        """Elastic Load Balancer Target Group list function.

        List ARN of all elbv2 Target Group with a timestamp lower than time_delete.

        :param int time_delete:
            Timestamp in seconds used for filter elbv2 Target Groups

        :yield Iterator[str]:
            Elbv2 ARN
        """
        paginator = self.elbv2.get_paginator("describe_target_groups")

        for page in paginator.paginate():
            for targetgroup in page["TargetGroups"]:
                yield targetgroup["TargetGroupArn"]

    def _elb_has_required_tags(self, elb_name: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Classic Load Balancer has the required tags.

        :param str elb_name:
            The name of the Classic Load Balancer
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the load balancer has all the required tags, False otherwise
        """
        try:
            response = self.elb.describe_tags(LoadBalancerNames=[elb_name])
            tags = response["TagDescriptions"][0]["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Classic Load Balancer tagging", elb_name, exc)
            return False

    def _elbv2_has_required_tags(self, elbv2_arn: str, required_tags: Dict[str, str]) -> bool:
        """Check if the Application Load Balancer or Network Load Balancer has the required tags.

        :param str elbv2_arn:
            The ARN of the Application Load Balancer or Network Load Balancer
        :param dict required_tags:
            A dictionary of required tags (key-value pairs) to exclude from deletion

        :return bool:
            True if the load balancer has all the required tags, False otherwise
        """
        try:
            response = self.elbv2.describe_tags(ResourceArns=[elbv2_arn])
            tags = response["TagDescriptions"][0]["Tags"]
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
            for key, value in required_tags.items():
                if tag_dict.get(key) != value:
                    return False
            return True
        except ClientError as exc:
            nuke_exceptions("Application Load Balancer tagging", elbv2_arn, exc)
            return False
