################################################
#
#            IAM CONFIGURATION
#
################################################

resource "aws_iam_role" "this" {
  count              = var.custom_iam_role_arn == null ? 1 : 0
  name               = "${var.name}-lambda-nuke"
  description        = "Allows Lambda functions to destroy all aws resources"
  assume_role_policy = data.aws_iam_policy_document.this.json
  tags               = var.tags
}

data "aws_iam_policy_document" "this" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "nuke_compute" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-compute"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_compute.json
}

data "aws_iam_policy_document" "nuke_compute" {
  statement {
    actions = [
      "ec2:DescribeInstances",
      "ec2:TerminateInstances",
      "ec2:DescribeSpotInstanceRequests",
      "ec2:CancelSpotInstanceRequests",
      "ec2:DescribeSpotFleetRequests",
      "ec2:DeleteSpotInstanceRequest",
      "ec2:DescribeLaunchTemplates",
      "ec2:DeleteLaunchTemplate",
      "ec2:DescribeSnapshots",
      "ec2:DeleteSnapshot",
      "ec2:DescribeVolumes",
      "ec2:DeleteVolume",
      "ec2:DescribeKeyPairs",
      "ec2:DeleteKeyPair",
      "ec2:DescribePlacementGroups",
      "ec2:DeletePlacementGroup",
      "ec2:DescribeImages",
      "ec2:DeregisterImage",
      "dlm:GetLifecyclePolicy",
      "dlm:GetLifecyclePolicies",
      "dlm:DeleteLifecyclePolicy",
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DeleteAutoScalingGroup",
      "autoscaling:DescribeLaunchConfigurations",
      "autoscaling:DeleteLaunchConfiguration",
      "elasticloadbalancing:DescribeLoadBalancers",
      "elasticloadbalancing:DeleteLoadBalancer",
      "elasticloadbalancing:DescribeTargetGroups",
      "elasticloadbalancing:DeleteTargetGroup",
      "ecr:DescribeRepositories",
      "ecr:DeleteRepository",
      "eks:ListClusters",
      "eks:DescribeCluster",
      "eks:DeleteCluster",
      "elasticbeanstalk:DescribeApplications",
      "elasticbeanstalk:DescribeEnvironments",
      "elasticbeanstalk:DeleteApplication",
      "elasticbeanstalk:TerminateEnvironment",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "nuke_storage" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-storage"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_storage.json
}

data "aws_iam_policy_document" "nuke_storage" {
  statement {
    actions = [
      "s3:ListAllMyBuckets",
      "s3:ListBucket",
      "s3:ListBucketVersions",
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:DeleteObject",
      "s3:DeleteObjectVersion",
      "s3:DeleteBucketPolicy",
      "s3:DeleteBucket",
      "elasticfilesystem:DescribeFileSystems",
      "elasticfilesystem:DeleteFileSystem",
      "glacier:ListVaults",
      "glacier:DescribeVault",
      "glacier:DeleteVault",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "nuke_database" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-database"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_database.json
}

data "aws_iam_policy_document" "nuke_database" {
  statement {
    actions = [
      "rds:DescribeDBClusters",
      "rds:DeleteDBCluster",
      "rds:DescribeDBInstances",
      "rds:DeleteDBInstance",
      "rds:DescribeDBSubnetGroups",
      "rds:DeleteDBSubnetGroup",
      "rds:DescribeDBClusterParameterGroups",
      "rds:DeleteDBClusterParameterGroup",
      "rds:DescribeDBParameterGroups",
      "rds:DeleteDBParameterGroup",
      "rds:DescribeDBClusterSnapshots",
      "rds:DeleteDBClusterSnapshot",
      "dynamodb:ListTables",
      "dynamodb:DescribeTable",
      "dynamodb:DeleteTable",
      "dynamodb:ListBackups",
      "dynamodb:DescribeBackup",
      "dynamodb:DeleteBackup",
      "elasticache:DescribeCacheClusters",
      "elasticache:DeleteCacheCluster",
      "elasticache:DescribeSnapshots",
      "elasticache:DeleteSnapshot",
      "elasticache:DescribeCacheSubnetGroups",
      "elasticache:DeleteCacheSubnetGroup",
      "elasticache:DescribeCacheParameterGroups",
      "elasticache:DeleteCacheParameterGroup",
      "redshift:DescribeClusters",
      "redshift:DeleteCluster",
      "redshift:DescribeClusterSnapshots",
      "redshift:DeleteClusterSnapshot",
      "redshift:DescribeClusterParameterGroups",
      "redshift:DeleteClusterParameterGroup",
      "redshift:DescribeClusterSubnetGroups",
      "redshift:DeleteClusterSubnetGroup",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "nuke_network" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-network"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_network.json
}

data "aws_iam_policy_document" "nuke_network" {
  statement {
    actions = [
      "ec2:DescribeSecurityGroups",
      "ec2:DeleteSecurityGroup",
      "ec2:DescribeNetworkAcls",
      "ec2:DeleteNetworkAcl",
      "ec2:DescribeVpcEndpoints",
      "ec2:DeleteVpcEndpoints",
      "ec2:DescribeVpcEndpointServices",
      "ec2:DescribeVpcEndpointServiceConfigurations",
      "ec2:DeleteVpcEndpointServiceConfigurations",
      "ec2:DescribeNatGateways",
      "ec2:DeleteNatGateway",
      "ec2:DescribeAddresses",
      "ec2:ReleaseAddress",
      "ec2:DescribeRouteTables",
      "ec2:DeleteRouteTable",
      "ec2:DescribeInternetGateways",
      "ec2:DeleteInternetGateway",
      "ec2:DescribeEgressOnlyInternetGateways",
      "ec2:DeleteEgressOnlyInternetGateway",
      "ec2:RevokeSecurityGroupEgress",
      "ec2:RevokeSecurityGroupIngress",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "nuke_analytic" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-analytic"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_analytic.json
}

data "aws_iam_policy_document" "nuke_analytic" {
  statement {
    actions = [
      "elasticmapreduce:ListClusters",
      "elasticmapreduce:TerminateJobFlows",
      "kafka:ListClusters",
      "kafka:DeleteCluster",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "nuke_monitoring" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-nuke-monitoring"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.nuke_monitoring.json
}

data "aws_iam_policy_document" "nuke_monitoring" {
  statement {
    actions = [
      "cloudwatch:ListDashboards",
      "cloudwatch:DeleteDashboards",
      "cloudwatch:DescribeAlarms",
      "cloudwatch:DeleteAlarms",
    ]

    resources = [
      "*",
    ]
  }
}

locals {
  lambda_logging_policy = {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "${aws_cloudwatch_log_group.this.arn}:*",
        "Effect" : "Allow"
      }
    ]
  }
  lambda_logging_and_kms_policy = {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "${aws_cloudwatch_log_group.this.arn}:*",
        "Effect" : "Allow"
      },
      {
        "Action" : [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:CreateGrant"
        ],
        "Resource" : var.kms_key_arn,
        "Effect" : "Allow"
      }
    ]
  }
}

resource "aws_iam_role_policy" "lambda_logging" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-lambda-logging"
  role   = aws_iam_role.this[0].id
  policy = var.kms_key_arn == null ? jsonencode(local.lambda_logging_policy) : jsonencode(local.lambda_logging_and_kms_policy)
}
