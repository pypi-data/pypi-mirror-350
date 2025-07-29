#!/usr/bin/env python3

import asyncio
import argparse
import sys
import re
import requests
import os
from packaging import version
from filelock import FileLock, Timeout
from textwrap import dedent
from apogee_connect_rpi.Scripts.CommandImplement import CommandImplement
from apogee_connect_rpi.Scripts.ErrorHandling import ErrorHandling
from apogee_connect_rpi.version import __version__

class ApogeeConnect:
    def __init__(self):
        self.commandImplement = CommandImplement()
        self.lock_path = os.path.join('/tmp','apogee_connect_rpi.lock')

        # Map command name to function name for CLI-usage
        self.COMMAND_MAP = {
            'collect': 'collect',
            'config': 'config',
            'list': 'list',
            'scan': 'scan',
            'stop': 'stop',
            'transfer': 'transfer',
            
            'diagnostics': 'diagnostics',
            'run-data-collection': 'run_data_collection'
        }

    async def _dispatch_cli_command(self, parser, command, *args):
        func_name = self.COMMAND_MAP.get(command)
        if func_name and hasattr(self, func_name):
            method = getattr(self, func_name)
            try:
                await asyncio.wait_for(method(*args), timeout=290)
            except asyncio.TimeoutError:
                # If something causes a timeout error, it's likely the Bluetooth on the device freezing up. Make sure everything is reset for next iteration at least
                ErrorHandling().run_reset_script()
                self._release_lock_file()
                raise RuntimeError(f"Command '{command}' timed out. Resetting Bluetooth and releasing lock file.")
            except SystemExit as e:
                # This exception is hit when using `--help` flag with a command. This helps it exit smoothly and quietly
                return
            except Exception as e:
                print(e)
        else:
            parser.print_help()
            raise ValueError('\nUnrecognized command. For additional information see the available commands and documentation listed above')
    
    async def _check_for_updates(self):
        try: 
            response = requests.get(f"https://pypi.org/pypi/apogee-connect-rpi/json")
            response.raise_for_status()
            latest_version = response.json()['info']['version']

            if version.parse(latest_version) > version.parse(__version__):
                print(f"\n[notice]: A new release of apogee-connect-rpi is available: {__version__} -> {latest_version}")
                print(f"[notice]: To update, run: 'pipx upgrade apogee-connect-rpi' or 'pip install apogee-connect-rpi --upgrade', depending on initial install method.")

        except Exception as e:
            return

    #
    # COMMANDS
    #   
    async def collect(self, *args, **kwargs) -> False:
        """
        Collects data from an Apogee sensor and writes it to a CSV file.

        kwargs:
        address (str): MAC address of the sensor in the format AA:BB:CC:DD:EE:FF. This is a required argument.
        interval (int): The interval (in minutes) at which the sensor will log data. Must be a positive integer. Default is 5 minutes.
        start (int): Start time for data collection using epoch time (Unix timestamp in seconds). Default is 0 (immediate start).
        end (int): End time for data collection using epoch time (Unix timestamp in seconds). Default is 4294967295 (no end time).
        file (str): Path to the file where data will be written. The path will be expanded, and folders/files will be created if they don't exist. Default is '~/Apogee/apogee_connect_rpi/data/{address}.csv'.
        manual (bool): If True, enables manual data collection mode. Default is False.
        """
        try:
            if args:
                parser = argparse.ArgumentParser(description='Collect data from an Apogee sensor via bluetooth')
                parser.add_argument('address', type=self._mac_address,
                                    help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
                parser.add_argument('-i', '--interval', metavar='INTERVAL', type=self._positive_int, default=5,
                                    help="Collect data every INTERVAL minutes (must be a positive integer)")
                parser.add_argument('-s', '--start', metavar='START', type=self._positive_int,
                                    help="Start time for data collection using epoch time (Unix timestamp in seconds)")
                parser.add_argument('-e', '--end', metavar='END', type=self._positive_int,
                                    help="End time for data collection using epoch time (Unix timestamp in seconds)")
                parser.add_argument('-f', '--file', metavar='FILE', type=str,
                                    help="Filepath to write data to csv file")
                parser.add_argument('-a', '--append', 
                                    help="Automatically append to an existing file.")
                parser.add_argument('-o', '--overwrite', 
                                    help="Automatically overwrite existing file and bypass prompt.")
                parser.add_argument('-m', '--manual', 
                                    help="Manually collect data from sensor or initiate collection in manual collection mode")
                
                parsed_args = parser.parse_args(args)
                # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value
                
            address = kwargs.get('address', None)        
            interval = kwargs.get('interval', 5)
            start = kwargs.get('start', None)
            end = kwargs.get('end', None)
            file = kwargs.get('file', None)
            append = kwargs.get('append', None)
            auto_overwrite = kwargs.get('overwrite', False)
            manual_collection = kwargs.get('manual', False)

            if not address:
                raise ValueError("Error: The 'address' argument is required")

            if append and auto_overwrite:
                raise ValueError("'append' and 'overwrite' cannot both be used")

            if manual_collection:
                return await self.commandImplement.collect_manual(address, interval, start, end, file, append, auto_overwrite)
            else:
                return await self.commandImplement.collect_auto(address, interval, start, end, file, append, auto_overwrite)

        except Exception as e:
            print(e)

    async def config(self, *args, **kwargs) -> dict:
        """
        Change or view the application settings. When no arguments are provided, this function returns a dictionary of the current configuration parameters.

        kwargs:
        precision (int): Maximum number of decimal places for collected data. Default is 2.
        filepath (str): The default folder to save collected data. Adjust to avoid specifying the full filepath every time data collection is initiated. Default is '~/Apogee/apogee-connect-rpi/data/'.
        temp (str): Preferred temperature units. Enter 'C' for Celsius or 'F' for Fahrenheit. Default is 'C'.
        par_filtering (bool): Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. Default is False.
        collection_frequency (int): Frequency in minutes to check for new data logs and add to the CSV data file. Must be between 5 and 60 minutes. Default is 5.
        reset (bool): Set to True to reset configuration back to default values. Default is False.

        Returns:
        dict: A dictionary where:
                * Key: String representing the configuration parameter name
                * Value: The current value of the corresponding parameter.
        """
        try:
            if args:
                parser = argparse.ArgumentParser(description='Collect data from an Apogee sensor via bluetooth at desired intervals')
                parser.add_argument('-p', '--precision', metavar='PRECISION', type=self._positive_int,
                                    help="Change the maximum number of decimals displayed for data")
                parser.add_argument('-f', '--filepath', metavar='FILEPATH', type=str,
                                    help="The default folder to save collected data.")
                parser.add_argument('-t', '--temp', metavar='TEMP', type=self._valid_temp,
                                    help="Change preferred temperature units. Enter “C” for Celsius and “F” for Fahrenheit (without quotations).")
                parser.add_argument('-pf', '--par-filtering', metavar='PAR_FILTERING', type=self._adaptable_bool,
                                    help='Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. Enter "True" or "False" (without quotations)')
                parser.add_argument('-cf', '--collection-frequency', metavar='COLLECTION_FREQUENCY', type=self._positive_int,
                                    help='Frequency in minutes to check for new data logs (This is different than the data logging interval for the sensor). Must be between 5 - 60 minutes.')
                parser.add_argument('-r', '--reset', action='store_true',
                                    help='Reset config back to defaults')
                
                parsed_args = parser.parse_args(args)
                    # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value
            
            config_args = {
                'precision': kwargs.get('precision', None),
                'filepath': kwargs.get('filepath', None),
                'temp': kwargs.get('temp', None),
                'par_filtering': kwargs.get('par_filtering', None),
                'collection_frequency': kwargs.get('collection_frequency', None),
                'reset': kwargs.get('reset', None)
            }

            if isinstance(config_args['collection_frequency'], int) and (config_args['collection_frequency'] < 5 or config_args['collection_frequency'] > 60):
                    raise ValueError("Collection frequency must be 5 - 60 minutes")

            config = await self.commandImplement.config(config_args)
            return config # Returns empty dict if config was only updated rather than retrieved
        
        except Exception as e:
            print(e)

    async def list(self, *args, **kwargs) -> dict:
        """
        Retrieve a dictionary of all sensors currently collecting data.

        This function returns information about sensors that are actively collecting data, including their collection parameters and statuses.

        Returns:
        dict: A dictionary where:
            - *Key:* The unique MAC address of the sensor (str).
            - *Value:* A dictionary containing sensor logging information with the following keys:
                - 'interval' (int): The interval (in minutes) at which the sensor logs data.
                - 'start_time' (int): The start time for data collection (epoch time in seconds).
                - 'end_time' (int): The end time for data collection (epoch time in seconds).
                - 'logs' (int): The number of logs collected.
                - 'file' (str): The file path where data is saved.
                - 'sensorID' (int): A unique identifier for the sensor.
                - 'collection_mode' (str): The current collection mode (e.g., 'automatic' or 'manual').
                - 'last_collection_time' (int): The timestamp of the last data collection (epoch time in seconds).
        """

        try:
            if args:
                parser = argparse.ArgumentParser(description='Show list of Apogee bluetooth sensors that are currently collecting data')
                # Args not used now but keeping logic here for potential future expansion
            
                parsed_args = parser.parse_args(args)
                 # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value

            sensor_list = await self.commandImplement.list()
            return sensor_list
        
        except Exception as e:
            print(e)

    async def scan(self, *args, **kwargs) -> dict:
        """
        Scan for nearby Apogee sensors and retrieve a dictionary with all discovered sensors.

        kwargs:
        time (int): Number of seconds to scan for Apogee Bluetooth sensors. The default is 20 seconds. The scanning will continue for the specified time or until no new sensors are being discovered, whichever comes first. The acceptable range is 5 to 20 seconds.

        Returns:
            dict: A dictionary where:
                * Key: The unique MAC address of the sensor (str)
                * Value: An instance of the custom Apogee Sensor class with the following attributes:
                    - 'sensorID' (int): Unique identifier for the sensor 
                    - 'alias' (str): Alias name or label of the sensor
                    - 'serial' (str): Serial number of the sensor 
                    - 'type' (str): Type of the sensor (e.g., model) 
        """

        try:
            if args:
                parser = argparse.ArgumentParser(description='Scan for nearby Apogee bluetooth sensors')
                parser.add_argument('-t', '--time', metavar='TIME', type=self._positive_int,
                                help="Scan for TIME seconds")
                parsed_args = parser.parse_args(args)
                 # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value

            time = kwargs.get('time', None)
            discovered_sensors = await self.commandImplement.scan(time)
            return discovered_sensors
        
        except Exception as e:
            print(e)

    async def stop(self, *args, **kwargs):
        """
        Stop data collection from an Apogee sensor. Optionally, stop data collection from all sensors with the 'all' parameter.

        kwargs:
        address (str): MAC address of the sensor in the format of AA:BB:CC:DD:EE:FF. Required unless `all` is set to True.
        end (int): End time for data collection using epoch time (Unix timestamp in seconds). If not specified, data collection will stop immediately. This argument is ignored if `all` is True.
        all (bool): If True, stop data collection for all sensors. If False (the default), only stops collection for the sensor specified by `address`.
        """

        try:
            if args:
                parser = argparse.ArgumentParser(description='Stop data collection from an Apogee sensor via bluetooth')
                group = parser.add_mutually_exclusive_group(required=True)
                group.add_argument('address', type=self._mac_address, nargs='?',
                                help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
                group.add_argument('-a', '--all', action='store_true',
                                help='Stop data collection from all sensors')
                parser.add_argument('-e', '--end', metavar='END', type=self._positive_int,
                                    help="End time for data collection using epoch time (Unix timestamp in seconds)")
                
                parsed_args = parser.parse_args(args)
                 # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value

            address = kwargs.get('address', None)        
            all = kwargs.get('all', None)
            end = kwargs.get('end', None)

            if not address and not all:
                raise ValueError("Error: The 'address' argument is required")
            
            if all and end:
                raise ValueError("End time cannot be set when also using 'all'")

            if all:
                await self.commandImplement.stop_all()
            else:
                await self.commandImplement.stop(address, end)    

        except Exception as e:
            print(e)

    async def transfer(self, *args, **kwargs) -> bool:
        """
        Transfer data from an Apogee sensor for a specified interval.

        kwargs:
        address (str): MAC address of the sensor in the format of AA:BB:CC:DD:EE:FF. This argument is required.
        start (int): Start time for data collection using epoch time (Unix timestamp in seconds). Defaults to 0, which typically means the earliest available data.
        end (int): End time for data collection using epoch time (Unix timestamp in seconds). Defaults to 4294967295, which typically means the latest available data.
        file (str): File path to write data to CSV file. The default path is `~/Apogee/apogee_connect_rpi/data/{address}.csv`, where `{address}` is replaced with the sensor's MAC address. This path will create folders and files if they do not exist.
        append (bool): If True, append data to the file if it exists. If False (the default), the file will be overwritten.
        """

        try:
            if args:
                parser = argparse.ArgumentParser(description='Transfer data from an Apogee sensor via bluetooth for a given time period')
                parser.add_argument('address', type=self._mac_address,
                                    help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
                parser.add_argument('-s', '--start', metavar='START', type=self._positive_int,
                                    help="Start time for data collection using epoch time (Unix timestamp in seconds)")
                parser.add_argument('-e', '--end', metavar='END', type=self._positive_int,
                                    help="End time for data collection using epoch time (Unix timestamp in seconds)")
                parser.add_argument('-f', '--file', metavar='FILE', type=str,
                                    help="Filepath to write data to csv file")
                parser.add_argument('-a', '--append', action='store_true',
                                    help='Append data to existing file')
                parser.add_argument('-o', '--overwrite', action='store_true',
                                help="Automatically overwrite existing file and bypass prompt.")
            
                parsed_args = parser.parse_args(args) 
                 # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value

            address = kwargs.get('address', None)
            start = kwargs.get('start', None)
            end = kwargs.get('end', None)
            file = kwargs.get('file', None)
            append = kwargs.get('append', False)
            auto_overwrite = kwargs.get('overwrite', False)

            print(kwargs)
            return
            if not address:
                raise ValueError("Error: The 'address' argument is required")

            if append and auto_overwrite:
                raise ValueError("'append' and 'overwrite' cannot both be used")
            
            collected_data = await self.commandImplement.transfer(address, start, end, file, append, auto_overwrite)    
            return collected_data
        
        except Exception as e:
            print(e)

    #
    # ADDITIONAL UNLISTED COMMANDS
    #
    # This will send log and other helpful diagnostic information to developers email
    async def diagnostics(self, *args, **kwargs):
        try:
            parser = argparse.ArgumentParser(description='Compile helpful diagnostic information in a zip file to send to Apogee Instruments')
            parser.add_argument('addresses', type=self._mac_address, nargs='*', help='List of MAC addresses to include data for in the report (can be none)')
            if args:
                parsed_args = parser.parse_args(args)
                 # Only update if value from CLI isn't None
                for key, value in vars(parsed_args).items():
                    if value is not None:
                        kwargs[key] = value
        
            addresses = kwargs.get('addresses', [])
            await self.commandImplement.diagnostics(addresses)

        except Exception as e:
            print(e)

    # This function is only intended to be run by crontab command on a schedule
    async def run_data_collection(self):
        try:
            # Avoid duplicate data collection processes from running
            with FileLock(self.lock_path).acquire(timeout=10):
                await self.commandImplement.run_data_collection()
        except Timeout as e:
            print(f"\n{e}")
            print(f"The previous data collection process is still running. Skipping this instance.")
        except Exception as e:
            print(f"\n{e}")
        finally:
            self._release_lock_file()

    #
    # HELPERS
    #         
    def _release_lock_file(self):
        if os.path.exists(self.lock_path):
            try:
                os.remove(self.lock_path)
            except Exception as e:
                print(f"Failed to remove lock file: {e}")
                
    #
    # CUSTOM DATA TYPES
    #   
    def _positive_int(self, value):
        try:
            value_int = int(value)
            if value_int <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
            return value_int
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

    def _mac_address(self, value):
        pattern = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
        if not pattern.match(value):
            raise argparse.ArgumentTypeError(f"{value} is not a valid MAC address. Format must follow XX:XX:XX:XX:XX:XX")
        
        formatted_value = value.replace('-',':').upper()
        return formatted_value
    
    def _valid_temp(self, value):
        if value.upper() not in ['C', 'F']:
            raise argparse.ArgumentTypeError(f"Invalid temperature unit '{value}'. Must be 'C' or 'F'.")
        return value.upper()
    
    def _adaptable_bool(self, value):
        if value.lower() in ('true', '1', 't'):
            return True
        elif value.lower() in ('false', '0', 'f'):
            return False
        else:
            raise argparse.ArgumentTypeError(f"Boolean value expected (true/false), got '{value}'.")

#
# MAIN
#  
def cli():
    parser = argparse.ArgumentParser(
            description='Apogee Connect for Raspberry Pi',
            usage=dedent('''
                Interact with Apogee bluetooth sensors for automatic data collection
                         
                Available Commands:
                collect    Collect data from a sensor
                config     Change or read app configuration
                list       Show a list of currently collecting sensors
                scan       Scan for nearby sensors
                stop       Stop data collection for a sensor
                transfer   Transfer data from the sensor for given period
                         
                For documentation, see: https://pypi.org/project/apogee-connect-rpi/
                For information about Apogee Instruments, see: https://www.apogeeinstruments.com/
            '''))
        
    parser.add_argument('command', help='Any command from the above list may be used')
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version number of application')
    args = parser.parse_args(sys.argv[1:2])

    apogee = ApogeeConnect()
    try:
        asyncio.run(apogee._dispatch_cli_command(parser, args.command, *sys.argv[2:]))
    except Exception as e:
        print(e)
    
    asyncio.run(apogee._check_for_updates())

if __name__ == '__main__':
    cli()
