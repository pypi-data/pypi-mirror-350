import math

import numpy as np
import pandas as pd

M_AIR_KG_PER_MOL: float = 0.029
ACCELERATION_GRAVITY_M_PER_S2: float = 9.81
GAS_CONSTANT_J_PER_MOL_K: float = 8.314
GAS_CONSTANT_J_PER_KG_K: float = 287.058
T_0_DEGREE_KELVIN: float = 288.15
P_0_HPA: float = 1013.25
P_GRADIENT_HPA_PER_M: float = 1 / 8
AIR_DENSITY_KG_PER_M3: float = 1.225


# # Calculate the pressure at altitude h using the barometric formula
# def atmospheric_pressure(
#     h, P0=1013.25, h0=0
# ):  # P0=1013.25   Standard sea level pressure (Pa)
#     # M = 0.029  # Molar mass of air in kg/mol
#     # g = 9.81  # Acceleration due to gravity in m/s^2
#     # R = 8.314  # Universal gas constant in J/(mol·K)
#     # T0 = 288.15  # Standard temperature at sea level in K

#     # Calculate the temperature at altitude h using the standard lapse rate
#     lapse_rate = -0.0065  # K/m
#     T = T0 + lapse_rate * h

#     # Calculate atmospheric pressure using the barometric formula
#     P = P0 * math.exp(-M * g * (h - h0) / (R * T))

#     return P


def barometric(
    pressure_hpa: float,
    temperature_at_height: float,
    data_height: float,
    target_height: float,
):
    """
    the barometric height equation to calculate the air density at hub
    height using pressure and Temperature at hub height.
    R is the specific gas constant for dry air (around
    287.05 J/(kg·K)).
    Pressure gradient of -1/8 hPa/m   ASSUMPTION
        1.225   # rho
        pressure:  Air pressure in Pa.
        pressure_height : Height in m for which the parameter `pressure`
            applies. the  same for  temperature_height
        pressure_height: hub height of wind turbine in m.
        temperature_hub_height : Air temperature at hub height in K
    """

    #

    # pressure_height = temperature_height
    # pressure = self.atmospheric_pressure(
    #      pressure
    # )
    # pressure_height = self.atmospheric_pressure(hub_height )
    #   temperature_hub_height = self.linear_gradient(
    #      temperature, self.config.temperature_height, self.config.hub_height
    #  )

    return (
        pressure_correction(pressure_hpa, data_height, target_height)
        * AIR_DENSITY_KG_PER_M3
        * T_0_DEGREE_KELVIN
        / (P_0_HPA * temperature_at_height)
    )


def ideal_gas(
    pressure_hpa: float,
    temperature_at_height: float,
    data_height: float,
    target_height: float,
):
    """
    The barometric height equation to calculate the air density at hub
    height using pressure and Temperature at hub height
    gas constant of dry air (287.058 J/(kg*K))
    return air density at hub height
    """
    #
    # pressure_height = self.config.temperature_height
    # temperature_hub_height = self.linear_gradient(temperature)

    return (
        pressure_correction(pressure_hpa, data_height, target_height)
        / (GAS_CONSTANT_J_PER_KG_K * temperature_at_height)
        * 100
    )


def pressure_correction(
    pressure_hpa: float, data_height: float, target_height: float
):
    return pressure_hpa - (target_height - data_height) * P_GRADIENT_HPA_PER_M
