resource "aws_dynamodb_table" "ingestion_source_raw_table" {
  name           = "data_audit_table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key = "SK"
  attribute {
    name = "PK"
    type = "S"
  } 
  attribute {
    name = "SK"
    type = "S"
  }
}

data "aws_iam_policy_document" "dynamodb_policy" {
  
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:*",
    
    ]
    resources = ["*"]
  }
} 

resource "aws_iam_role_policy" "dynamodb_policy_tf" {
  name   = "dynamodb_policy_tf"
  policy = data.aws_iam_policy_document.dynamodb_policy.json
  role   = aws_iam_role.iam_for_lambda.name
}

/* resource "aws_lambda_event_source_mapping" "dynamodb_mapping" {
  event_source_arn = aws_dynamodb_table.ingestion_source_raw_table.stream_arn
  function_name    = aws_lambda_function.lambda-source-raw.function_name
  starting_position = "LATEST"
} */

