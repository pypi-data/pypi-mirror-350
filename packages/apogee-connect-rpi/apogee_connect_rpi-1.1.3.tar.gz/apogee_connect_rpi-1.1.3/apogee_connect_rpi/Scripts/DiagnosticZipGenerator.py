import zipfile
import subprocess
import os

from apogee_connect_rpi.Scripts.SensorManager import SensorManager

class DiagnosticZipGenerator:
    def __init__(self):
        self.sensorManager = SensorManager()

    def generate_zip_report(self, addresses):
        print("Compiling diagnostic information into zip file...")

        base_path = os.path.expanduser('~/Apogee/apogee_connect_rpi')
        logs_path = os.path.join(base_path, 'logs')
        reports_path = os.path.join(base_path, 'diagnostics')
        os.makedirs(reports_path, exist_ok=True)

        log_file = os.path.join(logs_path, 'ac_rpi_log.log')
        dmesg_file = os.path.join(reports_path, 'dmesg.txt')
        app_version_file = os.path.join(reports_path, 'app_version.txt')
        sensor_list_file = os.path.join(reports_path, 'sensor_list.txt')
        config_file = os.path.join(reports_path, 'config.txt')
        crontab_jobs_file = os.path.join(reports_path, 'crontab_jobs.txt')
        zip_filename = os.path.join(reports_path, 'diagnostic_report.zip')       
        
        files_to_zip = [
            log_file,
            dmesg_file,
            app_version_file,
            sensor_list_file,
            config_file,
            crontab_jobs_file
        ]

        self.create_file_from_command('dmesg', dmesg_file)
        self.create_file_from_command('apogee --version', app_version_file)
        self.create_file_from_command('apogee list', sensor_list_file)        
        self.create_file_from_command('apogee config', config_file)        
        self.create_file_from_command('crontab -l', crontab_jobs_file)

        if addresses:
            data_files = self.get_data_files_from_addresses(addresses)
            files_to_zip.extend(data_files)
        
        self.zip_all_files(zip_filename, files_to_zip)
        self.remove_extra_files(files_to_zip)
        
        print(f"Finished creating diagnostic zip file located at {zip_filename}. Please include in email to Apogee Instruments.")

    def create_file_from_command(self, command, file):
        try:
            split_command = command.split()
            result = subprocess.run(split_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            with open(file, 'w') as file:
                file.write(result.stdout)
                if result.stderr:
                    file.write("\nErrors:\n")
                    file.write(result.stderr)
        except Exception as e:
            raise RuntimeError(f"Error making {command} file: {e}")
    
    def get_data_files_from_addresses(self, addresses):
        try:
            files = []
            for address in addresses:
                file = self.sensorManager.get_sensor_file(address)
                if file:
                    files.append(file)
            
            return files
        
        except Exception as e:
            raise RuntimeError(f"Error getting data file for input address(es): {e}")
    
    def zip_all_files(self, zip_file, files):
        try:
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                for file in files:
                    if os.path.exists(file):
                        zipf.write(file, os.path.basename(file))
        except Exception as e:
            raise RuntimeError(f"Error making zip file: {e}")
    
    def remove_extra_files(self, files):
        for file_path in files:
            try:
                os.remove(file_path)
            except Exception as e: 
                continue        