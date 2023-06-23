from datetime import datetime
import boto3
import json                #The code you provided imports several modules and libraries
import os
import logging
import itertools
from aws_lambda_powertools import Logger
import uuid

log = Logger(service="ingest_source_raw")

current_date = datetime.now()
#date_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
codelamdabucket = os.environ['codebucket']
print(codelamdabucket)
sns_topic_variable = os.environ['sns_topic']
#data_set = os.environ['folder_key']
s3 = boto3.resource('s3')  #These lines initialize the AWS clients using the boto3 library.
s3_client=boto3.client('s3')
sns_client = boto3.client('sns')
dynamo_client = boto3.client('dynamodb')
waiter = dynamo_client.get_waiter('table_exists')


    
#unique_id = str(uuid.uuid4()).replace("-", "")

def put_items_to_audit_table(item):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'data_audit_table'
    table = dynamodb.Table(table_name)
    
    # item = {
    #     'PK' : context.aws_request_id,
    #     'SK' : 'test',
    #     'Process_name' : 'test',
    #     'function_name' : context.function_name,
    #     'aqcuisition' : 'test',
    #     'file_name' : 'test',
    #     'date_time' : 'test',
    #     'process_time_taken' : 'test',
    #     'status' : 'test',
    # }
    table.put_item(Item=item)
# logging.basicConfig(      #function from the logging module
#     level=logging.INFO,
#     format=f"%(asctime)s  %(lineno)d    %(levelname)s   %(message)s",
# )
# log = logging.getLogger("Priya-Ingest-file")  #getLogger() function from the logging module is used to create a logger object.
#log.setLevel(logging.INFO) #in this way, you can use the log object to log messages with a severity level of INFO or higher.
log.info("ingest_raw")
def sending_email(message, subject):     
    response = sns_client.publish(  #that sends an email using the Amazon Simple Notification Service (SNS) client 
        TopicArn=sns_topic_variable,
        Message=message,
        Subject= subject,
        
    )

    #print(f"{output} table exits")
# partition should be a string:  " DAY / MONTH / YEAR"
def parse_partition(partition):
    current_date = datetime.now()
    date_dict = {
        "year"  : current_date.year,
        "month" : current_date.month,
        "day"   : current_date.day,
        "hours" : current_date.hour,
    }
        
    res = list(date_dict.keys()).index(partition.lower().strip()) + 1
    #Python 3 you can use the itertools islice to slice the dict.items() iterator
    #To slice the dictionary up to the specified index
    m = list(dict(itertools.islice(date_dict.items(), res))) #This returns an iterator of key-value pairs up to the specified index.
    result = ""  #string variable called result is initialized.
    for key in m:
        result = result+f"{key}={date_dict[key]}/"
    return result

def lambda_handler(event, context): #the entry point for your Lambda function. It is triggered when an event occurs, and it takes two parameters: event and context
    
    try:
        data_set = event.get("data_set")
        log.info(f"{data_set} This is the key we used")
        output = waiter.wait(
            TableName='data_audit_table'
            )
        put_items_to_audit_table(item)
    except Exception as e:
        log.info("table doesnot exits")
    
    try:
        response = s3_client.get_object(Bucket=codelamdabucket, Key=f"{data_set}/config/config.json")  #method is called to retrieve an object from an S3 bucket. It uses the codelamdabucket variable as the bucket name and constructs the object key based on the data_set value.
        log.info("curretly executed")
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
    except Exception as e:
         log.exception(f"error occurred {e}")
         sending_email("getting the bucket or folder or target bucket from json had issue please check the json file", "failure targetbucket" )
    
    try:
        response = s3_client.list_objects_v2(Bucket=source_bucket) # method is called on the s3_client to list objects in the source_bucket
        log.info(response)
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
    file_names_data = []
    
    for index, i in enumerate(file_list[1:]):
        try:
            file_part = i.split('.')[0] #Split the file name into two parts
            file_extension = i.split('.')[1]
            log.info(file_part)
            data_asset = config_json['pipeline'][index]['data_asset']
            partition_data = config_json['pipeline'][index]['raw']['partition']
            pattern = config_json['pipeline'][index]['raw']['file_pattern']
            updated_file_name = file_part
            if pattern.replace("*","") in data_asset:
                updated_file_name = data_asset
            log.info(partition_data)
            print(partition_data)
            otherkey = f"{source_folder}/{file_part}/{parse_partition(partition_data)}{updated_file_name}_{current_date}.{file_extension}"
            log.info(otherkey)
            file_names_data.append(otherkey)
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
  
    
        
    # return {        #The return statement in the code snippet is used to define the response of the AWS Lambda function.
    # 'statusCode': 200, #HTTP status code of the response
    # 'body': json.dumps(file_names_data) #otherkey variable is converted to a JSON string using json.dumps() 
             
    # }
    
    item = {
        'PK' : context.aws_request_id,
        'SK' : 'test',
        'Process_name' : 'test',
        'function_name' : context.function_name,
        'aqcuisition' : 'test',
        'file_name' : 'test',
        'date_time' : 'test',
        'process_time_taken' : 'test',
        'status' : 'test',
    }
    put_items_to_audit_table(item)