import numpy as np
from apogee_connect_rpi.Scripts.AppConfig import AppConfig

def par_calculator(par: float) -> float:
    filtering = AppConfig().get_par_filtering()

    if (par < 0) and (filtering):
        return 0.0
    else: 
        return par

def temp_calculator(tempC: float) -> float:
    if(AppConfig().get_temp_units() == "F"):
        return ((tempC * 9/5) + 32)
    else:
        return tempC

def dew_point_calculator(humidity: float, tempC: float) -> float:
    saturation = saturation_vapor_pressure_calculator(tempC)
    vapor_pressure = (humidity / 100.0) * saturation
    log_term = (vapor_pressure / 0.61121)
    log = np.log(log_term).item()
    dew_point =  (257.14 * log) / (18.678 - log)

    if(AppConfig().get_temp_units() == "F"):
        return float((dew_point * 9/5) + 32)
    else:
        return float(dew_point)

def vpd_calculator(humidity: float, tempC: float) -> float:
    saturation = saturation_vapor_pressure_calculator(tempC)
    vapor_pressure = (humidity / 100.0) * saturation
    vpd = saturation - vapor_pressure

    return vpd

def saturation_vapor_pressure_calculator(tempC: float) -> float:
    exponent = ((18.678 - (tempC / 234.5)) * tempC) / (257.14 + tempC)
    return float(0.6121 * np.exp(exponent))

def uv_pfd_calculator(uv_efd: float) -> float:
    return uv_efd * 3.0

def uvb_efd_calculator(uvi: float) -> float:
    return -0.0037 * uvi ** 2 + 0.21 * uvi + 0.0

def uvb_pfd_calculator(uvi: float) -> float:
    uvb_efd = uvb_efd_calculator(uvi)
    return uvb_efd * 2.6

def approx_ndvi_calculator(red: float, nir: float) -> float:
    return ((1.35 * nir) - red) / ((1.35 * nir) + red)

def reflectance_calculator(radiance: float, irradiance: float) -> float:
    return radiance / irradiance

def pair_ndvi_calculator(red_reflectance: float, nir_reflectance: float) -> float:
    return (nir_reflectance - red_reflectance) / (nir_reflectance + red_reflectance)

def red_farRed_ratio_calculator(red: float, far_red: float) -> float:
    return red / far_red

def percent_red_farRed_calculator(red: float, far_red: float) -> float:
    return (far_red / (red + far_red) * 100)

def percent_par_farRed_calculator(par: float, far_red: float) -> float:
    return (far_red / (par + far_red) * 100)

def total_pfd_calculator(par: float, far_red: float) -> float:
    return par + far_red

def albedo_calculator(upward: float, downward: float) -> float:
    return downward / upward
