resource "aws_cloudwatch_event_rule" "lambda_trigger" {
  name        = "lambda_trigger"
  description = "Trigger Lambda function every night at 8 PM"
  schedule_expression = "cron(0 20 * * ? *)"  # Cron expression for 8 PM every day
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_trigger.name
  target_id = "event-target-lambda"
  arn = aws_lambda_function.lambda-source-raw.arn
}