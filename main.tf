################################################
#
#            LAMBDA FUNCTION
#
################################################
data "aws_region" "current" {}

data "archive_file" "this" {
  type        = "zip"
  source_dir  = "${path.module}/package/"
  output_path = "${path.module}/nuke-everything.zip"
}

resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = var.name
  role             = var.custom_iam_role_arn == null ? aws_iam_role.this[0].arn : var.custom_iam_role_arn
  handler          = "nuke.main.lambda_handler"
  source_code_hash = data.archive_file.this.output_base64sha256
  runtime          = var.runtime
  timeout          = "900"
  kms_key_arn      = var.kms_key_arn
  tags             = var.tags

  environment {
    variables = {
      AWS_REGIONS       = var.aws_regions == null ? data.aws_region.current.name : join(", ", var.aws_regions)
      EXCLUDE_RESOURCES = var.exclude_resources
      OLDER_THAN        = var.older_than
    }
  }
}

################################################
#
#            CLOUDWATCH EVENT
#
################################################
resource "aws_cloudwatch_event_rule" "this" {
  name                = "trigger-lambda-nuke-${var.name}"
  description         = "Trigger lambda nuke"
  schedule_expression = var.cloudwatch_schedule_expression
  tags                = var.tags
}

resource "aws_cloudwatch_event_target" "this" {
  arn  = aws_lambda_function.this.arn
  rule = aws_cloudwatch_event_rule.this.name
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.this.function_name
  source_arn    = aws_cloudwatch_event_rule.this.arn
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 14
  tags              = var.tags
}
