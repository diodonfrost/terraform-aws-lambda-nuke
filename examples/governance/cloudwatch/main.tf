# Terraform cloudwatch with lambda scheduler

# Create cloudwatch dashboard
resource "aws_cloudwatch_dashboard" "nuke" {
  count          = 3
  dashboard_name = "nuke-dashboard-${count.index}"

  dashboard_body = <<EOF
 {
   "widgets":[
      {
         "type":"text",
         "x":0,
         "y":7,
         "width":3,
         "height":3,
         "properties":{
            "markdown":"Hello world"
         }
      }
   ]
}
EOF

}

# Create cloudwatch metric alarm
resource "aws_cloudwatch_metric_alarm" "nuke" {
  alarm_name                = "nuke alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "80"
  alarm_description         = "This is a metric test for nuke scheduler"
  insufficient_data_actions = []
}

### Terraform modules ###

module "nuke-everything" {
  source                         = "../../../"
  name                           = "nuke-cloudwatch"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  exclude_resources              = ""
  older_than                     = "0d"
}

