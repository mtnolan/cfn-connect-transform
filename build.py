import sys
import os
import boto3
import logging

from botocore.exceptions import ClientError
import yaml
from cfn_tools import load_yaml, dump_yaml

def get_resources(data):
  return data['Resources']

def process_contact_flow(uri):
  print("Processing Contact Flow: ", uri)

  s3_client = boto3.client('s3')

  bucket = sys.argv[2]
  file_path = (sys.argv[3] + "/" + os.path.basename(uri))

  try:
    s3_client.upload_file(uri, bucket, file_path)
    
    print('Contact flow uploaded to ', bucket, "/", file_path)
    return {
      'bucket': bucket, 
      'file_path': file_path,
    }
  except ClientError as e:
    print("Error: ", e)
    logging.error(e)
    raise e

print("Transforming Template: ", sys.argv[1])
print("Bucket Name: ", sys.argv[2])
print("Bucket Prefix: ", sys.argv[3])

function_names = []

with open(sys.argv[1]) as file:
  text = file.read()
  data = load_yaml(text)

  resources = get_resources(data)

  for resource in resources.items():
    for prop in resource:
      if isinstance(prop, str): # Logical resource names get skipped
        continue
      print(prop)
      if prop['Type'] == 'Custom::ContactFlow':
        uri = prop['Properties']['ContactFlowUri']

        new_uri_object = process_contact_flow(uri)
        prop['Properties']['ContactFlowPath'] = new_uri_object['file_path']
        prop['Properties']['BuildNumber'] = sys.argv[3]
        prop['Properties']['ContactFlowBucket'] = new_uri_object['bucket']

new_file = open(sys.argv[1], "w")
new_file.write(dump_yaml(data))
new_file.close()
