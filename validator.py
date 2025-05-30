import pandas as pd
import json, sys
from collections import namedtuple

# files we need
command_file_xlsx = "commands/cdte1/cdte1_command_deck.xlsx"
command_file = "command_deck.csv"
systems_file = "systems.json"
output_json_filename = "commands/cdte1/cdte1_commands.json"

if len(sys.argv) == 2:
    command_file_xlsx = sys.argv[1]
    # output_json_filename = command_file_xlsx[0:command_file_xlsx.rfind(".")] + ".json"
    output_json_filename = command_file_xlsx
    output_json_filename = output_json_filename.replace("xlsx", "json")
    output_json_filename = output_json_filename.replace("_deck", "s")

    print("writing to " + output_json_filename)
elif len(sys.argv) == 1:
    print("using default file names")

# convert xlsx to csv
try:
    excel_data = pd.read_excel(command_file_xlsx, "all_systems", index_col=None)
    excel_data.to_csv(command_file, encoding='utf-8', index=False)
    pass
except:
    raise(Exception("couldn't open " + command_file_xlsx))

# read command deck in
try:
    command_data = pd.read_csv(command_file)
except:
    raise Exception("couldn't open " + command_file)

# read systems list in
sys_dict = {}
try:
    with open(systems_file) as sys_json:
        sys_dict = json.load(sys_json)
except:
    raise Exception("couldn't open systems list")

# clean up systems
sys_names = [sys["name"].upper() for sys in sys_dict]
sys_ids = [sys["hex"] for sys in sys_dict]

# clean up commands
head = list(command_data.iloc[0])
command_systems = [name.upper() for name in head[11:23]]

command_data = command_data[1:]
command_data.dropna(axis=0, how="all", inplace=True)

order = command_data.iloc[:,27]

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

if len(order) != len(set(order)):
    raise Exception("order is not unique")

# validate commands
CommandBitstring = namedtuple("CommandBitstring", "cdte_bits command_bits arg1_bits arg2_bits")
keys = []
values = []
for i, row in command_data.iterrows():
    cdte_b_str = row.iloc[1]
    rw_b_str = row.iloc[2]
    cmd_b_str = row.iloc[3]
    arg1_b_str = row.iloc[6]
    arg2_b_str = row.iloc[7]
    lookup_instr = row.iloc[24]
    lookup_addr = row.iloc[25]
    lookup_len = row.iloc[10]
    lookup_instr = lookup_instr.replace(" ", "")
    full_cmd_str = (rw_b_str + cmd_b_str).replace(" ", "")
    # full_cmd_hex = hex(int(full_cmd_str, 2))
    full_cmd_hex = row.iloc[4]
    keys.append(full_cmd_hex)
    values.append((lookup_instr, lookup_addr, lookup_len))

duplicates = set([key for key in keys if keys.count(key) > 1])

if len(set(keys)) != len(keys):
    print("duplicates: " + str(duplicates))
    raise Exception("command codes are not unique")

# generate .json file
# edit header for json variable naming
json_head = head
json_head[5] = "arg1." + json_head[5]
json_head[6] = "arg1." + json_head[6]
json_head[7] = "arg2." + json_head[7]
json_head[8] = "arg2." + json_head[8]
json_head[9] = "reply." + json_head[9]
json_head[10] = "reply." + json_head[10]

json_data = command_data
json_data.columns = json_head

# write the file
with open(output_json_filename, "w") as file:
    json_result = json_data.to_json(orient="records")
    parsed = json.loads(json_result)
    json_string = json.dumps(parsed, indent=4)
    file.write(json_string)

# validate outputed files
