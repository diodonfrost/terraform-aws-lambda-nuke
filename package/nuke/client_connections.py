# -*- coding: utf-8 -*-

"""Boto3 client connection class."""

import boto3


class MetaSingleton(type):
    """Singleton pattern for boto3 client connection."""

    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        """Singleton pattern method."""
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class AwsClient(metaclass=MetaSingleton):
    """Abstract aws client connection in a class."""

    connection = None
    aws_region = None
    aws_service = None

    def connect(self, service_name: str, region_name=None):
        """Initializes aws client connection to aws api only once.

        Connecting to aws api with low-level api client. This function
        uses a singleton pattern for initialize the connection only one
        time.

        :param str service_name:
            The AWS service used in instantiating the client.
        :param str region_name:
            The AWS Region used in instantiating the client. If used,
            this takes precedence over environment variable and
            configuration file values.
        """
        if (
            self.connection is None
            or self.aws_region != region_name
            or self.aws_service != service_name
        ):
            if region_name:
                self.connection = boto3.client(service_name, region_name)
            else:
                self.connection = boto3.client(service_name)
            self.aws_region = region_name
            self.aws_service = service_name
        return self.connection


class AwsResource(metaclass=MetaSingleton):
    """Abstract aws resource connection in a class."""

    connection = None
    aws_region = None
    aws_service = None

    def connect(self, service_name: str, region_name=None):
        """Initializes aws connection to aws api only once.

        Connecting to aws api with higher-level abstraction.
        This function uses a singleton pattern for initialize
        the connection only one time.

        :param str service_name:
            The AWS service used in instantiating the client.
        :param str region_name:
            The AWS Region used in instantiating the client. If used,
            this takes precedence over environment variable and
            configuration file values.
        """
        if (
            self.connection is None
            or self.aws_region != region_name
            or self.aws_service != service_name
        ):
            if region_name:
                self.connection = boto3.resource(service_name, region_name)
            else:
                self.connection = boto3.resource(service_name)
            self.aws_region = region_name
            self.aws_service = service_name
        return self.connection
