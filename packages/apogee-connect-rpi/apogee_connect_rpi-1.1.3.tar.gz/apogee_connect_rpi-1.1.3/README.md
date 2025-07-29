# Apogee Connect for Raspberry Pi 

## Table of Contents
- [Intro](#prerequisite)
- [Command Line Application](#command_line_application)
   - [Installation](#installation)
   - [Basic Example](#basic_example)
   - [Commands](#commands)
- [Python Module API](#python_module_api)
   - [Installation](#installation)
   - [Functions](#functions)
- [Contact](#contact)

## Intro

Apogee Connect for Raspberry Pi is a lightweight script intended for automating the data collection process with Apogee's Bluetooth sensors. 

Apogee Connect can be used in two different ways: 

1. As a standalone command line application with straightforward commands for interacting with Apogee's Bluetooth sensors. 

2. As a Python module for those looking to implement the application functionality directly into their own Python script (The method assumes an existing familiarity with Python, virtual environments, and pip).

#### *Prerequisite*

In order to install, you will need pip (the package installer for Python). Pip is likely already included by default on a Raspberry Pi or if Python was installed from source. You can confirm pip is installed by running the command:

`pip --version`

If pip isn't already installed, visit the following site for instructions on a simple pip installation:

[https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)


## Command Line Application

### Installation

#### *Install*

1) We will use pipx, which is a tool that runs Python modules as a standalone command line application. In terminal, run the following command (It may be necessary to close and restart the terminal after installing pipx for it to be recognized):

`sudo apt install pipx`

2) Install Apogee Connect for Raspberry Pi from the Python Package Index by running the following command in terminal:

`pipx install apogee-connect-rpi`

3) Add the install location to your PATH environment variables so that it can be run from anywhere in the terminal.

`pipx ensurepath`

4) Verify installation by running the following command (It may be necessary to close and restart the terminal first for the changes to take effect):

`apogee --version`

#### *Update*

To update to the latest version, run the following command in terminal:

`pipx upgrade apogee-connect-rpi`

#### *Uninstall*

To uninstall, run the following command in terminal:

`pipx uninstall apogee-connect-rpi`

## Basic Example

Note: `apogee` is the command that can be run from the terminal at any location to use the app.
 
1. Scan for nearby Apogee sensors to obtain sensor's MAC address required for connection.

`apogee scan`

2. Start collecting data from the sensor with the MAC address of AA:BB:CC:DD:EE:FF and set a logging interval of 10 minutes.

`apogee collect AA:BB:CC:DD:EE:FF --interval 10`
 
3. See a list of all currently collecting sensors along with the number of logs currently collected, data file location, start/end time, etc.

`apogee list`
 
4. Stop data collection from the sensor with the MAC address of AA:BB:CC:DD:EE:FF, but not until the epoch timestamp of 1726247820 (Unix timestamp in seconds).

`apogee stop AA:BB:CC:DD:EE:FF --end 1726247820`


### Commands
*Key:*

`apogee command <required_argument> [--optional_arguments (default: value)]`


### *collect*

*Usage*

Collect data from an Apogee sensor and write the data to a csv file. 

Automatic collection is the default collection mode, which will turn the sensor's logging on and then automatically collect all available data and record it in a csv file. The frequency with which the Raspberry Pi will "wake up" and check for available data from all sensors can be adjusted through the `config` command.

If a manual collection mode is needed, add the `--manual` flag to the command. The first time this command is used for a sensor, the application will turn the sensor's logging on with the included interval, start/end time, etc. Then, use the `collect` command again with the `--manual` flag to collect available data from the sensor and add it to the csv file (when collecting data, the `--file` argument can be included to store the data in a different file than what was originally set but `--interval`, `--start`, and `--end` will be ignored).


*Examples*

`apogee collect D7:52:21:95:5C:6C`

`apogee collect D7:52:21:95:5C:6C  --interval 10 --start 1720647720 --end 1721250915 --file /usr/Documents/greenhouse-data.csv --append`

`apogee collect D7:52:21:95:5C:6C  --interval 10 --file /usr/Documents/greenhouse-data.csv --manual --overwrite`

*Documentation*

`apogee collect <MAC address> [--interval (default: 5)] [--start (default: Now)] [--end (default: Never)] [--file (default: ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv)] [--overwrite] [--append] [--manual]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| Mac Address| N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF |
| -i, --interval | 5 minutes | The interval that sensor will log data (must be a positive integer) |
| -s, --start | Now | Start time for data collection using epoch time (Unix timestamp in seconds) |
| -e, --end | Never | End time for data collection using epoch time (Unix timestamp in seconds) |
| -f, --file | ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv | File path to write data to csv file. Will create folders and files if they don’t exist. |
| -a, --append | False | Add this flag to automatically append to an existing data file. |
| -o, --overwrite | False | Add this flag to automatically overwrite an existing data file. |
| -m, --manual | N/A | Add this flag for manual data collection mode.|  


### *config*

*Usage*

Change or view the application settings.

*Examples*

`apogee config`

`apogee config --filepath /usr/documents/live-data --precision 4 --temp F --par-filtering True`

`apogee config --reset`

*Documentation*

`apogee config [--filepath (default: ~/Apogee/apogee_connect_rpi/data/)] [--precision (default: 2)] [--temp (default: C)] [--par-filtering (default: False)] [--collection-frequency (default: 5)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| (N/A)| (N/A) | If no optional arguments are provided, the current configuration will be displayed. |
| -f, --filepath | ~/Apogee/apogee-connect-rpi/data/ | The default folder to save collected data. Adjust to avoid needing to specify full filepath every time data collection is initiated. |
| --p, --precision | 2 | Maximum number of decimal places for collected data. |
| -t, --temp | C | Change preferred temperature units. Enter “C” for Celsius and “F” for Fahrenheit (without quotations). |
| -pf, --par-filtering | False | Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. Enter "True" or "False" (without quotations). |
| -cf, --collection-frequency | 5 | Frequency in minutes to check for new data logs and add to .csv data file (This is different than the data logging interval for the sensor). Must be between 5 - 60 minutes. |
| -r, --reset | N/A | Add this flag to reset configuration back to default values. |

### *list*

*Usage*

List all the sensors currently collecting data.

*Example*

`apogee list`

*Documentation*

`apogee list`


### *scan*

*Usage*

Scan for nearby Apogee sensors

*Example*

`apogee scan`

`apogee scan --time 10`

*Documentation*

`apogee scan [--time (default: 5-20)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
|-t, --time | 5-20 | Number of seconds to scan for Apogee Bluetooth sensors. If not set, scanning will continue until no new sensors are being discovered or a maximum of 20 seconds. |


### *stop*

*Usage*

Stop data collection from an Apogee sensor. Can optionally use the `--all` flag to stop data collection from all Apogee sensors instead.

*Examples*

`apogee stop D7:52:21:95:5C:6C`

`apogee stop D7:52:21:95:5C:6C --end 1724428813`

`apogee stop --all`

*Documentation*

`apogee stop <MAC address> [--end (default: now)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| MAC address | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF (Required unless the '--all' flag is used). |
| -e, --end | Now | End time for data collection using epoch time (Unix timestamp in seconds). Cannot be used when using the '--all' flag. |
| -a, --all | N/A | Stop data collection for all sensors (Can be used instead of the MAC address requirement).|

### *transfer*

*Usage*

Transfer data from an Apogee sensor for a desired logging interval. This command is separate from the collect command and is just used to obtain a specific time period or previously logged data.

*Examples*

`apogee transfer D7:52:21:95:5C:6C`

`apogee transfer D7:52:21:95:5C:6C --start 1720647720 --end 1721250915 --file /usr/documents/greenhouse-data.csv --overwrite`

*Documentation*

`apogee transfer <MAC address> [--start (default: Now)] [--end (default: Never)] [--file (default: ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv)] [--append] [--overwrite]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| MAC address | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF. |
| -s, --start | Now | Start time for data collection using epoch time (Unix timestamp in seconds) |
| -e, --end | Never | End time for data collection using epoch time (Unix timestamp in seconds) |
| -f, --file | ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv | File path to write data to csv file. Will create folders and files is they don’t exist. |
| -a, --append | N/A | Add this flag to automatically append data to a file if it exists instead of overwriting. |  
| -o, --overwrite | False | Add this flag to automatically overwrite an existing data file. |

### *version*

*Usage*

Show current application version

*Example*

`apogee --version`

*Documentation*

`apogee --version`


### *help*

*Usage*

Show help menu for entire application or for specific command, depending on usage

*Example*

`apogee --help`

`apogee collect --help`

*Documentation*

Entering just `--help` (or `-h`) will show a high-level overview of available commands.
Entering a command followed by `--help` will show a menu with required and optional arguments.
Any unrecognized command will also print the high-level overview help menu.


## Python Module API

#### *Install*

1) Simply install Apogee Connect for Raspberry Pi from the Python Package Index by running the following command in terminal within an activated virtual environment: 

`pip install apogee-connect-rpi`

#### *Update*

To update to the latest version, run the following command in terminal:

`pip install apogee-connect-rpi --upgrade`

#### *Uninstall*

To uninstall, run the following command in terminal:

`pip uninstall apogee-connect-rpi`


### Functions

### *collect*

*Usage*

Collect data from an Apogee sensor and write the data to a csv file. 

Automatic collection is the default collection mode, which will turn the sensor's logging on and then automatically collect all available data and record it in a csv file. The frequency with which the Raspberry Pi will "wake up" and check for available data from all sensors can be adjusted through the `config` function.

If a manual collection mode is needed, set the `manual` argument to `True`. The first time this function is used for a sensor, the sensor's logging will be turned on with the included interval, start/end time, etc.  Then, use the `collect` function again with `manual=True` to collect available data from the sensor and add it to the csv file (when collecting data, the `file` argument can be included to store the data in a different file than what was originally set but `interval`, `start`, and `end` will be ignored).


*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    await apogee.collect(address="D7:52:21:95:5C:6C", interval=10, file="~/Desktop/greenhouse-data.csv")
```

*Function Signature*

The values in the function signature are defaults used if the corresponding arguments are omitted.

```
async def collect(
    address,
    interval = 5,
    start = 0,
    end = 4294967295,
    file = '~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv',
    append = False,
    overwrite = False,
    manual = False
) -> None
# The values above are defaults used if the corresponding arguments are omitted 
```

*Arguments*

| Argument | Type | Default Value | Usage |
| -------- | ---- | ------------- | ----- |
| address  | str  | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF |
| interval | int  | 5 minutes | The interval that sensor will log data (must be a positive integer) |
| start    | int  | Now | Start time for data collection using epoch time (Unix timestamp in seconds) |
| end      | int  | Never | End time for data collection using epoch time (Unix timestamp in seconds) |
| file     | str  | ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv | File path to write data to CSV file. Will create folders and files if they don’t exist. |
| append   | bool | False | Set to True to automatically append to an existing data file. |
| overwrite | bool | False | Set to True to automatically overwrite an existing data file. |
| manual   | bool | False | Set to True for manual data collection mode. |


### *config*

*Usage*

Change or view the application settings. When no arguments are included with the function call, the `config` function will return a dictionary of the current configuration parameters.


*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    await apogee.config(precision=5, filepath="/usr/Documents/GreenhouseData")
    updated_config = await apogee.config()
    print(updated_config)
```

*Function Signature*

The values in the function signature are defaults used if the corresponding arguments are omitted.

```
async def config(
    precision = 2,
    filepath = '~/Apogee/apogee-connect-rpi/data/',
    temp = 'C',
    par_filtering = False,
    collection_frequency = 5,
    reset = False
) -> dict
```

*Arguments*

| Argument | Type | Default Value | Usage |
| -------- | ---- | ------------- | ----- |
| precision  | int  | 2 | Maximum number of decimal places for collected data. |
| filepath | str  | ~/Apogee/apogee-connect-rpi/data/ | The default folder to save collected data. Adjust to avoid needing to specify full filepath every time data collection is initiated. |
| temp | str  | C | Change preferred temperature units. Enter “C” for Celsius and “F” for Fahrenheit (without quotations). |
| par_filtering | bool  | False | Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. |
| collection_frequency | int  | 5 | Frequency in minutes to check for new data logs and add to .csv data file (This is different than the data logging interval for the sensor). Must be between 5 - 60 minutes. |
| reset | bool | False | Set to True to reset configuration back to default values. |

*Returns*

The function returns a dictionary where:

* *Key:* A string of the configuration parameter name
* *Value:* The current value of the configuration parameter


### *list*

*Usage*

Retreieve a dictionary of all the sensors currently collecting data.

*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    collecting_sensors = await apogee.list()
    print(collecting_sensors)
```

*Function Signature*

```
async def list() -> dict
```

*Returns*

The function returns a dictionary where:

* *Key:* The unique MAC address of the sensor
* *Value:* A dictionary containing sensor logging information (see table below)


| Sensor Info Key | Value |
| -------- | -------- | 
| interval  | int | 
| start_time  | int |
| end_time  | int | 
| logs  | int | 
| file  | str | 
| sensorID  | int | 
| collection_mode  | str | 
| last_collection_time  | int | 

### *scan*

*Usage*

Scan for nearby Apogee sensors and retrieve a dictionary with all discovered sensors.

*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    discovered_sensors = await apogee.scan(time=10)
    print(discovered_sensors)
```

*Function Signature*

The values in the function signature are defaults used if the corresponding arguments are omitted.

```
async def scan(
    time = 20
) -> dict
```

*Arguments*

| Argument | Type | Default Value | Usage |
| -------- | ----- | ------------- | ----- |
|time | int | 5-20 | Number of seconds to scan for Apogee Bluetooth sensors. If not set, scanning will continue until no new sensors are being discovered or a maximum of 20 seconds. |

*Returns*

The function returns a dictionary where:

* *Key:* The unique MAC address of the sensor
* *Value:* A custom Apogee Sensor class with attributes specific to the sensor (see table below)


| Sensor Attributes  | Value |
| -------- | -------- | 
| sensorID  | int |
| alias  | str | 
| serial  | str | 
| type  | str | 

### *stop*

*Usage*

Stop data collection from an Apogee sensor. Can optionally set the `all` argument to True to stop data collection from all Apogee sensors.

*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    await apogee.stop(address=D7:52:21:95:5C:6C, end=1726247820)
```

*Function Signature*

The values in the function signature are defaults used if the corresponding arguments are omitted.

```
async def stop(
    address,
    end = {current_time},
    all = False
)
```

*Arguments*

| Argument | Type | Default Value | Usage |
| -------- | ----- | ------------- | ----- |
| address | str | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF (Required unless the '--all' flag is used). |
| end | int | Now | End time for data collection using epoch time (Unix timestamp in seconds). Cannot be used when the 'all' argument is set to True. |
| all | bool | False | Stop data collection for all sensors (Can be used instead of the address requirement).|


### *transfer*

*Usage*

Transfer data from an Apogee sensor for a desired logging interval. This function is separate from the collect command and is just used to obtain a specific time period or previously logged data.

*Example*

```
from apogee_connect_rpi import ApogeeConnect

async def main():
    apogee = ApogeeConnect()
    await apogee.transfer(address="D7:52:21:95:5C:6C", start=1720647720, end=1726247820)
```

*Function Signature*

The values in the function signature are defaults used if the corresponding arguments are omitted.

```
async def transfer(
    address,
    start = 0,
    end = 4294967295,
    file = '~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv',
    append = False,
    overwrite = False
)
```

*Arguments*

| Argument | Type | Default Value | Usage |
| -------- | ----- | ------------- | ----- |
| address | str | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF. |
| start | int | Now | Start time for data collection using epoch time (Unix timestamp in seconds) |
| end | int | Never | End time for data collection using epoch time (Unix timestamp in seconds) |
| file | str | ~/Apogee/apogee_connect_rpi/data/<MAC_ADDRESS>.csv | File path to write data to csv file. Will create folders and files is they don’t exist. |
| append | bool | False | Set to True to automatically append data to a file if it exists instead of overwriting. |  
| overwrite | bool | False | Set to True to automatically overwrite an existing data file. |


## Contact

For more information or additional help, contact Apogee Instruments at: [techsupport@apogeeinstruments.com](mailto:techsupport@apogeeinstruments.com) or [+1(435)245-8012](tel:+14352458012)