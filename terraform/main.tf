resource "aws_s3_bucket" "priya-soure-bucket" {
  bucket = "priya-soure-bucket"
  #region =var.aws_region
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket" "priya-raw-bucket" {
  bucket = "priya-raw-bucket"
  #region =var.aws_region
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket" "priya-code-bucket" {
  bucket = "priya-code-bucket"
  #region =var.aws_region
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_object" "object" {
  bucket = "priya-code-bucket"
  key    = "priyamovielens/config/config.json"
  #acl = "private"
  source = "../src/config/config.json"

  etag = filemd5("../src/config/config.json")
}

resource "aws_s3_object" "process_json" {
  bucket = "priya-code-bucket"
  key    = "priyamovielens/config/process_config.json"
  #acl = "private"
  source = "../src/config/process_config.json"

  etag = filemd5("../src/config/process_config.json")
}
