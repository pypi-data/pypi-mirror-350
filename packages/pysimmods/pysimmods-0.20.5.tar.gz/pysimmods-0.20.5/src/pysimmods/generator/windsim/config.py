"""This module contains the config model for the Wind plant."""

import numpy as np

from ...model.config import ModelConfig


class WindPowerPlantConfig(ModelConfig):
    """Config parameters of Wind plant model.

    Parameters
    ----------

    params : dict
        Contains the configuration of the turbine. See attribute
        section for more information about the parameters, attributes
        marked with *(Input)* can or must be provided.

    Attributes
    ----------

    wind_speed_height:
    roughness_length:
    obstacle_height:
    air_density:
        represent the default value
    nominal_power:
    hub_height:
    rotor_diameter:
    turbine_type:
    pressure:
    temperature:
    temperature_height:
    pressure:

    """

    def __init__(self, params):
        super().__init__(params)

        self.p_max_kw = params.get("pn_max_kw", 2000)
        self.p_min_kw = 0
        self.turbine_type = params.get("turbine_type", "E-82/2000")
        self.hub_height_m = params.get("hub_height_m", 78)
        self.rotor_diameter_m = params.get("rotor_diameter_m", 82)
        self.roughness_length_m = params.get("roughness_length_m", 15)
        self.obstacle_height_m = params.get("obstacle_height_m", 0)

        self.wind_height_m = params.get("wind_height_m", 10)
        self.temperature_height_m = params.get("temperature_height_m", 10)
        self.pressure_height_m = params.get("pressure_height_m", 10)
        # self.air_density = params.get("air_density", 1.225)
        # self.nominal_power = params.get("nominal_power", 10e6)

        # self.pressure = params.get("pressure", 98405.7)
        # self.temperature = params.get("temperature", 268)

        self.method = params.get("method", "power_curve")

        self.temperature_profile = params.get(
            "temperature_profile", "linear_gradient"
        )
        if self.temperature_profile != "linear_gradient":
            self.temperature_profile = "no_profile"

        # self.pressure_profile = params.get(
        #     "pressure_profile", "atmospheric_pressure"
        # )

        self.wind_profile = params.get("wind_profile", "hellmann")

        self.air_density_profile = params.get(
            "air_density_profile", "barometric"
        )
        self.power_curve_w = np.array(
            params.get("power_curve_m", [0, 26, 180, 1500, 3000, 3000])
        )

        self.power_coefficient = np.array(
            params.get(
                "power_coefficient", [0.301, 0.36, 0.39, 0.409, 0.421, 0.429]
            )
        )

        self.wind_speeds_m_per_s = np.array(params.get("wind_speeds", []))
        if self.wind_speeds_m_per_s.size == 0:
            if self.method == "power_curve":
                num_vals = len(self.power_curve_w)
            else:
                num_vals = len(self.power_coefficient)

            self.wind_speeds_m_per_s = np.linspace(0.0, 25.0, num_vals)

        # power_curve_wind_speed = params.get(
        #     "power_curve_wind_speeds", [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
        # )

        # self.power_curve = pd.DataFrame(
        #     data={
        #         "value": power_curve_values,
        #         "wind_speed": power_curve_wind_speed,
        #     }
        # )
        # power_coefficient_wind_speed = params.get(
        #     "power_coefficient_curve_wind_speeds",
        #     [4.0, 4.5, 5.0, 5.5, 6.0, 6.5],
        # )
        # power_coefficient_curve_value = params.get(
        #     "power_coefficient_curve_values",
        #     [0.301, 0.36, 0.39, 0.409, 0.421, 0.429],
        # )
        # power_coefficient_dict = {
        #     "value": power_coefficient_curve_value,
        #     "wind_speed": power_coefficient_wind_speed,
        # }
        # self.power_coefficient = pd.DataFrame(power_coefficient_dict)

        # self.p_min_kw = 0
        # self.p_max_kw = power_curve_wind_speed[-1]
        # self.default_p_schedule = None
        # self.default_q_schedule = None
