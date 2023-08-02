# foxsi4-commands
A list of uplink commands for FOXSI-4 onboard systems and associated tools.

## About this repository

This repository is used to manage changes to the FOXSI-4 flight command list. There is a full command deck and relevant metadata for each subsystem. A script ([validator.py](validator.py)) exists to generate and validate all commands in the deck (guarantee command uniqueness and applicability to onboard systems) and generate command files for integration in the flight software.

A good entry point is the [systems.json](systems.json) file. This file names, identifies, and captures system-specific interface information for each system the Formatter may interact with. Each commandable system in [systems.json](systems.json) should include an interface section detailing the physical protocol parameters used for the interface, and a path to a command file for that system.

## Command structure

Commands sent to the Formatter from the ground have the following structure:

```
<system ID> <subsystem ID> <R/W bit> <command bits> <arg 1> <arg 2>
```

where the different components are structured like this:

| Component     | Length [bits]     | Description |
|:--------------|:-----------------:|:------------|
| `system ID`   | 8                 | Selects the onboard system (like Formatter, CdTe DE, CMOS 1, etc) to send the command to. |
| `subsystem ID`| 8                 | Selects the subsystem (CdTe 1, 2, 3, or 4) to send the command to. Otherwise disregarded. |
| `R/W bit`     | 1                 | Set `1` for read and `0` for write commands. |
| `command bits`| 7                 | This bit string is concatenated to the `R/W bit` to create a unique ID for each command. |
| `arg 1`       | 32 (max)          | This argument has a different role for a few commands, but is totally unused for most commands. See [command_deck.csv](command_deck.csv) for details. |
| `arg 2`       | 32 (max)          | This argument has a different role for a few commands, but is totally unused for most commands. See [command_deck.csv](command_deck.csv) for details. |

In the Formatter, the `R/W bit` and `command bits` are concatenated to form a unique **`command id`** byte. This **`command id`** is then used in a lookup table unique to a specific detector system to find command data to send to that detector system. This way, the Formatter has a generic interface for command transmission, which relies on command implementation defined by each detector team for their specific system. The command lookup by **`command id`** is [defined below](lookup_section).

#### Note on CdTe commands

For the CdTe system, I  plan to use the last four bits of `subsystem ID` to specify which canisters to apply the command to. For example, setting to `0b0000 0100` would send the command to canister 3, and setting `0b0000 0101` would send the command to both canisters 3 and 1. Setting `subsystem ID` to `0b0000 0000` would send the command to the CdTe DE. Using only a lookup table, this would mean enumerating 16 versions of each command. So we should define a less rigid interface to use for this purpose.

### [Command lookup](#lookup_section)

After editing [command_deck.csv](command_deck.csv), run the [validator.py](validator.py) script to validate commands and update the [commands.h](commands.h), [commands.py](commands.py), [commands.json](commands.json) output files. The file [commands.h](commands.h) will contain a C++ `std::unordered_map` which can be indexed by `command id` keys, returning a custom data structure defined to hold SpaceWire instruction byte, memory address, and data (for write commands) or reply data length (for read commands): 

```C++
struct MemData {
    uint8_t instruction;    // SpaceWire instruction byte
    uint32_t addr;          // remote memory address
    uint32_t data;          // data to write or length of data to be read
};
```

The file [commands.py](commands.py) defines a Python Dict object, mapping input `command id` key to a Tuple of SpaceWire instruction byte, memory address, and data.

The file [commands.json](commands.json) provides the same information in the .xlsx or .csv, but formatted as a .json for use in software.

## Actions for detector teams

Detector teams (CMOS and CdTe) should populate [command_deck.csv](commands.csv) with SpaceWire instruction byte, write data, or read data length for each command in the appropriate fields. 

After editing, please push your modified files to your branch in this repository.

### Step-by-step:

At your terminal, navigate to a folder you want this repository in. Then:

```console
$ git clone https://github.com/foxsi/foxsi4-commands.git
$ cd foxsi4-commands.git
$ git checkout <your branch name>
$ git pull
```

where `<your branch name>` is either `cmos`, `timepix`, or `cdte`. Now, make your edits to the [commands.csv](commands.csv). When you are done, 

```console
$ git add <all> <the> <files> <you> <edited>
$ git commit -m "<a short messages describing your edits>"
$ git push
```