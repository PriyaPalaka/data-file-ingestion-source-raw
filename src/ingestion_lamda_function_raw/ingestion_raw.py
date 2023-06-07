from datetime import datetime
import boto3
import json
import os
import logging


current_date = datetime.now() 
year = current_date.year
month = current_date.month
day = current_date.day
codelamdabucket = os.environ['codebucket']
print(codelamdabucket)
s3 = boto3.resource('s3')
s3_client=boto3.client('s3')
sns_client = boto3.client('sns')


logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s  %(lineno)d    %(levelname)s   %(message)s",
)
log = logging.getLogger("Priya-Ingest-file")
log.setLevel(logging.INFO)

def sending_email(message):     
    response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-2:817512490234:data-pipeline-notification',
        Message=message,
        Subject='priyamovielens ingestion',
        
    )

def lambda_handler(event, context):
    try:
        data_set = event.get("data_set")
        log.info(f"{data_set} This is the key we used")
        response = s3_client.get_object(Bucket=codelamdabucket, Key=f"{data_set}/config/process_config.json")
        log.info("curretly executed")
        sending_email("The bucket and key are executed here")
    except Exception as e:
        log.exception(f"error occurred {e}")
        sending_email("getting an error with the environmental variable or the folder name")
    
    try:     
        config_data = response.get('Body').read().decode('utf-8')
        config_json = json.loads(config_data)
        source_bucket = config_json.get('source_bucket')
        source_folder = config_json.get('source_folder')
        target_bucket = config_json.get('target_bucket')
        log.info(source_bucket)
        sending_email("getting bucket and folder and target buckets has no issues")
    except Exception as e:
         log.exception(f"error occurred {e}")
         sending_email("getting the bucket or folder or target bucket from json had issue please check the json file")
    
    try:
        response = s3_client.list_objects_v2(Bucket=source_bucket)
        log.info(response)
        sending_email("getting list of files from source bucket")
    except Exception as e:
         log.exception(f"error occurred {e}")
         sending_email("error occured showing the list of files in source bucket")
 
    file_list = []
 
    for obj in response['Contents']:
        try:
            file_name = obj['Key']
            file_name = file_name.replace(source_folder + '/', '')
            file_list.append(file_name)
            sending_email("The file list occured in right order")
    #log.info(file_list)
        except Exception as e:
            log.exception(f"error occurred {e}")
            sending_email("list of files have some issue")

    for i in file_list[1:]:
        try:
            file_part = i.split('.')[0]
            file_extension = i.split('.')[1]
            log.info(file_part)
            otherkey = f"{source_folder}/{file_part}/year={year}/month={month}/day={day}/{file_part}_{current_date}.{file_extension}"
            log.info(otherkey)
            copy_source = {
            'Bucket': source_bucket,
            'Key': f"{source_folder}/{i}"
                
            }
            bucket = s3.Bucket(target_bucket)
            bucket.copy(copy_source, otherkey)
            sending_email("File names are created as we mentioned in day, year and month with file name")
        except Exception as e:
            log.exception(f"error occurred {e}")
            sending_email("issue occured creating the file name")



        
    return {
    'statusCode': 200,
    'body': json.dumps(otherkey)
             
        }

    