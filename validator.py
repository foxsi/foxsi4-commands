import pandas as pd
import json
from collections import namedtuple

# files we need
command_file = "command_deck.csv"
systems_file = "all_systems.json"

asics_per_cdte = 4

# read command deck in
try:
    command_data = pd.read_csv(command_file)
except:
    raise Exception("couldn't open command_deck.csv")

# read systems list in
sys_dict = {}
try:
    with open(systems_file) as sys_json:
        sys_dict = json.load(sys_json)
except:
    raise Exception("couldn't open systems list")

# clean up systems
sys_names = [sys["name"].upper() for sys in sys_dict]
sys_ids = [sys["id"] for sys in sys_dict]

# clean up commands
head = list(command_data.iloc[0])
command_systems = [name.upper() for name in head[11:23]]

command_data = command_data[1:]
command_data.dropna(axis=0, how="all", inplace=True)

# validate systems
if len(sys_names) != len(set(sys_names)):
    raise Exception("system names are not unique")
if len(sys_ids) != len(set(sys_ids)):
    raise Exception("system ids are not unique")

if len(command_systems) != len(set(command_systems)):
    raise Exception("system names are not unique")

if set(command_systems) >= set(sys_names):
    raise Exception("systems in command list are not covered by system list")
elif set(command_systems) < set(sys_names):
    print("system list contains the following uncommanded systems: " + str(set(sys_names) - set(command_systems)))

# validate commands
CommandBitstring = namedtuple("CommandBitstring", "cdte_bits command_bits arg1_bits arg2_bits")
keys = []
values = []
for i, row in command_data.iterrows():
    cdte_b_str = row[1]
    rw_b_str = row[2]
    cmd_b_str = row[3]
    arg1_b_str = row[6]
    arg2_b_str = row[7]
    lookup_instr = row[24]
    lookup_addr = row[25]
    lookup_len = row[26]
    lookup_instr = lookup_instr.replace(" ", "")
    full_cmd_str = (rw_b_str + cmd_b_str).replace(" ", "")
    full_cmd_hex = hex(int(full_cmd_str, 2))
    keys.append(full_cmd_hex)
    values.append((lookup_instr, lookup_addr, lookup_len))

duplicates = set([key for key in keys if keys.count(key) > 1])

if len(set(keys)) != len(keys):
    raise Exception("command codes are not unique")


# generate files that will generate Dict for each detector
py_filename = "commands.py"
dict_name = "COMMAND_LOOKUP"
with open(py_filename, "w") as file:
    file.write(dict_name + " = {} \n")
    for i, key in enumerate(keys):
        file.write(dict_name + "[" + str(key) + "] = (0b" + str(values[i][0]) + ", " + str(values[i][1]) + ", 0x" + str(values[i][2]) + ")\n")

# generate files that will generate C++ std::unordered_map for each detector
c_filename = "commands.h"
struct_dec = "struct MemData {\n\tuint8_t instruction;\n\tuint32_t addr;\n\tuint32_t data;\n};\n"
map_name = "COMMAND_LOOKUP"
map_type = "<char, MemData>"
with open(c_filename, "w") as file:
    file.write("#include <unordered_map>\n\n")
    file.write(struct_dec)
    file.write("std::unordered_map" + map_type + " " + map_name + " = {\n")
    for i, key in enumerate(keys):
        file.writelines("\t{" + str(key) + ", (struct MemData){0b" + str(values[i][0]) + ", " + str(values[i][1]) + ", 0x" + str(values[i][2]) + "}},\n")
    file.write("};")

# generate .json file

# validate outputed files
