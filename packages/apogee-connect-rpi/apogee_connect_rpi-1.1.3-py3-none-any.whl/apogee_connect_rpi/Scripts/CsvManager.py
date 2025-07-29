import os
import csv
import datetime
from dateutil import parser

from apogee_connect_rpi.Scripts.liveDataTypes import liveDataTypes
from apogee_connect_rpi.Scripts.AppConfig import AppConfig

class CsvManager:
    def __init__(self):
        self.config = AppConfig()
        self.date_format = '%a %b %d %H:%M:%S %Y' # Mon Sep 16 14:11:28 2024 
        self.delimiter = ';'
        self.encoding = 'utf-8'
    
    def write_to_csv(self, timestamp, live_data, sensor, file):
        expanded_filepath = os.path.expanduser(file)
        directory = os.path.dirname(expanded_filepath)
        os.makedirs(directory, exist_ok=True)        
        
        file_exists = os.path.isfile(file)
        if not file_exists:
            self.create_csv(sensor, file)

        precision = self.get_precision()

        datetime = self.convert_timestamp_dattime(timestamp)
        truncated_values = [datetime] + [self.truncate_float(value, precision) for value in live_data]
        with open(file, 'a', newline='', encoding=self.encoding) as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            writer.writerow(truncated_values)
            csvfile.flush()
    
    def create_csv(self, sensor, file, appending=False, auto_overwrite=False):
        expanded_filepath = os.path.expanduser(file)
        directory = os.path.dirname(expanded_filepath)
        os.makedirs(directory, exist_ok=True)

        file_exists = os.path.isfile(file)
        if file_exists and appending:
            print("Appending data to existing file")
            return
        
        if file_exists and not appending and not auto_overwrite:
            overwrite = input(f"\nThe file '{file}' already exists. Do you want to overwrite it? [Y/N]: ")
            if overwrite.lower() != 'y':
                raise RuntimeError("File not overwritten. Exiting command.")
            else:
                print("Overwriting file")
            
        labels_with_units = ["Timestamp"] + [self.format_label_with_units(label) for label in sensor.live_data_labels]
        with open(file, 'w', newline='', encoding=self.encoding) as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            writer.writerow(labels_with_units)
            csvfile.flush()
   
    def get_valid_file(self, file, address):        
        # Default case
        if not file:
            path = AppConfig().get_default_filepath()
            return os.path.join(path, "{}.csv".format(address.replace(':', '-')))
        
        # Expand ~ and normalize path format
        file = os.path.expanduser(os.path.normpath(file))

        # If file is provided, it must be a csv file
        if not file.endswith('.csv'):
            raise ValueError("The 'file' parameter must have a '.csv' extension")

        # Just a file name and no filepath
        if not os.path.dirname(file):
            path = AppConfig().get_default_filepath()
            return os.path.join(path, f"{file}")

        # Check for relative filepath vs absolute filepath
        if os.path.isabs(file):
            return file
        else:
            return os.path.join(os.getcwd(), file)
    
    #
    # HANDLING CORRUPTED FILE
    #
    def check_csv_data_corruption(self, file) -> bool:
        # Most likely scenario of data corruption is power loss while writing to file
        try:
            file_exists = os.path.isfile(file)
            if file_exists:
                with open(file, 'rb') as f:
                    content = f.read()
                    if b'\x00' in content:
                        print("File data corruption detected")
                        return True
                    else:
                        return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return True
    
    def clean_corrupted_csv_file(self, file):
        print("Cleaning corrupted file")

        temp_file = file + '.temp'
        try:
            with open(file, 'r', encoding=self.encoding, errors='ignore') as infile:
                with open(temp_file, 'w', encoding=self.encoding) as outfile:
                    while True:
                        chunk = infile.read(1024 * 1024)  # Read in 1 MB chunks in case of large files
                        if not chunk:
                            break
                        
                        null_index = chunk.find('\x00')
                        if null_index != -1:
                            outfile.write(chunk[:null_index])
                            break
                        else:
                            outfile.write(chunk)
            
            # Replace the original file with the cleaned file
            os.replace(temp_file, file)
            print(f"Cleaned file saved and replaced")
        
        except Exception as e:
            print(f"Error processing file: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)  # Clean up temporary file in case of error
        
    #
    # HELPERS
    #     
    def get_last_timestamp(self, file):
        print("Retrieving last timestamp in file")
        try:
            with open(file, 'rb') as file:
                # Go to end of file and search backwards for beginning of last row
                file.seek(-2, os.SEEK_END)  
                while file.read(1) != b'\n': 
                    file.seek(-2, os.SEEK_CUR)
                
                # Decode the last row and get just the date (first element)
                last_row_bytes = file.readline()  
                last_row = last_row_bytes.decode(self.encoding).strip()  
                date = last_row.split(self.delimiter)[0] 

            # Convert date to epoch timestamp
            dt = parser.parse(date)
            return int(dt.timestamp())

        except Exception as e:
            print(f"Error getting last timestamp: {e}")
            return None
        
    def format_label_with_units(self, label):
        if label in liveDataTypes:
            units = liveDataTypes[label]["units"]
            return f"{label} ({units})"
        else:
            return label
    
    def truncate_float(self, value, precision=2):
        return f"{value:.{precision}f}"
    
    def convert_timestamp_dattime(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime(self.date_format)
    
    def get_precision(self):
        return self.config.get_precision()