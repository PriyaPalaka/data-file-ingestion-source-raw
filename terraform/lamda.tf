data "archive_file" "lambda" { # It creates a data object named "lambda" that represents a zip file.
  type        = "zip"  
  source_file = "../src/ingestion_lamda_function_raw/ingestion_raw.py" #source file
  output_path = "../src/ingestion_lamda_function_raw/ingestion_raw.zip"
}
resource "aws_lambda_function" "lambda-source-raw" {
  filename      = data.archive_file.lambda.output_path #It references the output path of the archive_file data source
  function_name = "priya-ingest-source-raw"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "ingestion_raw.lambda_handler"  # Indicates the entry point of the Lambda function within the code package
  timeout       = 900
  runtime       = "python3.10"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  ephemeral_storage {
    size = 512 # Min 512 MB and the Max 10240 MB
  }
  environment {
    variables = {
      codebucket = "priya-code-bucket"
      sns_topic = aws_sns_topic.creating_topic.arn
     
  }
}
}
