from datetime import datetime
import boto3
import json                #The code you provided imports several modules and libraries
import os
import logging


current_date = datetime.now().date()
year = current_date.year
month = current_date.month
day = current_date.day
codelamdabucket = os.environ['codebucket']
print(codelamdabucket)
sns_topic_variable = os.environ['sns_topic']
#data_set = os.environ['folder_key']
s3 = boto3.resource('s3')  #These lines initialize the AWS clients using the boto3 library.
s3_client=boto3.client('s3')
sns_client = boto3.client('sns')


logging.basicConfig(      #function from the logging module
    level=logging.INFO,
    format=f"%(asctime)s  %(lineno)d    %(levelname)s   %(message)s",
)
log = logging.getLogger("Priya-Ingest-file")  #getLogger() function from the logging module is used to create a logger object.
log.setLevel(logging.INFO) #in this way, you can use the log object to log messages with a severity level of INFO or higher.

def sending_email(message, subject):     
    response = sns_client.publish(  #that sends an email using the Amazon Simple Notification Service (SNS) client 
        TopicArn=sns_topic_variable,
        Message=message,
        Subject= subject,
        
    )

def lambda_handler(event, context): #the entry point for your Lambda function. It is triggered when an event occurs, and it takes two parameters: event and context
    try:
        data_set = event.get("data_set")
        log.info(f"{data_set} This is the key we used")
        response = s3_client.get_object(Bucket=codelamdabucket, Key=f"{data_set}/config/process_config.json")  #method is called to retrieve an object from an S3 bucket. It uses the codelamdabucket variable as the bucket name and constructs the object key based on the data_set value.
        log.info("curretly executed")
        sending_email("The bucket and key are executed here", "evironment variable success")
    except Exception as e:
        log.exception(f"error occurred {e}")
        sending_email(f"getting an error '{e}' with the environmental variable or the folder name", "environment variable failure ")
    
    try:     
        config_data = response.get('Body').read().decode('utf-8')
        config_json = json.loads(config_data)  #The config_data string is loaded into a JSON object using json.loads(config_data), creating the config_json object.
        source_bucket = config_json.get('source_bucket')
        source_folder = config_json.get('source_folder')
        target_bucket = config_json.get('target_bucket')

        log.info(source_bucket) #the value of source bucket
        sending_email("getting bucket and folder and target buckets has no issues", "success targetbucket")
    except Exception as e:
         log.exception(f"error occurred {e}")
         sending_email("getting the bucket or folder or target bucket from json had issue please check the json file", "failure targetbucket" )
    
    try:
        response = s3_client.list_objects_v2(Bucket=source_bucket) # method is called on the s3_client to list objects in the source_bucket
        log.info(response)
        sending_email("getting list of files from source bucket", "success list files")
    except Exception as e:
         log.exception(f"error occurred {e}")
         sending_email("error occured showing the list of files in source bucket", "failure list files")
 
    file_list = []  #An empty list file_list is initialized to store the extracted file names.
 
    for obj in response['Contents']: #An empty list file_list is initialized to store the extracted file names.
        try:
            file_name = obj['Key']  #retrieves the key of each object in the response['Contents'] list.
            file_name = file_name.replace(source_folder + '/', '')  #The source_folder is removed from the file_name by replacing it with an empty string, using the replace method.
            file_list.append(file_name)
            sending_email("The file list occured in right order", "success list order")
    #log.info(file_list)
        except Exception as e:
            log.exception(f"error occurred {e}")
            sending_email("list of files have some issue", "failure list order")

    for i in file_list[1:]:
        try:
            file_part = i.split('.')[0] #Split the file name into two parts
            file_extension = i.split('.')[1]
            log.info(file_part)
            otherkey = f"{source_folder}/{file_part}/year={year}/month={month}/day={day}/{file_part}_{current_date}.{file_extension}"
            log.info(otherkey)
            copy_source = { 
            'Bucket': source_bucket,
            'Key': f"{source_folder}/{i}"
                
            }
            bucket = s3.Bucket(target_bucket)
            bucket.copy(copy_source, otherkey) #and copy the file from the source bucket to the target bucket using the copy() method.
            sending_email("File names are created as we mentioned in day, year and month with file name", "success with file name")
        except Exception as e:
            log.exception(f"error occurred {e}")
            sending_email("issue occured creating the file name", "failure")
  


        
    return {        #The return statement in the code snippet is used to define the response of the AWS Lambda function.
    'statusCode': 200, #HTTP status code of the response
    'body': json.dumps(otherkey) #otherkey variable is converted to a JSON string using json.dumps() 
             
        }

    

