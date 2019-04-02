################################################
#
#            IAM CONFIGURATION
#
################################################

# Create role for nuke all aws resouces
resource "aws_iam_role" "nuke_lambda" {
  name        = "${var.name}-lambda-nuke"
  description = "Allows Lambda functions to destroy all aws resources"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Create custom policy for allow destroying all compute resources
resource "aws_iam_policy" "nuke_compute" {
  name        = "${var.name}-nuke-compute"
  description = "Allow destroying all aws compute resources"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Action": [
            "ec2:DescribeInstances",
            "ec2:TerminateInstances",
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
            "ecs:ListClusters",
            "ecs:DeleteCluster",
            "eks:ListClusters",
            "eks:DescribeCluster",
            "eks:DeleteCluster",
            "elasticbeanstalk:DescribeApplications",
            "elasticbeanstalk:DescribeEnvironments",
            "elasticbeanstalk:DeleteApplication",
            "elasticbeanstalk:TerminateEnvironment"
        ],
        "Resource": "*",
        "Effect": "Allow"
    }
  ]
}
EOF
}

# Create custom policy for allow destroying all storage resources
resource "aws_iam_policy" "nuke_storage" {
  name        = "${var.name}-nuke-storage"
  description = "Allow destroying all aws storage resources"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Action": [
            "s3:ListAllMyBuckets",
            "s3:DeleteBucketPolicy",
            "s3:DeleteBucket",
            "elasticfilesystem:DescribeFileSystems",
            "elasticfilesystem:DeleteFileSystem",
            "glacier:ListVaults",
            "glacier:DescribeVault",
            "glacier:DeleteVault"
        ],
        "Resource": "*",
        "Effect": "Allow"
    }
  ]
}
EOF
}

# Create custom policy for allow destroying all rds resources
resource "aws_iam_policy" "nuke_database" {
  name        = "${var.name}-nuke-database"
  description = "Allow destroying all aws database resources"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
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
        "dax:DescribeClusters",
        "dax:DeleteCluster",
        "dax:DescribeParameterGroups",
        "dax:DeleteParameterGroup",
        "dax:DescribeSubnetGroups",
        "dax:DeleteSubnetGroup",
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
        "redshift:DeleteClusterSubnetGroup"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# Create custom policy for allow destroying all network resources
resource "aws_iam_policy" "nuke_network" {
  name        = "${var.name}-nuke-network"
  description = "Allow destroying all aws network resources"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
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
        "ec2:DeleteRouteTable"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# Attach custom policy compute nuke to role
resource "aws_iam_role_policy_attachment" "compute" {
  role       = "${aws_iam_role.nuke_lambda.name}"
  policy_arn = "${aws_iam_policy.nuke_compute.arn}"
}

# Attach custom policy storage nuke to role
resource "aws_iam_role_policy_attachment" "storage" {
  role       = "${aws_iam_role.nuke_lambda.name}"
  policy_arn = "${aws_iam_policy.nuke_storage.arn}"
}

# Attach custom policy database nuke to role
resource "aws_iam_role_policy_attachment" "database" {
  role       = "${aws_iam_role.nuke_lambda.name}"
  policy_arn = "${aws_iam_policy.nuke_database.arn}"
}

# Attach custom policy network nuke to role
resource "aws_iam_role_policy_attachment" "network" {
  role       = "${aws_iam_role.nuke_lambda.name}"
  policy_arn = "${aws_iam_policy.nuke_network.arn}"
}

################################################
#
#            LAMBDA FUNCTION
#
################################################

# Convert *.py to .zip because AWS Lambda need .zip
data "archive_file" "convert_py_to_zip" {
  type        = "zip"
  source_dir  = "${path.module}/package/"
  output_path = "${path.module}/nuke-everything.zip"
}

# Create Lambda function for destroy all aws resources
resource "aws_lambda_function" "nuke" {
  filename         = "${data.archive_file.convert_py_to_zip.output_path}"
  function_name    = "${var.name}"
  role             = "${aws_iam_role.nuke_lambda.arn}"
  handler          = "main.lambda_handler"
  source_code_hash = "${data.archive_file.convert_py_to_zip.output_base64sha256}"
  runtime          = "python3.7"
  timeout          = "600"
  environment {
    variables = {
      EXCLUDE_RESOURCES = "${var.exclude_resources}"
      OLDER_THAN        = "${var.older_than}"
    }
  }
}

################################################
#
#            CLOUDWATCH EVENT
#
################################################

# Create event cloud watch for trigger lambda function
resource "aws_cloudwatch_event_rule" "lambda_event" {
  name                = "trigger-lambda-nuke-${var.name}"
  description         = "Trigger lambda nuke"
  schedule_expression = "${var.cloudwatch_schedule_expression}"
}

# Set lambda function nuke as target
resource "aws_cloudwatch_event_target" "lambda_event_target" {
  arn  = "${aws_lambda_function.nuke.arn}"
  rule = "${aws_cloudwatch_event_rule.lambda_event.name}"
}

# Allow cloudwatch to invoke lambda function nuke
resource "aws_lambda_permission" "allow_cloudwatch_nuke" {
    statement_id  = "AllowExecutionFromCloudWatch"
    action        = "lambda:InvokeFunction"
    principal     = "events.amazonaws.com"
    function_name = "${aws_lambda_function.nuke.function_name}"
    source_arn    = "${aws_cloudwatch_event_rule.lambda_event.arn}"
}
