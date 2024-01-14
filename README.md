# foxsi4-commands
A list of uplink commands for FOXSI-4 onboard systems and associated tools.

## About this repository

This repository is used to manage changes to the FOXSI-4 flight command list. There is a full command deck and relevant metadata for each subsystem. All system-specific metadata is stored in the top-level configuration file, [systems.json](systems.json). This file includes all systems visible to the FOXSI-4 Formatter.

A script ([expand_systems.py](expand_systems.py)) can be used to generate a nearly fully elaborated version of [template_systems.json](template_systems.json) called [systems.json](systems.json) that substitutes JSON content where links previously existed. This is done for all fields except `commands`, which references a large array of command-related JSON content for each system.

For system-specific commands, a script ([validator.py](validator.py)) exists to generate and validate all commands in the deck (guarantee command uniqueness and applicability to onboard systems) and generate command files for integration in the flight software.

## Command structure

Commands sent to the Formatter from the ground have the following structure:

```
<system ID> <command ID>
```

Each field is 1 byte wide. A valid uplink command is 2 bytes wide.

### Editing commands:

At your terminal, navigate to a folder you want this repository in. Then:

```bash
git clone https://github.com/foxsi/foxsi4-commands.git
cd foxsi4-commands.git
git checkout <your branch name>
git pull
```

where `<your branch name>` is `cmos`, `timepix`, `cdte`, or another. Now, make your edits to the `.xlsx` file under [commands](commands) you would like to modify. When you are done, validate uniqueness for your commands and convert JSON like this:
```bash
python3 foxsi4-commands/validator.py <path/to/your/xlsx/file>
```

If you are modifying `systems.json`, apply changes made in subfolders to the global system configuration files like this:
```bash
python3 foxsi4-commands/expand_systems.py
```

```bash
git add <all> <the> <files> <you> <edited>
git commit -m "<a short messages describing your edits>"
git push
```