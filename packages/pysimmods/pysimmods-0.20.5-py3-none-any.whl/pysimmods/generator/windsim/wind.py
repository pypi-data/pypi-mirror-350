"""This module contains a Wind turbine."""

import math
from copy import deepcopy

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ...model.generator import Generator
from ...util.air_density_at_height import (
    AIR_DENSITY_KG_PER_M3,
    barometric,
    ideal_gas,
)
from ...util.temperature_at_height import linear_gradient
from ...util.wind_at_height import hellman, logarithmic_profile
from .config import WindPowerPlantConfig
from .inputs import WindPowerPlantInputs
from .state import WindPowerPlantState


class WindPowerPlant(Generator):
    """Simulation model of a windturbine plant.

    The code for the corrections and power output is heavily inspired
    by the windpowerlib::

        https://github.com/wind-python/windpowerlib

    """

    def __init__(self, params, inits):
        self.config: WindPowerPlantConfig = WindPowerPlantConfig(params)
        self.state: WindPowerPlantState = WindPowerPlantState(inits)
        self.inputs: WindPowerPlantInputs = WindPowerPlantInputs()

    def step(self):
        """Perform a simulation step."""
        next_state = deepcopy(self.state)
        self._check_inputs(next_state)

        # First step: wind speed at hub height using hellmann or
        # logarithmic profile
        if self.config.wind_profile == "hellmann":
            next_state.wind_hub_v_m_per_s = hellman(
                self.inputs.wind_v_m_per_s,
                self.config.wind_height_m,
                self.config.hub_height_m,
            )

        elif self.config.wind_profile == "logarithmic":
            next_state.wind_hub_v_m_per_s = logarithmic_profile(
                self.inputs.wind_v_m_per_s,
                self.config.wind_height_m,
                self.config.hub_height_m,
            )

        # Second step: temperature at hub height using linear gradient
        # need T and P  at hub height
        if self.config.temperature_profile == "linear_gradient":
            next_state.t_air_hub_deg_kelvin = linear_gradient(
                self.inputs.t_air_deg_kelvin,
                self.config.temperature_height_m,
                self.config.hub_height_m,
            )
        else:
            next_state.t_air_hub_deg_kelvin = self.inputs.t_air_deg_kelvin

        # Third step: air density at hub height using temperature at
        # hub height. Two different profiles available: barometric or
        # ideal_gas

        if self.config.air_density_profile == "barometric":
            next_state.air_density_hub_kg_per_m3 = barometric(
                self.inputs.air_pressure_hpa,
                next_state.t_air_hub_deg_kelvin,
                self.config.pressure_height_m,
                self.config.hub_height_m,
            )
            wind_speed_corrected = self.wind_curve_correction(
                next_state.air_density_hub_kg_per_m3
            )

        elif self.config.air_density_profile == "ideal_gas":
            next_state.air_density_hub_kg_per_m3 = ideal_gas(
                self.inputs.air_pressure_hpa,
                next_state.t_air_hub_deg_kelvin,
                self.config.pressure_height_m,
                self.config.hub_height_m,
            )
            wind_speed_corrected = self.wind_curve_correction(
                next_state.air_density_hub_kg_per_m3
            )
        else:
            # No air density correction; use default value
            next_state.air_density_hub_kg_per_m3 = AIR_DENSITY_KG_PER_M3
            wind_speed_corrected = self.config.wind_speeds_m_per_s

        # Last step: power output with either power_curve or
        # power_coefficient method
        if self.config.method == "power_curve":
            next_state.p_kw = self.power_curve_output(
                next_state.wind_hub_v_m_per_s, wind_speed_corrected
            )
        elif self.config.method == "power_coefficient":
            next_state.p_kw = self.power_coefficient_output(
                next_state.air_density_hub_kg_per_m3,
                next_state.wind_hub_v_m_per_s,
            )

        self.state = next_state
        self.inputs.reset()

    def wind_curve_correction(
        self, density: float, density0: float = AIR_DENSITY_KG_PER_M3
    ):
        """Power curve at hub height

        Air density initial is set to the default value 1.225
        The correction is displayed in the new values of 
        power_curve_wind_speeds
        """
        interpolation = np.interp(
            self.config.wind_speeds_m_per_s, [7.5, 12.5], [1 / 3, 2 / 3]
        )
        power_curve_correction = (
            np.array(density0 / density).reshape(-1, 1) ** interpolation
        ) * self.config.wind_speeds_m_per_s

        return power_curve_correction[0]

    def power_curve_output(self, wind_speed, power_curve):
        """
        Calculation of the power curve value for a given wind speed by
        interpolation of power curve values dictionary.
        the only value required is the wind speed at hub  height
        wind_hub  = method(logarithmic_profile or hellmann profile)

        """

        power_output = np.interp(
            wind_speed, power_curve, self.config.power_curve_w, left=0, right=0
        )
        return power_output / 1000  # to kW

    def power_coefficient_output(self, air_density, wind_speed):
        """
        calculate the poweroutput using  power coffecient method
        method that requires the following parameters: rotor diameter,  density
        which means it offers more versatile parameters to play with
        """

        power_coefficient_inter = np.interp(
            wind_speed,
            self.config.wind_speeds_m_per_s,
            self.config.power_coefficient,
            left=0,
            right=0,
        )

        return (
            1
            / 8
            * air_density
            * self.config.rotor_diameter**2
            * np.pi
            * np.power(wind_speed, 3)
            * power_coefficient_inter
        ) / 1000  # to kW

    def _check_inputs(self, nstate):
        pass
