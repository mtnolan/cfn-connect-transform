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
  file_path = (sys.argv[3] +  os.path.basename(uri))

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
  print(data, "\n")

  resources = get_resources(data)

  for resource in resources.items():
    for prop in resource:
      print(prop)
    if prop['Type'] == 'Custom::ContactFlow':
      print("!!! \n")
      uri = prop['Properties']['ContactFlowUri']
      
      new_uri_object = process_contact_flow(uri)
      prop['Properties']['ContactFlowPath'] = new_uri_object['file_path']
      prop['Properties']['ContactFlowBucket'] = new_uri_object['bucket']


print(dump_yaml(data))

# for mod in export_json['modules']:
#   if mod['type'] == 'InvokeExternalResource':
#     # TODO: Don't assume this will be true if other external resources are exposed.  For now assuming Lambda function only.

#     for param in mod['parameters']:
#       if param['name'] == 'FunctionArn':
#         function_names.append(param['value'])
      

# unique_functions = np.unique(function_names)
# function_name_maps = [];

# print(len(unique_functions), " unique Lambdas found.  Select a variable name for each lambda function.")
# # TODO: Play some kind of closing message when there are no lambdas found

# for function_name in np.unique(function_names):
#   name = input(function_name + " variable name:")
#   function_name_maps.append({'function_name': function_name, 'variable_name': name})
  

# print(function_name_maps)
# new_export = original_export_string

# for name_map in function_name_maps:
#   name = name_map['function_name']
#   variable_name = name_map['variable_name']
# # TODO: Name new_export better
#   print("Replacing ", name, " with variable name ", variable_name)
#   new_export = new_export.replace(name, (format_variable_name(variable_name)))

# print("Export Transform Complete.  Saving new file.")
# new_file = open(r"newfile.json", "w")
# new_file.write(new_export)
# new_file.close()
