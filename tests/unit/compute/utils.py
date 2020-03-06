"""Module use by nuke unit tests."""

import boto3


def create_autoscaling(region_name):
    """Create autoscaling group."""
    client = boto3.client("autoscaling", region_name=region_name)
    client.create_launch_configuration(
        LaunchConfigurationName="lc-test",
        ImageId="ami-02df9ea15c1778c9c",
        InstanceType="t2.micro",
    )
    client.create_auto_scaling_group(
        AutoScalingGroupName="asg-test",
        MaxSize=5,
        DesiredCapacity=3,
        MinSize=1,
        LaunchConfigurationName="lc-test",
        AvailabilityZones=[region_name + "a", region_name + "b"],
    )


def create_ebs(region_name):
    """Create ebs volume."""
    client = boto3.client("ec2", region_name=region_name)
    client.create_volume(AvailabilityZone=region_name + "a", Size=50)


def create_instances(count, region_name):
    """Create ec2 instances."""
    client = boto3.client("ec2", region_name=region_name)
    client.run_instances(
        ImageId="ami-02df9ea15c1778c9c", MaxCount=count, MinCount=count
    )


def create_ecr(region_name):
    """Create ecr repository."""
    client = boto3.client("ecr", region_name=region_name)
    client.create_repository(repositoryName="ecr-test")


def create_elb(region_name):
    """Create elb."""
    elb = boto3.client("elb", region_name=region_name)

    elb.create_load_balancer(
        LoadBalancerName="elb-test",
        AvailabilityZones=[region_name + "a", region_name + "b"],
        Listeners=[
            {
                "Protocol": "tcp",
                "LoadBalancerPort": 80,
                "InstanceProtocol": "tcp",
                "InstancePort": 80,
            }
        ],
    )


def create_elbv2(region_name):
    """Create elbv2."""
    elbv2 = boto3.client("elbv2", region_name=region_name)
    ec2 = boto3.client("ec2", region_name=region_name)

    elbv2.create_load_balancer(
        Name="elbv2-test",
        Subnets=[
            ec2.describe_subnets()["Subnets"][0]["SubnetId"],
            ec2.describe_subnets()["Subnets"][1]["SubnetId"],
        ],
        Scheme="internal",
    )


def create_keypair(region_name):
    """Create keypair."""
    client = boto3.client("ec2", region_name=region_name)

    client.create_key_pair(KeyName="keypair-test")


def create_spot(count, region_name):
    """Create spot request and spot fleet."""
    client = boto3.client("ec2", region_name=region_name)

    client.request_spot_instances(InstanceCount=count)


def create_ami(region_name):
    """Create ami image."""
    client = boto3.client("ec2", region_name=region_name)

    instance = client.run_instances(
        ImageId="ami-02df9ea15c1778c9c", MaxCount=1, MinCount=1
    )
    client.create_image(
        InstanceId=instance["Instances"][0]["InstanceId"], Name="nuke-ami"
    )


def create_snapshot(region_name):
    """Create ec2 snapshot."""
    client = boto3.client("ec2", region_name=region_name)

    ebs_volume = client.create_volume(
        AvailabilityZone=region_name + "a", Size=50
    )
    client.create_snapshot(VolumeId=ebs_volume["VolumeId"])
