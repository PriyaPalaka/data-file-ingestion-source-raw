resource "aws_cloudwatch_event_rule" "lambda_trigger" {
  name        = "lambda_trigger"
  description = "Trigger Lambda function every night at 8 PM"
  schedule_expression = "cron(0 20 * * ? *)"  # Cron expression for 8 PM every day
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_trigger.name
  #target_id = "event-target-lambda"
  role_arn = aws_iam_role.event_bridge_role.arn
  input = "{\"data_set\" : \"priyamovielens\"}" # The input attribute specifies the input data that will be passed to the Lambda function when it is triggered
  arn = aws_sfn_state_machine.sfn_state_machine.arn
  target_id = aws_sfn_state_machine.sfn_state_machine.name
}






/* resource "aws_s3_bucket_object" "object1" {
for_each = fileset("../movielens_dataset/", "*")
bucket = aws_s3_bucket.priya-soure-bucket.id
key = each.value
source = "../movielens_dataset/${each.value}"
etag = filemd5("../movielens_dataset/${each.value}")
} */
