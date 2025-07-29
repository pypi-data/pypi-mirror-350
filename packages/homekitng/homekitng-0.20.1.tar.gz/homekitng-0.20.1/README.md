# HomeKit Python

With this code it is possible to implement a HomeKit Accessory or to simulate a HomeKit Controller.

The code presented in this repository was created based on the Homekit Accessory Protocol release R1 from 2017-06-07.

# Contributors

 * [jc2k](https://github.com/Jc2k)
 * [quarcko](https://github.com/quarcko)
 * [mjg59](https://github.com/mjg59)
 * [mrstegeman](https://github.com/mrstegeman)
 * [netmanchris](https://github.com/netmanchris)
 * [limkevinkuan](https://github.com/limkevinkuan)
 * [tleegaard](https://github.com/tleegaard)
 * [benasse](https://github.com/benasse)
 * [PaulMcMillan](https://github.com/PaulMcMillan)
 * [elmopl](https://github.com/lmopl)
 * [pierrekin](https://github.com/pierrekin)

(The contributors are not listed in any particular order!)

# Installation

Simply use **pip** to install the package:

```bash
pip install homekit
```

This installation can be done without any operating system level installations and should also work on operating systems other than linux (Mac OS X, Windows, ...).  


# HomeKit Accessory
This package helps in creating a custom HomeKit Accessory.

The demonstration uses this JSON in `~/.homekit/demoserver.json`: 
```json
{
  "name": "DemoAccessory",
  "host_ip": "$YOUR IP",
  "host_port": 8080,
  "accessory_pairing_id": "12:00:00:00:00:00",
  "accessory_pin": "031-45-154",
  "peers": {},
  "unsuccessful_tries": 0,
  "c#": 0,
  "category": "Lightbulb"

}
```

Now let's spawn a simple light bulb accessory as demonstration:

```python
#!/usr/bin/env python

import os.path

from homekit import AccessoryServer
from homekit.model import Accessory, LightBulbService


if __name__ == '__main__':
    try:
        httpd = AccessoryServer(os.path.expanduser('~/.homekit/demoserver.json'))

        accessory = Accessory('test_light', 'homekit_python', 'Demoserver', '0001', '0.1')
        lightService = LightBulbService()
        accessory.services.append(lightService)
        httpd.accessories.add_accessory(accessory)

        httpd.publish_device()
        print('published device and start serving')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('unpublish device')
        httpd.unpublish_device()
```

If everything went properly, you should be able to add this accessory to your home on your iOS device.

# HomeKit Controller

The following tools help to access HomeKit Accessories.

## `init_controller_storage`

This tool initializes the HomeKit controller's storage file.

Usage:
```bash
python -m homekit.init_controller_storage -f ${PAIRINGDATAFILE}
```

The option `-f` specifies the name of the file to contain the controller's data.

## `discover`

This tool will list all available HomeKit IP Accessories within the local network.

Usage:
```bash
python -m homekit.discover [-t ${TIMEOUT}] [-u] [--log ${LOGLEVEL}]
```

The option `-t` specifies the timeout for the inquiry. This is optional and 10s are the default.

The option `-u` activates a filter to show only unpaired devices. This is optional and deactivated by default.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

Output:
```
Name: smarthomebridge3._hap._tcp.local.
Url: http://192.168.178.21:51827
Configuration number (c#): 2
Feature Flags (ff): Paired (Flag: 0)
Device ID (id): 12:34:56:78:90:05
Model Name (md): Bridge
Protocol Version (pv): 1.0
State Number (s#): 1
Status Flags (sf): 0
Category Identifier (ci): Other (Id: 1)
```
Hints:

 * Some devices like the Koogeek P1EU Plug need bluetooth to set up wireless (e.g. join the wireless network) before. 
   Use your phone or the proper app to perform this paired devices should not show up


## `identify`

This tool will use the Identify Routine of a HomeKit Accessory. It has 3 modes of operation.

### identify unpaired Homekit IP Accessory

Usage:
```bash
python -m homekit.identify -d ${DEVICEID} [--log ${LOGLEVEL}]
```

The option `-d` specifies the device id of the accessory to identify. Can be obtained via *discovery*.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.


### identify paired Homekit Accessory

Usage:
```bash
python -m homekit.identify -f ${PAIRINGDATAFILE} -a ${ALIAS} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

## `pair`

This tool will perform a pairing to a new IP accessory.

Usage:
```bash
python -m homekit.pair -d ${DEVICEID} -p ${SETUPCODE} -f ${PAIRINGDATAFILE} -a ${ALIAS} [--log ${LOGLEVEL}]
```

The option `-d` specifies the device id of the accessory to pair. Can be obtained via discovery.

The option `-p` specifies the HomeKit Setup Code. Can be obtained from the accessory. This must look like `XXX-XX-XXX` 
(X is a single digit and the dashes are important).

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

The file with the pairing data will be required to send any additional commands to the accessory.

## `list_pairings`

This tool will perform a query to list all pairings of an accessory. The
controller that performs the query must be registered as `Admin`. If this is
not the case, no pairings are listed.

Usage:
```bash
python -m homekit.list_pairings -f ${PAIRINGDATAFILE} -a ${ALIAS} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

This will print information for each controller that is paired with the accessory:

```
Pairing Id: 3d65d692-90bb-41c2-9bd0-2cb7a3a5dd18
        Public Key: 0xed93c78f80e7bc8bce4fb548f1a6681284f952d37ffcb439d21f7a96c87defaf
        Permissions: 1 (admin user)
```

The information contains the pairing id, the public key of the device and permissions of the controller.

## `prepare_add_remote_pairing`

This tool will prepare data required for the `add_additional_pairing` command.

Usage:
```bash
python -m homekit.prepare_add_remote_pairing -f ${PAIRINGDATAFILE} -a ${ALIAS} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device to be added.

The option `--log` specifies the log level for the command. This is optional. 
Use `DEBUG` to get more output.

This will print information to be fed into `homekit.add_additional_pairing` 
(via a second channel):

```
Please add this to homekit.add_additional_pairing:
    -i cec11edd-7363-42c4-8d13-aeb06b608ffc -k 0cbfd3abc377f6c3bfd3b4c119c1c5ff0c840ef1f9530e0f99c68b1f531dd66a
```

## `add_additional_pairing`

This tool is used to tell a HomeKit Accessory accept a new pairing for an 
additional controller.
 
Usage:
```bash
python -m homekit.add_additional_pairing -f ${PAIRINGDATAFILE} -a ${ALIAS} -i ${PAIRINGID} -k ${PUBLIC_KEY} -p ${LEVEL} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device to be added.

The option `-i` specifies the additional controller's pairing id.

The option `-k` specifies the additional controller's public key.

The option `-p` specifies the additional controller's access privileges, this can be `User` or `Admin` for a pairing
with higher privileges.

The option `--log` specifies the log level for the command. This is optional. 
Use `DEBUG` to get more output.

This will print information to be fed into `homekit.finish_add_remote_pairing` (via a second channel):

```
Please add this to homekit.finish_add_remote_pairing:
    -i D0:CA:1E:56:13:AA -m cb:e0:b0:c9:e8:72 -k a07c471e12682b161034b91c0d016201516eb51d9bf1071b6dcf0e3be71e9269
```

## `finish_add_remote_pairing`

This tool finalizes the addition of a pairing to a HomeKit Accessory.

Usage:
```bash
python -m homekit.finish_add_remote_pairing -f ${PAIRINGDATAFILE} -a ${ALIAS} -c ${CONNECTIONTYPE} -i ${DEVICEID} -k ${DEVICEPUBLICKEY} [-m ${MACADDRESS}] [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device to be added.

The option `-i` specifies the accessory's device id.

The option `-k` specifies the accessory's public key.

The option `-m` specifies the accessory's mac address for Bluetooth Low Energy 
accessories. This is not required for IP accessories. 

The option `--log` specifies the log level for the command. This is optional. 
Use `DEBUG` to get more output.

## `remove_pairing`

This tool will remove a pairing from an accessory.

Usage:
```bash
python -m homekit.remove_pairing -f ${PAIRINGDATAFILE} -a ${ALIAS} [-i ${PAIRINGID}] [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `-i` specifies the controller pairing id to remove. This is optional. If left out, the calling controller's
pairing id is used and the controller looses the ability to controll the device. See the output of `list_pairings` 
how to get the controller's pairing id. *Important*: this is not the accessory's device id.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

## `get_accessories`

This tool will read the accessory attribute database.

Usage:
```bash
python -m homekit.get_accessories -f ${PAIRINGDATAFILE} -a ${ALIAS} [-o {json,compact}] [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `-o` specifies the format of the output:
 * `json` displays the result as pretty printed JSON
 * `compact` reformats the output to get more on one screen

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

Using the `compact` output the result will look like:
```
1.1: >accessory-information<
  1.2: Koogeek-P1-770D90 () >name< [pr]
  1.3: Koogeek () >manufacturer< [pr]
  1.4: P1EU () >model< [pr]
  1.5: EUCP031715001435 () >serial-number< [pr]
  1.6:  () >identify< [pw]
  1.37: 1.2.9 () >firmware.revision< [pr]
1.7: >outlet<
  1.8: False () >on< [pr,pw,ev]
  1.9: True () >outlet-in-use< [pr,ev]
  1.10: Outlet () >name< [pr]
```

## `get_characteristic`
This tool will read values from one or more characteristics.

Usage:
```bash
python -m homekit.get_characteristic -f ${PAIRINGDATAFILE} -a ${ALIAS} -c ${CHARACTERISTICS} [-m] [-p] [-t] [-e] [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `-c` specifies the characteristics to read. The format is `<aid>.<cid>`. This option can be repeated to 
retrieve multiple characteristics with one call (e.g. `-c 1.9 -c 1.8`). 
 
The option `-m` specifies if the meta data should be read as well.

The option `-p` specifies if the permissions should be read as well.

The option `-t` specifies if the type information should be read as well.

The option `-e` specifies if the event data should be read as well.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

For example, this command reads 2 characteristics of a Koogeek P1EU Plug:
```
python -m homekit.get_characteristic -f koogeek.json -a koogeek -c 1.8 -c 1.9
```

The result will be a json with data for each requested characteristic:
```json
{
    "1.8": {
        "value": false
    },
    "1.9": {
        "value": true
    }
}
```

## `put_characteristic`
This tool will write values to one or more characteristics.

Usage:
```bash
python -m homekit.put_characteristic -f ${PAIRINGDATAFILE} -a ${ALIAS} -c ${Characteristics} ${value} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `-c` specifies the characteristics to change. The format is `<aid>.<cid> <value>`. This option can be 
repeated to change multiple characteristics with one call  (e.g. `-c 1.9 On -c 1.8 22.3`) . If the value is complex or
some longer chunk of data, it can be read from a file e.g. `-c 1.9 @somefile` with the file containing the value.
 
The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

For example, this command turns of a Koogeek P1EU Plug:
```
python -m homekit.put_characteristic -f koogeek.json -a koogeek -c 1.8 false
```

No output is given on successful operation or a error message is displayed.

## `get_events`

**!!Not yet implemented for Bluetooth LE Accessories!!**

This tool will register with an accessory and listen to the events send back from it.

Usage
```bash
python -m homekit.get_events -f ${PAIRINGDATAFILE} -a ${ALIAS} -c ${Characteristics} [--log ${LOGLEVEL}]
```

The option `-f` specifies the file that contains the pairing data.

The option `-a` specifies the alias for the device.

The option `-c` specifies the characteristics to change. The format is `<aid>.<cid>`. This 
option can be repeated to listen to multiple characteristics with one call.

The option `--log` specifies the log level for the command. This is optional. Use `DEBUG` to get more output.

For example, you can listen to characteristics 1.8 (on characteristic), 1.22 (1 REALTIME_ENERGY) and 
1.23 (2 CURRENT_HOUR_DATA) of the Koogeek P1EU Plug with:
```bash
python -m homekit.get_events -f koogeek.json -a koogeek -c 1.8 -c 1.22 -c 1.23
```
This results in
```
event for 1.8: True
event for 1.22: 6.0
event for 1.23: 0.01666
event for 1.22: 17.0
event for 1.23: 0.06388
event for 1.23: 0.11111
event for 1.22: 18.0
event for 1.23: 0.16111
event for 1.8: False
```

## `debug_proxy`

To assist the adoption of new accessories, there is a debug proxy. See 
[its documentation](./doc/DebugProxy.md) for more details.
