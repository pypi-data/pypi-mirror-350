from apogee_connect_rpi.Scripts.Calculators import *

class ApogeeSensor():
    def __init__(self, address: str):
        self.address = address
        self.sensorID = 0
        self.alias = ""
        self.serial = ""
        self.model = ""
        self.type = ""
        self.live_data_labels = []

    def calculate_live_data(self, data):
        return data

    def setSensorID(self, modelNo: int):
        self.sensorID = modelNo
        self.populateSensorInfo(modelNo)
    
    def compatible_firmware(self, hw: int, fw: int):
        if (hw == 0 and fw >= 3) or (hw == 5 and fw >= 9) or (hw == 6 and fw >= 9):
            return True
        else:
            return False

class SP_110(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 1
        self.model = "SP-110"
        self.type = "Pyranometer"
        self.live_data_labels = ["Shortwave"]

    def calculate_live_data(self, data):
        return data

class SP_510(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 2
        self.model = "SP-510"
        self.type = "Thermopile Pyranometer"
        self.live_data_labels = ["Shortwave"]
        
    def calculate_live_data(self, data):
        return data

class SP_610(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 3
        self.model = "SP-610"
        self.type = "Thermopile Pyranometer (Downward)"
        self.live_data_labels = ["Shortwave"]
        
    def calculate_live_data(self, data):
        return data

class SQ_110(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 4
        self.model = "SQ-110"
        self.type = "Quantum (Solar)"
        self.live_data_labels = ["PPFD"]
        
    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        return live_data
    
class SQ_120(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 5
        self.model = "SQ-120"
        self.type = "Quantum (Electric)"
        self.live_data_labels = ["PPFD"]
        
    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        return live_data
    
class SQ_500(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 6
        self.model = "SQ-500"
        self.type = "Quantum (Full Spectrum)"
        self.live_data_labels = ["PPFD"]
        
    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        return live_data

class SL_510(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 7
        self.model = "SL-510"
        self.type = "Pyrgeometer"
        self.live_data_labels = ["Longwave", "Temperature"]
        
    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        temp = temp_calculator(live_data[1])
        live_data[1] = temp
        return live_data
    
class SL_610(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 8
        self.model = "SL-610"
        self.type = "Pyrgeometer (Downward)"
        self.live_data_labels = ["Longwave", "Temperature"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        temp = temp_calculator(live_data[1])
        live_data[1] = temp

        return live_data


class SI_1XX(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 9
        self.model = "SI-1XX"
        self.type = "IR Sensor"
        self.live_data_labels = ["Target Temp", "Sensor Temp"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        target_temp = temp_calculator(live_data[0])
        sensor_temp = temp_calculator(live_data[1])

        live_data = [target_temp, sensor_temp]
        return live_data

class SU_200(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 10
        self.model = "SU-200"
        self.type = "UV Sensor"
        self.live_data_labels = ["UV_EFD", "UV_PFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        uv_pfd = uv_pfd_calculator(live_data[0])
        live_data.append(uv_pfd)

        return live_data

class SE_100(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 11
        self.model = "SE-100"
        self.type = "Photometric"
        self.live_data_labels = ["Illuminance"]

    def calculate_live_data(self, data):
        return data

class S2_111(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 12
        self.model = "S2-111"
        self.type = "NDVI"
        self.live_data_labels = ["red", "NIR"]

    def calculate_live_data(self, data):
        return data

class S2_112(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 13
        self.model = "S2-112"
        self.type = "NDVI (Downward)"
        self.live_data_labels = ["red", "NIR", "NDVI"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        ndvi = approx_ndvi_calculator(live_data[0], live_data[1])
        live_data.append(ndvi)

        return live_data

class S2_121(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 14
        self.model = "S2-121"
        self.type = "PRI"
        self.live_data_labels = ["green", "yellow"]

    def calculate_live_data(self, data):
        return data

class S2_122(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 15
        self.model = "S2-122"
        self.type = "PRI (Downward)"
        self.live_data_labels = ["green", "yellow"]

    def calculate_live_data(self, data):
        return data

class S2_131(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 16
        self.model = "S2-131"
        self.type = "Red/FarRed"
        self.live_data_labels = ["red", "far_red", "red_farRed_ratio", "percent_red_farRed"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        red_farRed_ratio = red_farRed_ratio_calculator(live_data[0], live_data[1])
        percent_red_farRed = percent_red_farRed_calculator(live_data[0], live_data[1])

        live_data.append(red_farRed_ratio)
        live_data.append(percent_red_farRed)

        return live_data

class S2_141(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 17
        self.model = "S2-141"
        self.type = "PAR/FAR"
        self.live_data_labels = ["PAR", "far_red", "percent_par_farRed", "Total PFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        par = par_calculator(live_data[0])
        percent_par_farRed = percent_par_farRed_calculator(live_data[0], live_data[1])
        total_pfd = total_pfd_calculator(live_data[0], live_data[1])
        
        live_data[0] = par
        live_data.append(percent_par_farRed)
        live_data.append(total_pfd)
        
        return live_data

class SQ_610(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 18
        self.model = "SQ-610"
        self.type = "ePAR"
        self.live_data_labels = ["ePPFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        
        return live_data

class ST_XX0(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 19
        self.model = "ST-XX0"
        self.type = "Thermistor"
        self.live_data_labels = ["Temperature"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        temp = temp_calculator(live_data[0])
        live_data = [temp]

        return live_data

class SP_700(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 20
        self.model = "SP-700"
        self.type = "Albedometer"
        self.live_data_labels = ["Upward", "Downward", "Albedo"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 2):
            return live_data
        
        albedo = albedo_calculator(live_data[0], live_data[1])
        live_data.append(albedo)

        return live_data

class SQ_620(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 21
        self.model = "SQ-620"
        self.type = "Quantum (Extended Range)"
        self.live_data_labels = ["PFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par

        return live_data

class SQ_640(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 22
        self.model = "SQ-640"
        self.type = "Quantum (Low-Light)"
        self.live_data_labels = ["PFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        
        return live_data

class NDVI_Pair(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 23
        self.model = "NDVI Pair"
        self.type = "Pair NDVI"
        self.live_data_labels = ["red", "NIR"]

    def calculate_live_data(self, data):
        if (len(data) != 4):
            return data
        
        red_reflectance = reflectance_calculator(data[2], data[0])
        nir_reflectance = reflectance_calculator(data[3], data[1])
        ndvi = pair_ndvi_calculator(red_reflectance, nir_reflectance)

        live_data = [ndvi, red_reflectance, nir_reflectance]
        return live_data

class PRI_Pair(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 24
        self.model = "PRI Pair"
        self.type = "Pair PRI"
        self.live_data_labels = ["green", "yellow"]

    def calculate_live_data(self, data):
        return [data[0], data[1]]

class AY_002(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 25
        self.model = "Four Channel"
        self.type = "Four Channel"
        self.live_data_labels = ["ch1", "ch2", "ch3", "ch4"]

    def calculate_live_data(self, data):
        return data

class AY_001(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 26
        self.model = "Dual Channel"
        self.type = "Dual Channel"
        self.live_data_labels = ["ch1", "ch2"]

    def calculate_live_data(self, data):
        return data

class SQ_100X(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 27
        self.model = "SQ-100X"
        self.type = "Quantum"
        self.live_data_labels = ["PPFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        return live_data

class SQ_313(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 28
        self.model = "SQ-313"
        self.type = "Line Quantum"
        self.live_data_labels = ["PPFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        par = par_calculator(live_data[0])
        live_data[0] = par
        return live_data

class SM_500(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 29
        self.model = "SM-500"
        self.type = "Guardian"
        self.live_data_labels = ["PPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data

class SM_600(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 30
        self.model = "SM-600"
        self.type = "Guardian"
        self.live_data_labels = ["ePPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data

class SM1HUH(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 31
        self.model = "SM1HUH"
        self.type = "Guardian"
        self.live_data_labels = ["PPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data
    
class SM2HUH(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 32
        self.model = "SM2HUH"
        self.type = "Guardian"
        self.live_data_labels = ["PPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data

class SM3HUH(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 33
        self.model = "SM3HUH"
        self.type = "Guardian"
        self.live_data_labels = ["PPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data
    
class SM4HUH(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 34
        self.model = "SM4HUH"
        self.type = "Guardian"
        self.live_data_labels = ["PPFD", "Temperature", "Humidity", "CO2", "Pressure", "Dew Point", "VPD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 5):
            return live_data
        
        par = par_calculator(live_data[0])
        temp = temp_calculator(live_data[1])
        dew_point = dew_point_calculator(live_data[2], live_data[1])
        vpd = vpd_calculator(live_data[2], live_data[1])

        live_data[0] = par
        live_data[1] = temp
        live_data.append(dew_point)
        live_data.append(vpd)
        
        return live_data

class SO_100(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 35
        self.model = "SO-100"
        self.type = "Oxygen Sensor"
        self.live_data_labels = ["Oxygen"]

    def calculate_live_data(self, data):
        live_data = [data[0]]
        return live_data

class SO_200(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 36
        self.model = "SO-200"
        self.type = "Oxygen Sensor"
        self.live_data_labels = ["Oxygen"]

    def calculate_live_data(self, data):
        live_data = [data[0]]
        return live_data

class SU_300(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 37
        self.model = "SU-300"
        self.type = "UV Index"
        self.live_data_labels = ["UV_Index", "UBV_EFD", "UVB_PFD"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        uvb_efd = uvb_efd_calculator(live_data[0])
        uvb_pfd = uvb_pfd_calculator(live_data[0])

        live_data.append(uvb_efd)
        live_data.append(uvb_pfd)

        return live_data

class SF_110(ApogeeSensor):
    def __init__(self, address: str):
        super().__init__(address)
        self.sensorID = 38
        self.model = "SF-110"
        self.type = "Radiation Frost"
        self.live_data_labels = ["Temperature"]

    def calculate_live_data(self, data):
        live_data = data
        if (len(live_data) != 1):
            return live_data
        
        temp = temp_calculator(live_data[0])
        
        live_data = [temp]
        
        return live_data
    

# Helper Function
def get_sensor_class_from_ID(sensorID, address) -> ApogeeSensor:
        match sensorID:
            case 1:
                return SP_110(address)
            case 2:
                return SP_510(address)
            case 3:
                return SP_610(address)
            case 4:
                return SQ_110(address)
            case 5:
                return SQ_120(address)
            case 6:
                return SQ_500(address)
            case 7:
                return SL_510(address)
            case 8:
                return SL_610(address)
            case 9:
                return SI_1XX(address)
            case 10:
                return SU_200(address)
            case 11:
                return SE_100(address)
            case 12:
                return S2_111(address)
            case 13:
                return S2_112(address)
            case 14:
                return S2_121(address)
            case 15:
                return S2_122(address)
            case 16:
                return S2_131(address)
            case 17:
                return S2_141(address)
            case 18:
                return SQ_610(address)
            case 19:
                return ST_XX0(address)
            case 20:
                return SP_700(address)
            case 21:
                return SQ_620(address)
            case 22:
                return SQ_640(address)
            case 23:
                return NDVI_Pair(address)
            case 24:
                return PRI_Pair(address)
            case 25:
                return AY_002(address)
            case 26:
                return AY_001(address)
            case 27:
                return SQ_100X(address)
            case 28:
                return SQ_313(address)
            case 29:
                return SM_500(address)
            case 30:
                return SM_600(address)
            case 31:
                return SM1HUH(address)
            case 32:
                return SM2HUH(address)
            case 33:
                return SM3HUH(address)
            case 34:
                return SM4HUH(address)
            case 35:
                return SO_100(address)
            case 36:
                return SO_200(address)
            case 37:
                return SU_300(address)
            case 38:
                return SF_110(address)
            case _:
                return ApogeeSensor(address)
