data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloud_watch_policy" {


  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:us-east-2:${var.account_number}:*",
      "arn:aws:logs:us-east-2:${var.account_number}:log-group:/aws/lambda/priya-ingest-source-raw:*"
    ]
  }
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:*",
      "s3-object-lambda:*",
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "sns_topic_policy" {

  statement {
    effect = "Allow"

    actions = [
      "SNS:*",

    ]
    resources = ["*"]
  }
}


resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "s3_policy" {
  name   = "s3_policy"
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_iam_role_policy" "cloud_watch_policy" {
  name   = "cloud_watch_policy"
  policy = data.aws_iam_policy_document.cloud_watch_policy.json
  role   = aws_iam_role.iam_for_lambda.name
}

resource "aws_iam_role_policy_attachment" "s3_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_sns_topic" "creating_topic" {
  name = "priya-data-ingestion-pipeline"

}

resource "aws_iam_role_policy" "sns_topic_policy" {
  name   = "sns_topic_policy"
  policy = data.aws_iam_policy_document.sns_topic_policy.json
  role   = aws_iam_role.iam_for_lambda.name
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.creating_topic.arn
  protocol  = "email-json"
  endpoint  = "priyakpalaka@gmail.com"
}




