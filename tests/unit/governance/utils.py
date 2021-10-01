# -*- coding: utf-8 -*-
"""Module use by nuke unit tests."""

import boto3


def create_cloudwatch_dashboard(region_name):
    """Create cloudwatch dashboard."""
    client = boto3.client("cloudwatch", region_name=region_name)
    widget = {
        "widgets": [
            {
                "type": "text",
                "x": 0,
                "y": 7,
                "width": 3,
                "height": 3,
                "properties": {"markdown": "Hello world"},
            }
        ]
    }
    client.put_dashboard(
        DashboardName="dashboard-test",
        DashboardBody=str(widget).replace("'", '"'),
    )


def create_cloudwatch_alarm(region_name):
    """Create cloudwatch metric alarm."""
    client = boto3.client("cloudwatch", region_name=region_name)

    client.put_metric_alarm(
        AlarmName="alarm-test",
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Period=120,
        EvaluationPeriods=2,
        Statistic="Average",
        Threshold=80,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
    )
