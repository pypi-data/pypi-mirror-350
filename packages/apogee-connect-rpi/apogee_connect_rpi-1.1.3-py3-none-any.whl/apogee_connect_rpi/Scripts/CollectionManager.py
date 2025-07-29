import bleak
import struct
import asyncio  
import datetime

from apogee_connect_rpi.Scripts.SensorClasses import *
from apogee_connect_rpi.Scripts.ApogeeUuids import *
from apogee_connect_rpi.Scripts.SensorManager import SensorManager
from apogee_connect_rpi.Scripts.CronManager import CronManager
from apogee_connect_rpi.Scripts.CsvManager import CsvManager
from apogee_connect_rpi.Scripts.ErrorHandling import ErrorHandling


class CollectionManager:
    def __init__(self, address: str, filename: str):
        self.sensorManager = SensorManager()
        self.cronManager = CronManager()
        self.csvManager = CsvManager()

        self.address = address
        self.filename = self.csvManager.get_valid_file(filename, address)
        self.sensor = None
        self.bleak_client = None 
        self.collection_finished = asyncio.Event()
        self.end_time = 4294967295 # Default to 0xFFFFFFFF

        self.collected_data = []
        self.manual_collection = False

    #
    # SENSOR CONNECTION
    #
    async def connect(self, retries=3, delay=0.5):
        if not self.bleak_client:
            for attempt in range(retries):
                try:
                    print(f"Connecting to sensor {self.address}")
                    self.bleak_client = bleak.BleakClient(self.address)
                    await self.bleak_client.connect()
                    if self.bleak_client.is_connected:
                        ErrorHandling().reset_failure_count()
                        return
                except Exception as e:
                    print(f"Connection attempt {attempt + 1} failed to {self.address}: {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        if not self.manual_collection: # Only increment for restarting bluetooth if not collecting manually
                            ErrorHandling().increment_failure_count()
                        raise RuntimeError(f"Failed to connect to sensor {self.address}.")

    async def disconnect(self):
        if self.bleak_client:
            try:
                await self.bleak_client.disconnect()
                self.bleak_client = None
            
            except bleak.BleakError as e:
                raise RuntimeError(f"Could not disconnect from sensor {self.address}. {e}")

    #
    # COLLECTION SETUP
    #
    async def setup_collection(self, interval: int, start_time, end_time, appending=False, auto_overwrite=False, auto_collect=True):
        await self.connect()
        await self.populate_sensor_info()
        await self.check_sensor_time()
        await self.turn_on_gateway_mode()

        if self.sensor is None:
            print("Error retrieving sensor information")
            return
 
        try:           
            self.csvManager.create_csv(self.sensor, self.filename, appending, auto_overwrite)
 
            await self.set_last_timestamp_transferred(start_time)

            # Configure data logging settings and turn logging on 
            bytearray_data = self.get_logging_bytearray(interval, start_time, end_time)
            await self.initiate_logging(bytearray_data)

            if auto_collect:
                # Add sensor to list of currently collecting sensors
                self.sensorManager.add_sensor(self.sensor.address, interval, start_time, end_time, self.filename, self.sensor.sensorID, "Auto")
                await self.cronManager.setup_crontab_command_if_needed()         
                print(f"Data collection started. Data will be saved at {self.filename}.\nThis terminal may be closed.")
            else:
                # Add sensor to list of currently collecting sensors
                self.sensorManager.add_sensor(self.sensor.address, interval, start_time, end_time, self.filename, self.sensor.sensorID, "Manual")
                print(f"Sensor logging started in MANUAL collection mode.\nRun 'collect' command with 'manual' flag again to collect available data from sensor and add to {self.filename}.")
            
            return True
        except bleak.BleakError as e:
            print(f"Error retrieving sensor data: {e}")
        
        except RuntimeError as e:
            print(e)
        
        finally:
            await self.disconnect()

    async def set_last_timestamp_transferred(self, time):
        if not time:
            # Set last timestamp transferred to current time to avoid getting unwanted old data
            time = int(datetime.datetime.now().timestamp())

        await self.bleak_client.write_gatt_char(lastTransferredTimestampUUID, bytearray(struct.pack('<I', time)), True)

    def get_logging_bytearray(self, interval: int, start_time, end_time):
        SAMPLING_INTERVAL = 15 # Arbitrarily set to 15 seconds so there's some averaging of data logs
        logging_interval = interval * 60 # Convert to minutes
        data_array = [SAMPLING_INTERVAL, logging_interval]

        # Set start/end time
        data_array.append(start_time)
        if end_time:
            data_array.append(end_time)

        # Convert array to bytearray for gatt characteristic
        bytearray_data = bytearray()
        for num in data_array:
            bytearray_data.extend(struct.pack('<I', num)) 
        
        return bytearray_data                  

    async def check_sensor_time(self):
        data = await self.bleak_client.read_gatt_char(currentTimeUUID)
        data_packet = bytes(data)
        sensor_time = struct.unpack('<I', data_packet[:4])[0]

        current_time_epoch = int(datetime.datetime.now().timestamp())

        # Update time on sensor if more than a minute difference
        time_difference = abs(current_time_epoch - sensor_time)
        if time_difference > 60:
            print("Updating sensor real-time clock")
            await self.bleak_client.write_gatt_char(currentTimeUUID, bytearray(struct.pack('<I', current_time_epoch)), True)      

    async def initiate_logging(self, bytearray_data):
        # Start data logging
        print("Starting data collection...")
        await self.bleak_client.write_gatt_char(dataLoggingIntervalsUUID, bytearray_data, True)
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([1]), True)

    async def populate_sensor_info(self):
        await self.connect()

        try:
            print("Getting sensor info")
            sensorID_data = await self.bleak_client.read_gatt_char(sensorIDUUID)
            hw_data = await self.bleak_client.read_gatt_char(hardwareVersionUUID)
            fw_data = await self.bleak_client.read_gatt_char(firmwareVersionUUID)

            sensorID = int.from_bytes(sensorID_data, byteorder='little', signed=False)           
            hw = int(hw_data.decode('utf-8'))
            fw = int(fw_data.decode('utf-8'))

            self.sensor = get_sensor_class_from_ID(sensorID, self.address)

            if not self.sensor.compatible_firmware(int(hw), int(fw)):
                raise RuntimeError("Sensor firmware needs to be updated in order to be compatible with this application")
        
        except bleak.BleakError as e:
            raise RuntimeError(f"Error getting sensor info, {e}")

    async def turn_on_gateway_mode(self):
        await self.bleak_client.write_gatt_char(dataLogCollectionRateUUID, bytearray([1]), True)

    async def turn_off_gateway_mode(self):
        await self.bleak_client.write_gatt_char(dataLogCollectionRateUUID, bytearray([0]), True)

    #
    # DATA COLLECTION
    #                
    async def run_data_collection(self, sensorID: int, interval: int, end_time: int):
        await self.connect()
        self.sensor = get_sensor_class_from_ID(sensorID, self.address)
        await self.check_sensor_time()

        if isinstance(end_time, int):
            self.end_time = end_time

        try:
            corrupted_file = self.csvManager.check_csv_data_corruption(self.filename)
            if corrupted_file:
                await self.handle_corrupted_file()

            self.collected_data = [] # Clear this list before starting a new collection
            await self.bleak_client.start_notify(dataLogTransferUUID, self.process_data_packet)
            await asyncio.wait_for(self.collection_finished.wait(), timeout=30)
            await self.bleak_client.stop_notify(dataLogTransferUUID)

            # Go one extra interval past end_time just in case log was ready in time for last collect
            current_time_epoch = int(datetime.datetime.now().timestamp())
            if current_time_epoch > (end_time + interval * 60):
                print("Current time after end time")
                await self.stop_data_collection()

            self.sensorManager.update_last_collection_time(self.address, current_time_epoch)

            return self.collected_data
        except Exception as e:
            timestamp = self.csvManager.get_last_timestamp(self.filename)
            if timestamp:
                await self.set_last_timestamp_transferred(timestamp) # Set the last timestamp transferred in the event of an error during this process
            print(f"Sensor error: {self.address}. {e}")

        finally:
            await self.disconnect()

    async def process_data_packet(self, characteristic_uuid, data): 
        data_packet = bytes(data)
        hex_representation = data_packet.hex()
        print(f"Received data packet: {hex_representation}")

        # Check if data packet is incomplete or if it is just all "FF" indicating end of data
        if len(data_packet) < 8 or hex_representation == 'ffffffff':
            print("No more data to collect")
            self.collection_finished.set()
            return
              
        # Get packet header information
        timestamp = struct.unpack('<I', data_packet[:4])[0]
        intervalBetweenTimestamps = struct.unpack('<H', data_packet[4:6])[0]
        measurements_per_interval = struct.unpack('<B', data_packet[6:7])[0]
                
        data = []
        # This loop should usually only run once, but just in case a collection is missed and there are multiple sets in packet
        # Separate packet into groups based on timestamp (e.g., groups of 5 datapoints for the Guardian, groups of 1 datapoint for microcache)
        for startIndex in range(8, len(data_packet) - 1, 4 * measurements_per_interval):
            if timestamp > self.end_time:
                print("Current datalog timestamp after end time")
                self.collection_finished.set()
                return

            endIndex = min(startIndex + (4 * measurements_per_interval), len(data_packet))
            groupedArray = data_packet[startIndex:endIndex]

            # Get each datapoint within the current timestamp
            data = []
            for i in range(0, len(groupedArray), 4):
                raw = struct.unpack('<i', groupedArray[i:(i + 4)])[0]

                # Divide by 10,000 to scale from ten-thousandths to ones
                dataValue = raw / 10000.0

                data.append(dataValue)

            # Calculate all live data based on specific sensor class
            live_data = self.sensor.calculate_live_data(data)

            # Add data to list to be returned later
            self.add_data_to_list(timestamp, live_data, self.sensor)

            self.csvManager.write_to_csv(timestamp, live_data, self.sensor, self.filename)
            self.sensorManager.increment_collected_logs(self.address)

            # Increment timestamp in case there are multiple logs in a single packet
            timestamp += intervalBetweenTimestamps

    def add_data_to_list(self, timestamp, data, sensor: ApogeeSensor):

        dict_keys = sensor.live_data_labels

        data_dict = {}
        data_dict['timestamp'] = timestamp

        for i, value in enumerate(data):
            key = dict_keys[i] if i < len(dict_keys) else f"Unknown_{i}"
            data_dict[key] = value
        
        self.collected_data.append(data_dict)

    async def handle_corrupted_file(self):
        self.csvManager.clean_corrupted_csv_file(self.filename)
        timestamp = self.csvManager.get_last_timestamp(self.filename)
        if timestamp:
            await self.set_last_timestamp_transferred(timestamp) # Set to timestamp so we re-collect from there


    # 
    # STOP COLLECTION
    #
    async def stop_data_collection(self):
        await self.connect()
            
        print("Stopping Data Logging")
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([0]), True)

        print("Removing sensor from list")
        self.sensorManager.remove_sensor(self.address)

        if self.sensorManager.get_auto_collecting_sensor_list_length() <= 0:
            self.cronManager.remove_crontab_job()

        await self.turn_off_gateway_mode()

        await self.disconnect()
    
    #
    # DATA TRANSFER
    #
    async def data_transfer(self, start_time: int, end_time: int, appending: bool, auto_overwrite: bool):
        await self.connect()
        await self.populate_sensor_info()
        await self.check_sensor_time()

        if self.sensor is None:
            print("Error retrieving sensor information")
            return
    
        if isinstance(end_time, int):
            self.end_time = end_time

        try:
            self.csvManager.create_csv(self.sensor, self.filename, appending, auto_overwrite)
            await self.set_last_timestamp_transferred(start_time)

            print(f"Beginning data transfer to {self.filename}")
            await self.bleak_client.start_notify(dataLogTransferUUID, self.process_data_packet)
            await asyncio.wait_for(self.collection_finished.wait(), timeout=300)
            await self.bleak_client.stop_notify(dataLogTransferUUID)

            return self.collected_data
        except Exception as e:
            print(f"Sensor error: {self.address}. {e}")

        finally:
            await self.disconnect()