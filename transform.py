import sys
import json
import numpy as np

def format_variable_name(var_name):
  return ("$$" + var_name + "$$")


print("Creating template for ", sys.argv[1])

function_names = []

with open(sys.argv[1]) as f:
  original_export_string = f.read()
  export_json = json.loads(original_export_string)

for mod in export_json['modules']:
  if mod['type'] == 'InvokeExternalResource':
    # TODO: Don't assume this will be true if other external resources are exposed.  For now assuming Lambda function only.

    for param in mod['parameters']:
      if param['name'] == 'FunctionArn':
        function_names.append(param['value'])
      

unique_functions = np.unique(function_names)
function_name_maps = [];

print(len(unique_functions), " unique Lambdas found.  Select a variable name for each lambda function.")
# TODO: Play some kind of closing message when there are no lambdas found

for function_name in np.unique(function_names):
  name = input(function_name + " variable name:")
  function_name_maps.append({'function_name': function_name, 'variable_name': name})
  

print(function_name_maps)
new_export = original_export_string

for name_map in function_name_maps:
  name = name_map['function_name']
  variable_name = name_map['variable_name']
# TODO: Name new_export better
  print("Replacing ", name, " with variable name ", variable_name)
  new_export = new_export.replace(name, (format_variable_name(variable_name)))

print("Export Transform Complete.  Saving new file ", sys.argv[2])
new_file = open(sys.argv[2], "w")
new_file.write(new_export)
new_file.close()
