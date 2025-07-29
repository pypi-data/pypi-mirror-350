import json
import os
import shutil 

class AppConfig:    
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        script_parent_dir = os.path.dirname(script_dir)
        self.default_config_file  = os.path.join(script_parent_dir, 'Helpers', 'DefaultConfig.json')
        
        home_dir = os.path.expanduser("~")
        parent_dir = os.path.join(home_dir, ".local", "share", "apogee_connect_rpi")
        self.config_file = os.path.join(parent_dir, 'AppConfig.json')
        
        # This is temporary for a transition but can be deleted after the next iteration
        secondary_dir = os.path.join(home_dir, "Apogee", "apogee_connect_rpi", ".local")
        self.secondary_file = os.path.join(secondary_dir, 'AppConfig.json')

        if not os.path.exists(self.config_file):
            # Copy from the previous location to the new storage location (temporary and can be deleted in next iteration)
            if os.path.exists(self.secondary_file):
                os.makedirs(parent_dir, exist_ok=True)
                shutil.copy2(self.secondary_file, self.config_file)
            else:
                self.create_file(self.config_file)
    
    def create_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if os.path.exists(self.default_config_file):
            with open(self.default_config_file, 'r') as src_file:
                    config_data = json.load(src_file)
                
            with open(filename, 'w') as dest_file:
                json.dump(config_data, dest_file, indent=4)
        else:
            with open(filename, 'w') as file:
                json.dump({}, file)

    def _load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
            
        except FileNotFoundError:
            print(f"Config file not found. Using default config")
            self.create_file(self.config_file)
            return{}

    def _save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
            print("Config updated")
    
    def reset_config(self):
        self.create_file(self.config_file)

    def print_config(self):
        config = self._load_config()
        print(json.dumps(config, indent=4))
        return config

    def update_config(self, config_args):
        config = self._load_config()

        if config_args.get('precision') is not None:
            self._set_precision(config, config_args.get('precision'))
        
        if config_args.get('temp') is not None:
            self._set_temp_units(config, config_args.get('temp'))

        if config_args.get('par_filtering') is not None:
            self._set_par_filtering(config, config_args.get('par_filtering'))

        if config_args.get('filepath') is not None:
            self._set_default_filepath(config, config_args.get('filepath'))
        
        if config_args.get('collection_frequency') is not None:
            self._set_collection_frequency(config, config_args.get('collection_frequency'))
        
        self._save_config(config)
            
    #
    # PRECISION
    #
    def get_precision(self):
        config = self._load_config()
        return config.get('precision', 2)

    def _set_precision(self, config, precision: int):
        print("Updating precision")
        config['precision'] = precision

    #
    # UNITS
    #
    def get_temp_units(self):
        config = self._load_config()
        return config.get('units', {}).get('temperature')

    def _set_temp_units(self, config, unit):
        print("Updating temperature units")
        if unit not in ["C", "F"]:
            raise ValueError("Unit must be 'C' (Celsius) or 'F' (Fahrenheit)")

        if 'units' not in config:
            config['units'] = {}
        config['units']['temperature'] = unit

    #
    # PAR FILTERING
    #
    def get_par_filtering(self):
        config = self._load_config()
        return config.get('par_filter', False)
    
    def _set_par_filtering(self, config, enabled: bool):
        print("Updating PAR filtering")
        config['par_filter'] = enabled
    
    #
    # COLLECTION_FREQUENCY
    #
    def get_collection_frequency(self):
        config = self._load_config()
        return config.get('collection_frequency', 5)

    def _set_collection_frequency(self, config, frequency: int):
        print("Updating collection frequency")
        config['collection_frequency'] = frequency
    
    #
    # FILEPATH
    #
    def get_default_filepath(self):
        config = self._load_config()
        if 'default_path' in config:
            return config['default_path']
        
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Apogee", "apogee_connect_rpi", "data")

    def _set_default_filepath(self, config, path: str):
        print("Updating default filepath")
        filepath = self.validate_filepath(path)
        if not filepath:
            raise ValueError("Invalid filepath")

        config['default_path'] = filepath
    
    def validate_filepath(self, filepath):
        # Ensure just filepath is provided, not a filename as well
        if not filepath or os.path.basename(filepath):
            return None
        
        filepath = os.path.normpath(filepath)        

        # Check absolute vs relative filepath
        if os.path.isabs(filepath):
            return filepath
        else:
            return os.path.join(os.getcwd(), filepath)