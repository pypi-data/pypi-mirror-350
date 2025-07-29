import os
import json
import subprocess

class ErrorHandling:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(script_dir)
        self.file = os.path.join(parent_dir, 'Helpers/ErrorTracking.json')
        self.reset_script = os.path.join(parent_dir, 'Helpers/reset_bluetooth.sh')

    def read_error_data(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as file:
                return json.load(file)
        else:
            return {"bluetooth": {"max_failures": 5, "successive_failures": 0}}

    def increment_failure_count(self):
        data = self.read_error_data()
        bluetooth_data = data.get("bluetooth", {})
    
        # Increment the failure count
        bluetooth_data['successive_failures'] += 1
        print(f"Successive Bluetooth failure count is now {bluetooth_data['successive_failures']}")        

        # Check if the failure count exceeds the max_failures
        if bluetooth_data['successive_failures'] >= bluetooth_data.get('max_failures', 5):
            print("Maximum failures reached. Running reset script...")
            self.run_reset_script()
            bluetooth_data['successive_failures'] = 0 
        
        # Write updated data back to the file
        data['bluetooth'] = bluetooth_data
        self.save_file(data)

    def reset_failure_count(self):
        data = self.read_error_data()
        bluetooth_data = data.get("bluetooth", {})
        bluetooth_data['successive_failures'] = 0
        
        # Write updated data back to the file
        data['bluetooth'] = bluetooth_data
        self.save_file(data)

    def save_file(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def run_reset_script(self):
        try:
            subprocess.run(['sudo', 'bash', self.reset_script], check=True)
            print("Reset script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running reset script: {e}")