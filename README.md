# PROJECT


**CREATION AND ATTACHMENTS OF ROLE AND POLICIES**:

Creating data  for blocks define IAM policy documents that specify the permissions needed for different AWS services.

Creating an IAM policy document named "assume_role". This policy document can be used to grant the necessary permissions for AWS Lambda functions to assume that role.

The cloud_watch_policy policy allows actions related to CloudWatch Logs, such as creating log groups, log streams, and putting log events. It applies to CloudWatch Logs in a specific region and includes a specific log group associated with a Lambda function.

The s3_policy policy allows all actions related to Amazon S3, including S3 Object Lambda. It grants access to all S3 resources, allowing various operations on S3 buckets and objects.

The sns_topic_policy policy allows all actions related to Amazon SNS (Simple Notification Service). It grants access to all SNS resources, enabling sending and managing notifications using SNS.

These three policies are attached to the role which I mentioned as "assume_role".
Creating a resoure for the role and the policies.

**1.aws_iam_role**:

This resource creates an IAM role named "iam_for_lambda" that will be assumed by the Lambda function.
The assume_role_policy attribute specifies the trust policy document that allows the Lambda service (lambda.amazonaws.com) to assume this role.

2.aws_iam_policy:

resource creates an IAM policy named "s3_policy" that defines the permissions for interacting with Amazon S3.
The policy document is obtained from the data.aws_iam_policy_document.s3_policy.

aws_iam_role_policy_attachment:

resource attaches the "s3_policy" IAM policy to the "iam_for_lambda" IAM role.
It grants the role permissions to perform actions related to Amazon S3.
The role specified in the role attribute is aws_iam_role.iam_for_lambda.name.
The policy ARN specified in the policy_arn attribute is aws_iam_policy.s3_policy.arn.

Here in the cloud watch policy i did the policy creation and attach to the role in one step:
aws_iam_role_policy:

This resource attaches the "cloud_watch_policy" to the "iam_for_lambda" IAM role.
The policy document is obtained from the data.aws_iam_policy_document.cloud_watch_policy data block.
The role specified in the role attribute is aws_iam_role.iam_for_lambda.name


aws_sns_topic:

resource creates an SNS (Simple Notification Service) topic named "priya-data-ingestion-pipeline" that can be used for publishing and subscribing to messages.

aws_iam_role_policy:
resource attaches the "sns_topic_policy" to the "iam_for_lambda" IAM role.
The policy document is obtained from the data.aws_iam_policy_document.sns_topic_policy data block.
The role specified in the role attribute is aws_iam_role.iam_for_lambda.name.
This policy allows the role to perform actions related to Amazon SNS.

aws_sns_topic_subscription:
resource creates a subscription to the SNS topic.
It delivers messages to the specified email address ("priyakpalaka@gmail.com") using the "email-json" protocol.


CREATE THE LAMBDA FUNTION AND ATTACH TO ROLE:

1.create a zip file using the archive_file data source in Terraform. The zip file is created from a source file, which is a Python script located in my local ../src/ingestion_lamda_function_raw/ingestion_raw.py. The resulting zip file is saved at ../src/ingestion_lamda_function_raw/ingestion_raw.zip.

2.creating a lambda function references the output path of the previously defined archive_file data source.

The role parameter specifies the ARN (Amazon Resource Name) of the IAM role associated with the Lambda function. IAM roles define the permissions and access policies for the Lambda function. In this case, it references the ARN of the iam_for_lambda IAM role.

The handler parameter indicates the entry point of the Lambda function within the code package and giving the parameters live timeout = 900,
runtime = python3.10

The source_code_hash parameter ensures that the Lambda function is updated when the code package changes. It references the output of the output_base64sha256 attribute of the archive_file data source, which represents a hash value calculated based on the contents of the deployment package.

The environment block defines environment variables for the Lambda function. In this case, it sets the values for two variables: codebucket and sns_topic. The codebucket variable is set to "priya-code-bucket", and the sns_topic variable is set to the ARN of the creating_topic SNS topic resource.
These environment variable defined in the python lambda code for the use to make them Dynamic.

CREATING THE BUCKETS USING TERRAFORM:


IN PROCESS_CONFIG.JSON FILE:

I mentioned the bucket names to some meanining full variables.
    "source_bucket": "priya-soure-bucket",
    "source_folder": "priyamovielens",
    "target_bucket": "priya-raw-bucket"
    
EVENT BRIDGE:
    
    
 






