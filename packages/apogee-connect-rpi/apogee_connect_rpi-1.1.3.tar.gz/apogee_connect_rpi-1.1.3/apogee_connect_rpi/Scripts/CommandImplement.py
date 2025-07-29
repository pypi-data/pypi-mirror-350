import datetime

from apogee_connect_rpi.Scripts.BleScanner import BleScanner
from apogee_connect_rpi.Scripts.SensorManager import SensorManager
from apogee_connect_rpi.Scripts.CollectionManager import CollectionManager
from apogee_connect_rpi.Scripts.AppConfig import AppConfig
from apogee_connect_rpi.Scripts.CronManager import CronManager
from apogee_connect_rpi.Scripts.DiagnosticZipGenerator import DiagnosticZipGenerator

class CommandImplement:
    def __init__(self):
        self.sensorManager = SensorManager()

    # 
    # COLLECT
    #
    async def collect_auto(self, address, interval, start_time, end_time, file, append, auto_overwrite):

        if self.sensorManager.sensor_already_collecting(address):
            if self.sensorManager.get_sensor_collection_mode(address) == "Manual":
                raise RuntimeError("Sensor listed for MANUAL collection mode. Did you mean to add the '--manual' flag to the command? Otherwise, use the 'stop' command to stop data collection and then start with automatic collection mode.")
            else:
                raise RuntimeError("Sensor is already collecting data. Use the 'stop' command to stop data collection.")
        
        if self._max_sensors_reached():
            raise RuntimeError("\nMaximum number of sensors currently auto collecting data. Use 'list' command to see currently collecting sensors.")

        start, end = self._get_start_end_time(start_time, end_time)

        collectionManager = CollectionManager(address, file)
        collectionManager.manual_collection = False
        return await collectionManager.setup_collection(interval, start, end, append, auto_overwrite, auto_collect=True)

    async def collect_manual(self, address, interval, start_time, end_time, file, append, auto_overwrite):
        if not file:
            file = self.sensorManager.get_sensor_file(address)

        collectionManager = CollectionManager(address, file)
        collectionManager.manual_collection = True

        # If not already logging, start. If already in manual collection, collect data
        logging = self.sensorManager.sensor_already_collecting(address)
        if not logging:
            start, end = self._get_start_end_time(start_time, end_time)
            return await collectionManager.setup_collection(interval, start, end, append, auto_overwrite, auto_collect=False)

        else:
            if self.sensorManager.get_sensor_collection_mode(address) == "Auto":
                raise RuntimeError("Sensor listed for AUTO collection mode. Using the '--manual' flag may disrupt the automatic data collection. Use the 'stop' command to stop data collection and then start with manual collection mode.")
            
            sensor = self.sensorManager.get_sensor_info(address)
            sensorID = sensor['sensorID']
            interval = sensor['interval']
            end_time = sensor['end_time'] if isinstance(sensor['end_time'], int) else 4294967295 # Make sure end_time isn't "None" so we can compare against it. 4294967295 = 0xFFFFFFFF

            return await collectionManager.run_data_collection(sensorID, interval, end_time)
    
    def _max_sensors_reached(self) -> bool:
        MAX_SENSORS = 10
        current_sensor_length = self.sensorManager.get_auto_collecting_sensor_list_length()
        return current_sensor_length >= MAX_SENSORS
    
    def _get_start_end_time(self, start, end):
        current_time_epoch = int(datetime.datetime.now().timestamp())
        if not start:
            start = current_time_epoch
        if end:
            if (end <= start) or (end <= current_time_epoch):
                raise ValueError("End time must be after the start time and the current time")
            
        return start, end        

    # 
    # CONFIG
    #
    async def config(self, config_args) -> dict:
        config = AppConfig()
        
        # Check if no arguments included with command
        no_args = all(val is None for key, val in config_args.items() if key != 'reset')
        if no_args and not config_args.get('reset', False):
            return config.print_config()
        
        elif config_args.get('reset', False):
            reset = input(f"\nReset config back to defaults? [Y/N]: ")
            if reset.lower() != 'y':
                raise RuntimeError("Config not reset. Exiting command.")
            else:
                print("Resetting Config")
                config.reset_config()
                CronManager().update_cron_interval(config.get_collection_frequency())

        else:
            config.update_config(config_args)

            # Also update Crontab job 
            if config_args.get('collection_frequency') is not None:
                CronManager().update_cron_interval(config_args.get('collection_frequency'))

        return {}

    #
    # LIST
    #
    async def list(self) -> dict:
        sensor_list = self.sensorManager.print_collecting_sensor_list()
        return sensor_list

    #
    # SCAN
    #
    async def scan(self, scan_time) -> dict:
        scan_until_no_missing_packets = False

        # If no scan time was set, run at least 5 seconds until no discovered sensors are missing packets
        if not scan_time:
            scan_time = 5
            scan_until_no_missing_packets = True

        scanner = BleScanner(scan_time, scan_until_no_missing_packets)
        discovered_sensors = await scanner.startScan()
        return discovered_sensors

    #
    # STOP
    #
    async def stop(self, address, end_time):
        if end_time:
            self.sensorManager.update_end_time(address, end_time)
        else:
            collectionManager = CollectionManager(address, "")
            await collectionManager.stop_data_collection()
    
    async def stop_all(self):
        sensor_addresses = self.sensorManager.get_all_sensor_addresses()
        for address in sensor_addresses:
            try:
                collectionManager = CollectionManager(address, "")
                await collectionManager.stop_data_collection()
            except Exception as e:
                print(e)

    #
    # TRANSFER
    #
    async def transfer(self, address, start, end, file, append, auto_overwrite):
        if not start:
            start = 1
        if not end:
            end = 4294967295
        if end <= start:
            raise ValueError("End time must be after the start time")
    
        collectionManager = CollectionManager(address, file)
        collectionManager.manual_collection = True
        return await collectionManager.data_transfer(start, end, append, auto_overwrite) 

    #
    # CRONTAB DATA COLLECTION
    #
    async def run_data_collection(self):
        current_time = datetime.datetime.now()
        current_time_epoch = int(current_time.timestamp())
        sensors_queue = self.sensorManager.compile_sensors_for_auto_collection(current_time_epoch)

        print(f"\n{current_time}")
        print(f"Collecting from: {', '.join(sensor['address'] for sensor in sensors_queue)}")

        for sensor in sensors_queue:
            try:
                address = sensor['address']
                file = sensor['file']
                sensorID = sensor['sensorID']
                interval = sensor['interval']
                end_time = sensor['end_time']

                collectionManager = CollectionManager(address, file)
                return await collectionManager.run_data_collection(sensorID, interval, end_time)
            except Exception as e:
                print(e)
        
        print(f"Exiting scheduled data collection at {datetime.datetime.now()}")

    #
    # DIAGNOSTICS
    #
    async def diagnostics(self, addresses):
        DiagnosticZipGenerator().generate_zip_report(addresses)

            
            