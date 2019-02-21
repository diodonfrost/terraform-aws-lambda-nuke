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
  description = "Allow destroying all aws resources"

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
            "ecr:DeleteRepository"
        ],
        "Resource": "*",
        "Effect": "Allow"
    }
  ]
}
EOF
}

# Attach custom policy nuke to role
resource "aws_iam_role_policy_attachment" "autoscaling" {
  role       = "${aws_iam_role.nuke_lambda.name}"
  policy_arn = "${aws_iam_policy.nuke_compute.arn}"
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
