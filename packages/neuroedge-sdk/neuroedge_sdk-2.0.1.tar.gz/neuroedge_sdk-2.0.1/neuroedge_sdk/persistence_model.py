import boto3
import os
import logging
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
def persist_model(message_type, experiment_name, file_path):
    bucket_name = 'neuroedge-device'
    s3 = boto3.client('s3')
 
    if message_type == 1:
        folder = 'default'
    elif message_type == 2:
        folder = 'qnn'
    else:
        logging.warning(f"Unsupported message_type: {message_type}")
        return
 
    if os.path.exists(file_path):
        try:
            # Construct the S3 key with the folder path
            s3_key = f'{folder}/{experiment_name}_{os.path.basename(file_path)}'
            s3.upload_file(file_path, bucket_name, s3_key)
            logging.info(f"File '{file_path}' successfully uploaded to 's3://{bucket_name}/{s3_key}'")
        except Exception as e:
            logging.error(f"Error uploading file to S3: {e}")
    else:
        logging.warning(f"File '{file_path}' does not exist.")