import json
import os
import shutil

# Class to assist with storing which sensors are currently collecting data
class SensorManager:
    def __init__(self):
        home_dir = os.path.expanduser("~")
        parent_dir = os.path.join(home_dir, ".local", "share", "apogee_connect_rpi")
        self.storage_file = os.path.join(parent_dir, 'CollectingSensors.json')
        
        # This is temporary for a transition but can be deleted after the next iteration
        secondary_dir = os.path.join(home_dir, "Apogee", "apogee_connect_rpi", ".local")
        self.secondary_file = os.path.join(secondary_dir, 'CollectingSensors.json')
        
        if not os.path.exists(self.storage_file):
            # Copy from the previous location to the new storage location (temporary and can be deleted in next iteration)
            if os.path.exists(self.secondary_file):
                os.makedirs(parent_dir, exist_ok=True)
                shutil.copy2(self.secondary_file, self.storage_file)
            else:
                self.create_file(self.storage_file)

    def create_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump({}, file)

    def _load_sensor_list(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data
        else:
            return {}

    def _save_sensor_list(self, sensor_list):
        with open(self.storage_file, 'w') as f:
            json.dump(sensor_list, f, indent=4)

    def add_sensor(self, address: str, interval: int, start_time: int, end_time: int, filename: str, sensorID: int, collection_mode: str):    
        sensor_list = self._load_sensor_list()
        if address not in sensor_list:
            info = {
                "interval": interval,
                "start_time": start_time,
                "end_time": end_time if end_time is not None else "None", 
                "logs": 0,
                "file": filename,
                "sensorID": sensorID,
                "collection_mode": collection_mode,
                "last_collection_time": start_time # Set to start_time so future start sensors don't attempt data collection until then
            }

            sensor_list[address] = info
            self._save_sensor_list(sensor_list)

    def remove_sensor(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            del sensor_list[address]
            self._save_sensor_list(sensor_list)

    #
    # GETTERS
    #
    def get_sensor_info(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            return sensor_list[address]
        
    def get_all_sensor_addresses(self):
        sensor_list = self._load_sensor_list()
        return list(sensor_list.keys())

    def get_sensor_file(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            return sensor_list[address]['file']
    
    def get_sensor_id(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            return sensor_list[address]['sensorID']
    
    def get_sensor_collection_mode(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            return sensor_list[address]['collection_mode']
    
    def get_auto_collecting_sensor_list_length(self):
        sensor_list = self._load_sensor_list()
        auto_sensor_count = sum(1 for info in sensor_list.values() if info['collection_mode'] == 'Auto')
        return auto_sensor_count
    
    #
    # SETTERS
    #
    def update_end_time(self, address, end_time):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            print("Updating data collection end time")
            sensor_list[address]['end_time'] = end_time
            self._save_sensor_list(sensor_list)
        else:
            print("Sensor not found in list")
    
    def update_last_collection_time(self, address, time):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            print("Updating last data collection time")
            sensor_list[address]['last_collection_time'] = time
            self._save_sensor_list(sensor_list)

    def increment_collected_logs(self, address):
        sensor_list = self._load_sensor_list()
        if address in sensor_list:
            sensor_list[address]['logs'] += 1
            self._save_sensor_list(sensor_list)

    # OTHER
    def sensor_already_collecting(self, address):
        sensor_list = self._load_sensor_list()
        return address in sensor_list
    
    def compile_sensors_for_auto_collection(self, current_time):
        sensor_list = self._load_sensor_list()
        sensor_queue = [
            {
                "address": address,
                "end_time": details['end_time'] if isinstance(details['end_time'], int) else 4294967295, # Make sure end_time isn't "None" so we can compare against it. 4294967295 = 0xFFFFFFFF
                "file": details['file'],
                "sensorID": details['sensorID'],
                "interval": details['interval'],
                "last_collection_time": details['last_collection_time']
            }
            for address, details in sensor_list.items()
            if (details['sensorID'] >= 29 and details['sensorID'] <= 34 and details['collection_mode'] != "Manual") and (current_time >= (details['last_collection_time'] + (details['interval'] * 60) - 2)) # Minus 2 seconds to provide leeway for if script starts slightly quicker
        ]
        return sensor_queue
      
    def print_collecting_sensor_list(self):
        sensor_list = self._load_sensor_list()
        if not sensor_list:
            print("No sensors are currently collecting data")
        else:    
            print("\n*Currently Collecting Sensors*")
            
            # Print the header row
            headers = ["Address", "Logs", "Interval", "Start Time", "End Time", "Mode", "File"]
            print("{:^17} | {:^6} | {:^8} | {:^10} | {:^10} | {:^6} | {:^5}".format(*headers))

            # Print the row separator
            print('-' * 18 + '+' + '-' * 8 + '+' + '-' * 10 + '+' + '-' * 12 + '+' + '-' * 12 + '+' + '-' * 8 + '+' + '-' * 6)
            
            # Print the data rows
            for address, details in sensor_list.items():
                print("{:<17} | {:<6} | {:<8} | {:<10} | {:<10} | {:^6} | {:<5}".format(
                    address, 
                    details['logs'], 
                    details['interval'], 
                    details['start_time'], 
                    details['end_time'], 
                    details['collection_mode'], 
                    details['file']
                ))
        
        return sensor_list