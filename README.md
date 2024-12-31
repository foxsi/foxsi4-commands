# foxsi4-commands
A list of uplink commands for FOXSI-4 onboard systems and associated tools.

## Contents
- [foxsi4-commands](#foxsi4-commands)
  - [Contents](#contents)
  - [About this repository](#about-this-repository)
  - [Command structure](#command-structure)
    - [Editing commands](#editing-commands)
  - [`systems.json`](#systemsjson)
    - [Structure](#structure)
    - [`ethernet_interface`](#ethernet_interface)
    - [`spacewire_interface`](#spacewire_interface)
    - [`uart_interface`](#uart_interface)
    - [Commanding](#commanding)
    - [`ring_buffer_interface`](#ring_buffer_interface)
      - [Note on optional header/footer fields](#note-on-optional-headerfooter-fields)
    - [`timing`](#timing)
  - [Tips and caveats](#tips-and-caveats)
    - [1. Formatter v1.2.0 (FOXSI-4 flight) discrepancy](#1-formatter-v120-foxsi-4-flight-discrepancy)


## About this repository
This repository tells the FOXSI software how the FOXSI hardware is configured. It also provides some global software configuration information. There is a full command deck and relevant metadata for each subsystem. All system-specific metadata is stored in the top-level configuration file, [systems.json](systems.json). This file includes all systems visible to the FOXSI Formatter. This file is loaded by both Formatter software and GSE software when the start, so that they can agree on things like packet definitions and Ethernet interfaces.

>[!IMPORTANT] `systems.json` is a very important file! 
> It tells the Formatter and GSE software about the hardware configuration. If you want to get familiar with the configuration of the FOXSI software and hardware, read this file.

A script ([expand_systems.py](expand_systems.py)) can be used to generate a nearly fully elaborated version of [template_systems.json](template_systems.json) called [systems.json](systems.json) that substitutes JSON content where paths previously existed. This is done for all fields except `commands`, which references a large array of command-related JSON content for each system. 

For system-specific commands, a script ([validator.py](validator.py)) exists to generate and validate all commands in the deck (guarantee command uniqueness and applicability to onboard systems) and generate command files for integration in the flight software.

A flight system (such as the [Formatter software](https://github.com/foxsi/foxsi-4matter) or [GSE software](https://github.com/foxsi/GSE-FOXSI-4)) that uses `foxsi4-commands` for configuration requires only:
1. `systems.json` to describe each subsystem.
2. `commands/` to include all the commands for each subsystem.

If you modify this file for the Formatter, you also need to modify it for the GSE. So they don't disagree about interfaces.
## Command structure
See [`commands/README.md`](commands/README.md) for a lot of detail on commanding, or stay here for an overview.

Commands sent to the Formatter from the ground have the following structure:

```
<system ID> <command ID>
```

Each field is 1 byte wide. A valid uplink command is 2 bytes wide.

### Editing commands

Create a fork of this repository and add commands via PR. Make your edits to the `.xlsx` file under [commands](commands) that you would like to modify. For example, if you want to modify commands for CdTe 3, open the file `commands/cdte3/cdte3_command_deck.xlsx`. When you are done, validate uniqueness for your commands and convert to JSON like this:
```bash
python3 validator.py path/to/your/xlsx/file
```

If you are modifying `systems.json`, you should edit configuration in subfolders. For example, if you want to change the GSE's Ethernet configuration, best practice is to edit `ethernets/gse/ethernet_interface.json`. Then apply changes made in subfolders to the global system configuration files as follows. Note that because of the relative paths used in the JSON, *you need to run this from the parent directory of `foxsi4-commands`*:
```bash
python3 foxsi4-commands/expand_systems.py
```

## `systems.json`
This section describes the structure and content of `systems.json`. 

This is the principal source of configuration data for FOXSI Formatter and GSE software. It is a very important file. It tells the software how the hardware is configured. Don't be afraid to edit it, no hardware will break permanently. But make small changes at a time, because the whether the system (FOXSI as a data source/sink) works or not is very sensitive to the content of this file.

You should have a little familiarity with [JSON syntax](https://javaee.github.io/tutorial/jsonp001.html) for the rest of this.

### Structure
At the top level, `systems.json` is a [JSON](https://en.wikipedia.org/wiki/JSON#Data_types) array of JSON objects which represent *systems*. What is a system in this context? A system is, in a loose sense, a thing that the Formatter can talk to. **A system object always contains two key/value pairs: `name` and `hex`:**
```jsonc
{
    [ // the array of systems
        {
            "name": "a_system",
            "hex":  "0x01"
        },
    ] //...
}
```

>[!NOTE] JSON does not support hexadecimal notation for integers
> For example, in C++ the literal `0x0f` is identical to `15`. This is not the case in JSON files. The Formatter and GSE software have come to expect `systems.json` to write some fields as hexadecimal *strings*. Instead of writint `0x0f`, write the string `"0x0f"`. There's an example in the `"hex"` field in the snippet above.

The `hex` value is unique to each system. `validator.py` will complain if `systems.json` multiple systems with the same `hex` value.

The order of system definitions (i.e. "gse" appearing before "cdte1") in the list is not meaningful.

### `ethernet_interface`
All systems except `timepix` and `uplink` contain an `ethernet_interface` block. There are variations in specificity in the `ethernet_interface` definitions for different systems. This block must contain at least an `address` key:
```jsonc
{
    "ethernet_interface": {
        "address": "192.168.1.10"
    }
}
```
For the `formatter` (`0x01`) system, `address` is the only field defined. For all other systems, their `ethernet_interface` definitions must also include the following: 
- `protocol`: the [Transport Layer](https://en.wikipedia.org/wiki/Transport_layer#Comparison_of_Internet_transport_layer_protocols) protocol used for the Formatter to send data to this system. Can be either `"tcp"` or `"udp"` (include the quote marks, these are JSON strings).
  - Note: unfortunately, if you want to switch an interface from UDP to TCP or vice versa, you will also need to edit Formatter code. It is not smart enough to create the right type of socket purely by looking at `systems.json`.
- `port`: the [port number](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) the Formatter will send data to ***and*** expect to receive data from. It is assumed that the same port number will be used on the Formatter and remote system!
  - You may need root permissions to use certain ports ≤1024, depending on your OS.
- `max_payload_bytes`: the largest block of data, in bytes, that is permitted to be sent on this interface. If you want to send more data than this, it will need to be fragmented.
  - Quick aside: to pick a value here, you should identify your network's [MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit) (probably 1500 bytes), then subtract the IP header length (20 bytes) and UDP or TCP header length (8 bytes for UDP or 20+ bytes for TCP). Larger packets can be sent for an efficiency cost due to the [fragmentation overhead](https://en.wikipedia.org/wiki/IP_fragmentation#Impact_on_network_forwarding).

But that's not all. If the `ethernet_interface` is responsible for commanding the `system`, it may contain [additional fields](#commanding).

### `spacewire_interface`
Some systems use SpaceWire RMAP for communication (CdTes and CMOSes) with the Formatter. The Formatter **only** supports SpaceWire interfaces via Shimafuji's SPMU-001, which receives and transmits SpaceWire packets over a TCP connection. 

Because SpaceWire communication depends entirely on an Ethernet connection, any `system` that communicates over SpaceWire requires an `ethernet_interface` to support it. 

If you want to learn more about SpaceWire, see [ECSS-E-ST-50-12C](https://ecss.nl/wp-content/uploads/2019/05/ECSS-E-ST-50-12C-Rev.1(15May2019).pdf). 

If you want to learn more about RMAP, see [ECSS-E-ST-50-52C](https://ecss.nl/wp-content/uploads/standards/ecss-e/ECSS-E-ST-50-52C5February2010.pdf).

Like Ethernet-based networks, SpaceWire networks have some static configuration data. A `spacewire_interface` definition in `systems.json` captures that information in the following elements (see the ECSS-E-ST-50-52C standard above for more detail):
- `target_logical_address`: the 1-byte logical address of the RMAP target. This is w.r.t Formatter, so this field should always represent a detector readout system's logical address.
- `source_logical_address`: the 1-byte logical address of the RMAP source. This is w.r.t Formatter, so this field should always represent the Formatter's logical address (`0xfe`).
- `target_path_address`: an arbitrary length path address from the Formatter to the target detector readout system. This address specifies the intermediate ports in the SpaceWire network the message must pass through in order to reach its destination.
- `reply_path_address`: a 0, 4, 8, or 12-byte path address from the target detector readout system back to the Formatter. This address specifies the intermediate ports in the SpaceWire network the a reply message must pass through in order to get back to the Formatter.
- `key`: an arbitrary 1-byte value. SpaceWire replies will include the same `key` as the read message that prompted them. This can be used for validation of responses. Note: this field can be changed dynamically by the Formatter, it doesn't need to be defined staticly. But it is for now.
- `crc_draft`: only `"f"` is supported. This specifies the cyclic redundancy check (CRC) version that should be used.
- `hardware`: only `"spmu-001` is supported.

### `uart_interface`
This one is a little simpler. A `uart_inteface` should contain at least these fields:
- `tty_path`: a UNIX-style file path to the serial device used for the UART communication. On Linux, these appear in `/dev` and have names that start with `tty`. Note that the Formatter and GSE codes are totally unable to "discover" the right serial device—they rely on `systems.json` identifying the right one for them.
- `baud_rate`: the baud rate that is used for UART communication. Note that this needs to be negotiated with the other side of the interface as well.
- `parity_bits`: the number of parity bits used. Sometimes UART messages are referred to as having "odd" or "even" parity—set `"parity_bits": 1` for odd parity, `"parity_bits": 2` for even parity, and `"parity_bits": 0` for no parity bit.
- `data_bits`: the number of data bits in a UART packet. 
- `stop_bits`: the number of stop bits to use.
- `max_payload_bytes`: the size of the largest single message (in bytes) that this interface will handle. 

For `max_payload_bytes`, note that the usage here is slightly different from `ethernet_interface`. In `ethernet_interface` the value of `max_payload_bytes` is used to constrain packetization of large frames, and derives from the network MTU. In UART, bytes come across the wire one by one, so there is no notion of MTU, and you can choose whatever `max_payload_bytes` you want. This value is purely used to allocate buffers for holding that data.

### Commanding
If a `system` receives commands from the Formatter, two top-level fields need to be defined in the JSON: `command_type` and `commands`.
```jsonc
{
    "name": "cdte1",
    "hex":  "0x09",
    "command_type": "spacewire",
    "commands": "foxsi4-commands/commands/cdte1/cdte1_commands.json"
}
```

Here, `command_type` is a string that defines the interface that will be used for sending commands to the `system`. A `system` may have multiple physical interfaces, so `command_type` informs the Formatter which one to use for commanding. 

The `commands` field is a string representing an path in a UNIX filesystem (i.e. with forward slashes—unless the Formatter gets ported to Windows). The path points inside this repository to the specific JSON command file for that system.

### `ring_buffer_interface`
If a `system` sends data back to the Formatter, it must have one or more `ring_buffer_interface` defined in `systems.json`. 

> [!NOTE]
> 
> This is a bit of an abuse of nomenclature—`ring_buffer_interface` was originally implemented in the Formatter to handle large ring buffers of detector data in CMOS and CdTe. But this system (and the Formatter `FramePacketizer`/`PacketFramer` objects that ingest it) can handle non-ring buffer data as well. So you'll see `ring_buffer_interface` defined for systems that don't have ring buffers, such as Timepix and Housekeeping. A better name would be `buffer_interface` or something, but it's too late now for regret.

 `ring_buffer_interface` is a list of named objects. The names must be one of:
| Name | Description |
|------|-------------|
| `pc` | Photon-counting data |
| `ql` | Quick-look data |
| `tpx` | Timepix data |
| `hk` | General housekeeping data |
| `pow` | Power data |
| `rtd` | Temperature sensor data |
| `intro` | Microcontroller software health data |
| `ping` | Formatter software health/ping data |

If you want to include new *types* of data for downlink, you can create new names in `ring_buffer_interface` objects. But! You will also need to modify the Formatter's [`Parameters.h`](https://github.com/foxsi/foxsi-4matter/blob/main/include/Parameters.h) file and the GSE's [`listening.py`](https://github.com/foxsi/GSE-FOXSI-4/blob/main/FoGSE/listening.py) to include these new strings and their hex encoding in the downlink header.

So a `ring_buffer_interface` might look like this:
```jsonc
{
    "ring_buffer_interface": {
        "pc": {
            // properties of the photon-counting data interface
        },
        "hk": {
            // properties of the housekeeping data interface
        }
    }
}
```

There are five fields that define each data type in a `ring_buffer_interface`, all need to be provided by the detector provider. All of these should be written as hex strings:
- `ring_frame_size_bytes`: the size of a full frame of data in the ring buffer. This is defined by the detector provider. This is the minimum parsable unit of data. For this system and data type, the GSE logging will assemble frames of this size for logging.
- `ring_start_address`: the memory address *in the remote system's memory map* where the ring buffer begins. 
- `frames_per_ring`: the number of full frames of data that can be stored in the ring. If the size of the ring buffer is `ring_size_bytes` and `/` represents integer (floor) division, then `ring_size_bytes / ring_frame_size_bytes == frames_per_ring`.
- `ring_write_pointer_address`: the address *in the remote system's memory* storing the current write frame pointer in the ring buffer. The Formatter will access remote memory from this pointer up to `ring_write_pointer_address + ring_frame_size_bytes` to retrieve the frame data.
- `ring_write_pointer_width`: the size, in bytes, of the `ring_write_pointer_address` field.

Note that the `housekeeping` and `timepix` systems define all but `ring_frame_size_bytes` with dummy values, since those systems do not contain ring buffers or write pointer-based remote memory access. The Formatter just sends them request messages, and they respond with data.

But wait, there's more.

In the physical interface that includes the `ring_buffer_interface` (meaning `ethernet_interface`, `uart_interface`, or `spacewire_interface`), you need to include additional fields to support the packetization of the data described in the `ring_buffer_interface`. You should include:
- `static_header_size`: the fixed size (in bytes) of the (at the end) of packets coming from the remote system into the Formatter. This header is not part of the frame data that you wish to downlink, and so should be removed by the Formatter before trying to assemble frames for downlink.
- `static_footer_size`: the fixed size (in bytes) of the footer (at the end) of packets coming from the remote system into the Formatter. This footer is not part of the frame data that you wish to downlink, and so should be removed by the Formatter before trying to assemble frames for downlink.

For SpaceWire system that communicate with the Formatter via the SPMU-001, there is a 12-byte header on all packet transfers (and no footer). This header is used by the SPMU-001 to encapsulate SpaceWire messages in Ethernet-based TCP packets. Note that the TCP/IP/Ethernet headers *do not appear* to the Formatter, because they are already removed by the network API used.

For more complicated transfer schemes, in which systems package data with different size header/footer for only the *first* packet in a larger frame transfer, you can also include:
- `initial_header_size`: the header size (in bytes) of the first packet in the transfer. This value is added on top of `static_header_size`.
- `initial_footer_size`: the footer size (in bytes) of the first packet in the transfer. This value is added on top of `static_footer_size`.
- `subsequent_header_size`: the header size (in bytes) of any packet but the first in the transfer. This value is added on top of `static_header_size`.
- `subsequent_footer_size`: the footer size (in bytes) of any packet but the first in the transfer. This value is added on top of `static_footer_size`.

#### Note on optional header/footer fields
Note that for these optional `initial*`/`subsequent*` fields, the Formatter will still remove `static_header_size` and `static_footer_size` amount of data from the start and end of each packet before frame reassembly. So if, e.g., your data will arrive with a 12 byte header initially and a 4 byte header after that, and no footer, you can set:
```jsonc
{
    "initial_header_size": 8,
    "subsequent_header_size": 0,
    "static_header_size": 4,
}
```
or, equivalently,
```jsonc
{
    "initial_header_size": 11,
    "subsequent_header_size": 3,
    "static_header_size": 1,
}
```

### `timing`
System communication is not guaranteed. The Formatter requests data from detector systems by sending request commands. Then those detector systems are expected to respond. If they fail to respond in time, the attempt will timeout, the Formatter will retry a number of times, then will move on to other systems. This is all managed by the `timing` JSON block. This block lives at the top level for a system (it is not buried inside an `ethernet_interface`), and should contain:
- `retry_max_count`: if the system doesn't respond to the Formatter's request within `receive_timeout_millis`, this field sets the maximum number of times to resend the request.
- `receive_timeout_millis`: after request information from a system, the Formatter will wait this amount of milliseconds for a response.
- `intercommand_spacing_millis`: unused. 
- `total_allocation`: unused.
- `command`: unused.
- `request`: unused.
- `reply`: unused.
- `idle`: unused.

There are several fields that are currently unused by the Formatter. These are placeholders for use if the software design changes to timeout



## Tips and caveats
### 1. [Formatter v1.2.0](https://github.com/foxsi/foxsi-4matter/releases/tag/v1.2.0) (FOXSI-4 flight) discrepancy
[FOXSI-4 flight Formatter code (v1.2.0)](https://github.com/foxsi/foxsi-4matter/releases/tag/v1.2.0) transmitted downlink data to `gse.ethernet_interface.address`. But the GSE listened for downlink on `gse.ethernet_interface.mcast_group`. So if you use Formatter v1.2.0, you need to manually set *only the Formatter's copy of `systems.json`* to have `gse.ethernet_interface.address` match the GSE's `gse.ethernet_interface.mcast_group`. For FOXSI-4 flight, the Formatter's `systems.json` looked like this:
```jsonc
{
    "ethernet_interface": {
        "protocol": "udp",
        "address": "224.1.1.118",
        "port": 9999
        // ...
    }
}
```
and the GSE's `systems.json` looked like this:
```jsonc
{
    "ethernet_interface": {
        "protocol": "udp",
        "address": "192.168.1.118",
        "mcast_group": "224.1.1.118",
        "port": 9999
        // ...
    }
}
```

