data "archive_file" "lambda" { #getting a zip file
  type        = "zip"
  source_file = "../src/ingestion_lamda_function_raw/ingestion_raw.py" #source file
  output_path = "../src/ingestion_lamda_function_raw/ingestion_raw.zip"
}
resource "aws_lambda_function" "lambda-source-raw" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = data.archive_file.lambda.output_path
  function_name = "priya-ingest-source-raw"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "ingestion_raw.lambda_handler"
  timeout       = 900
  runtime       = "python3.10"

  ephemeral_storage {
    size = 512 # Min 512 MB and the Max 10240 MB
  }
  environment {
    variables = {
      codebucket = "indval-data-ingestion-code"
    }
  }
}