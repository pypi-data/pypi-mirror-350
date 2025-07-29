import bleak
import asyncio

from apogee_connect_rpi.Scripts.SensorClasses import *

class BleScanner:
    def __init__(self, scan_time: int, run_until_no_missing_packets: bool):
        self._scanner = bleak.BleakScanner(detection_callback=self.detectionCallback)
        self._discovered_sensors = {}
        self._scan_time = scan_time
        self._run_until_no_missing_packets = run_until_no_missing_packets

        self._scanning = asyncio.Event()
        self._loop = asyncio.get_event_loop()

    #
    # SCAN MANAGEMENT
    #
    async def startScan(self):
        try:
            print("Scanning", end="", flush=True)

            await self._scanner.start()
            self._scanning.set()
            endTime = self._loop.time() + self._scan_time

            # Set a max time for used only when scanning until all packets are found
            maxTime = self._loop.time() + 20

            # Check every second while scanner is still running
            while self._scanning.is_set():
                # Still less than endTime
                if (self._loop.time() <= endTime):
                    print(".",end="", flush=True)
                    await asyncio.sleep(1.0)
                    continue
                
                # Check if scanning until no discovered sensors are missing packets
                if self._run_until_no_missing_packets and self.missing_packets() and (self._loop.time() <= maxTime):
                    print(".",end="", flush=True)
                    await asyncio.sleep(1.0)
                    continue

                self._scanning.clear()

        except bleak.exc.BleakDBusError as e:
            print(f"Error occurred: {e}")
            print("Please try again:")

        finally:
            await self.stopScan()
            return self.show_discovered_sensors()

    async def stopScan(self):
        await self._scanner.stop()

    def missing_packets(self):
        for sensor in self._discovered_sensors.values():
            if (sensor.alias == "") or (sensor.serial == 0) or (sensor.type == ""):
                return True
        
        # None of the discovered sensors are missing packets
        return False

    #
    # HANDLE ADVERTISING DATA PACKET
    #
    def detectionCallback(self, sensor, advertisement_data):
        # Filter for Apogee's manufacturer ID: 1604
        if 1604 in advertisement_data.manufacturer_data:
            self.add_discovered_sensor(sensor, advertisement_data.manufacturer_data[1604])
        
    def add_discovered_sensor(self, sensor, manufacturer_data):
        address = sensor.address

        if address not in self._discovered_sensors:
            self._discovered_sensors[address] = ApogeeSensor(address)

        self.populate_discovered_sensor_info(address, manufacturer_data)

    def populate_discovered_sensor_info(self, address, manufacturer_data):
        sensor = self._discovered_sensors[address]
        
        # Check which manufacturer data packet was received
        if(self.is_alias_data(manufacturer_data)):
            sensor.alias = manufacturer_data.decode('utf-8')
        else:
            sensorID = int(manufacturer_data[-1])
            serial = int.from_bytes(manufacturer_data[:2], byteorder='little')
            sensor.serial = serial

            # Change sensor class to match sensorID if this is first time getting sensorID info (Just to get the sensor type really without needing to repeat code)
            if sensor.sensorID == 0:
                updated_sensor = get_sensor_class_from_ID(sensorID, address)
                updated_sensor.alias = sensor.alias
                updated_sensor.serial = sensor.serial
                self._discovered_sensors[address] = updated_sensor

    
    #
    # HELPERS
    #
    def is_alias_data(self, bytes):
        # Check if the first byte in within the printable ASCII range
        if not(32 <= bytes[0] <= 126):
            return False
        return True

    def show_discovered_sensors(self):
        if self._discovered_sensors:
            print("\n*Discovered Apogee Bluetooth Sensors*")

            # Print the header row
            headers = ["Address", "Alias", "S/N", "Type"]
            print("{:<17} | {:<20} | {:<4} | {:<8}".format(*headers))

            # Print the separator
            print(f'-' * 18 + '+' + '-' * 22 + '+' + '-' * 6 + '+' + '-' * 8)
            
            # Print the data rows
            for address, sensor in self._discovered_sensors.items():
                print("{:<17} | {:<20} | {:<4} | {:<8}".format(
                    address,
                    sensor.alias,
                    sensor.serial,
                    sensor.type
                ))

        else:
            print("\nNo Apogee Bluetooth Sensors Discovered")
        
        return self._discovered_sensors