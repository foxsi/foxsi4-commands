# foxsi4-commands
List of uplink commands for FOXSI-4 onboard systems and associated tools.

## Command structure

Commands sent to the Formatter from the ground have the following structure:

```
<system ID> <subsystem ID> <R/W bit> <command bits> <arg 1> <arg 2> <EOP>
```