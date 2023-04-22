# foxsi4-commands
List of uplink commands for FOXSI-4 onboard systems and associated tools.

## Using this repository

This repository exists to centrally manage changes to the FOXSI-4 flight command list. The full command deck and relevant metadata is in [command_deck.csv](command_deck.csv). A script ([validator.py](validator.py)) exists to validate all commands in the deck (guarantee command uniqueness and applicability to onboard systems) and generate command files for integration in the flight software.

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

### CdTe commands

For the CdTe system, setting the last for bits of `subsystem ID` specifies which canisters the command will be applied to. For example, setting to `0b0000 0100` will send the command to canister 3, and setting `0b0000 0101` will send the command to both canisters 3 and 1. Setting `subsystem ID` to `0b0000 0000` will send the command to the CdTe DE. The first four digits have are unused and should be set to 0. For other onboard systems, this byte is ignored. 

