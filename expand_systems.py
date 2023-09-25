import json, os
from collections import namedtuple

# files we need
source = "foxsi4-commands/systems.json"
output = "foxsi4-commands/expanded_systems.json"

cwd = os.getcwd()

# a function to recursively inject JSON from linked files into single parent file
def substitute_json(json_dict:dict):
    for key in json_dict.keys():
        val = json_dict[key]
        if isinstance(val, str):        # case where the rhs of key is a path
            if "/" in val and key != "commands":
                try:
                    sub_dict = {}
                    with open(cwd + "/" + val) as sub_json:
                        print("opened " + val)
                        sub_dict = json.load(sub_json)

                    json_dict[key] = sub_dict
                    substitute_json(sub_dict)
                except:
                    raise Exception("tried to open the wrong thing :(")
        elif isinstance(val, dict):     # case where the rhs of key is more nested JSON
            for subkey in val.keys():
                subval = val[subkey]
                if "/" in subval and subkey != "commands":
                    try:
                        sub_dict = {}
                        with open(cwd + "/" + subval) as sub_json:
                            print("opened " + subval)
                            sub_dict = json.load(sub_json)

                        val[subkey] = sub_dict
                        substitute_json(sub_dict)
                    except:
                        raise Exception("tried to open the wrong thing :(")
    

sys_dict = {}
try:
    with open(source) as sys_json:
        sys_dict = json.load(sys_json)
except:
    raise Exception("couldn't open systems list")

# look through the file, substituting in JSON where paths where
for item in sys_dict:
    substitute_json(item)
        
# write the output to output (provided above)
with open(output, "w") as result_file:
    json_string = json.dump(sys_dict, result_file, indent=4)

print("wrote output to " + output)