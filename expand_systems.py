import json, os, copy, ipaddress
from collections import namedtuple

# files we need
source = "foxsi4-commands/template_systems.json"
output = "foxsi4-commands/systems.json"
mock = "foxsi4-commands/foxsimile_systems.json"

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
                    print("could not parse file at " + val)
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

# create a localhost version of an IPv4 address, preserving LSB of the original address. Ignores multicast.
def set_local_socket(addr:str):
    if isinstance(addr, str):
        try:
            ipv4addr = ipaddress.IPv4Network(addr)
            if ipv4addr.is_multicast:
                return addr
            addr_split = addr.rsplit('.', 1)
            local_addr = "127.0.0." + addr_split[1]
            print("ip ", addr, "\twill have local value ", local_addr)
            return local_addr
        except ValueError:
            # could be a serial port...
            if "/dev/tty" in addr:
                addr = "/tmp/foxsi_serial"
            return addr

# recursively trawls a JSON dict and substitutes localhost IP addresses.
def substitute_ip(json_dict:dict):
    for key in json_dict.keys():
        val = json_dict[key]
        if isinstance(val, dict):
            val = substitute_ip(val)
            json_dict[key] = val
        elif isinstance(val, str):
            val = set_local_socket(val)
            json_dict[key] = val
    return json_dict
            
            

sys_dict = {}
try:
    with open(source) as sys_json:
        sys_dict = json.load(sys_json)
except:
    raise Exception("couldn't open systems list")

# look through the file, substituting in JSON where paths where
for item in sys_dict:
    substitute_json(item)
        
# write the synthesized json to output (provided above)
with open(output, "w") as result_file:
    json_string = json.dump(sys_dict, result_file, indent=4)

    # create a local-address based mocking version of the same file
    with open(mock, "w") as mock_file:
        local_dict = copy.deepcopy(sys_dict)
        for item in local_dict:
            substitute_ip(item)
        local_string = json.dump(local_dict, mock_file, indent=4)

print("wrote output to " + output)
print("wrote mocking output to " + mock)