"""This module contains multiple configuration examples for
wind_turbines with different nominal power.

"""

import csv
import logging
import os
import sys

import numpy as np
import pandas as pd

LOG = logging.getLogger(__name__)


def wind_power_plant_preset(
    pn_max_kw: float,
    wind_profile: str = "hellmann",
    temperature_profile: str = "linear_gradient",
    air_density_profile: str = "barometric",
    power_method: str = "power_curve",
    rng=None,
    turbine_type=None,
    force_type=False,
    **kwargs,
):  # need to add  an element for the type (p_curve  or  p_coff)
    """Return the parameter configuration for a turbine model
    from the
    .
    """
    # thismodule = sys.modules[__name__]
    # Accessing a function defined in the current module
    # num_gens = kwargs.get("num_gens", None)
    data = load_static_data()

    # correction = kwargs.get("correction", "power_curve")
    if wind_profile not in ["hellmann", "logarithmic"]:
        wind_profile = "hellmann"

    if temperature_profile not in ["linear_gradient", "no_profile"]:
        temperature_profile = "linear_gradient"

    if air_density_profile not in ["barometric", "ideal_gas", "no_profile"]:
        air_density_profile = "barometric"

    if power_method not in ["power_curve", "power_coefficient"]:
        power_method = "power_curve"

    params = {}
    if (
        turbine_type is not None
        and turbine_type in data
        and force_type
        and power_method == "power_curve"
    ):
        params = data[turbine_type]

    if not params:
        possible_pn = {}
        for ttype, values in data.items():
            possible_pn.setdefault(values["pn_max_kw"], [])
            if power_method == "power_curve" and values["has_power_curve"]:
                possible_pn[values["pn_max_kw"]].append(ttype)
            if (
                power_method == "power_coefficient"
                and values["has_power_coefficient"]
            ):
                possible_pn[values["pn_max_kw"]].append(ttype)
            # for key, value in values.items():
            #     if key == "pn_max_kw" and value == pn_max_kw:
            #         print(ttype)

        if pn_max_kw in possible_pn:
            if len(possible_pn[pn_max_kw]) == 1:
                params = data[possible_pn[pn_max_kw][0]]
            else:
                if (
                    turbine_type is not None
                    and turbine_type in possible_pn[pn_max_kw]
                ):
                    # for
                    params = data[turbine_type]
                elif rng is not None:
                    rnd = int(rng.random() * len(possible_pn[pn_max_kw]))
                    params = data[possible_pn[pn_max_kw][rnd]]
                else:
                    params = data[possible_pn[pn_max_kw][0]]
        else:
            p_lower = 0
            lower_diff = 0
            p_higher = 0
            higher_diff = 0
            for pn in possible_pn:
                if pn < pn_max_kw:
                    p_lower = pn
                    lower_diff = pn_max_kw - pn
                if pn > pn_max_kw:
                    p_higher = pn
                    higher_diff = pn - pn_max_kw
                    break
            if (
                lower_diff < higher_diff
                and p_lower in possible_pn
                or lower_diff > higher_diff
                and p_higher not in possible_pn
            ):
                params = data[possible_pn[p_lower][0]]

            else:
                params = data[possible_pn[p_higher][0]]
            params["pn_max_kw"] = pn_max_kw

    if power_method == "power_curve":
        params["power_curve_m"] = [
            v * 1000 * pn_max_kw for v in params["power_curve"]
        ]

    if rng is not None:
        h_min = params["height_min_m"]
        h_max = params["height_max_m"]
        rnd = h_min + int(rng.random() * (h_max - h_min))
        params["hub_height_m"] = rnd
    else:
        params["hub_height_m"] = params["height_min_m"]

    params["sign_convention"] = "active"
    params["method"] = power_method
    params["wind_profile"] = wind_profile
    params["temperature_profile"] = temperature_profile
    params["air_density_profile"] = air_density_profile
    return params, {}


def params_turbine_1T_15kw():
    """Params for a Turbuine type with 3 kw nominal power
    Nominal power  in W .
    """
    return {
        "rotor_diameter": 240,
        "hub_height": 150,
        "turbine_type": "IEA 15 MW offshore reference turbine",
        "temperature_height": 2,
        #   "power_coefficient_curve_wind_speeds": pd.Series([4.0, 5.0, 6.0]),
        #   "power_coefficient_curve_values": pd.Series([0.3, 0.4, 0.5]),
        #  "density": pd.Series(data=[1.3, 1.3, 1.3]),
        #  "density_correction": False,
        "power_curve_wind_speeds": pd.Series(
            [
                3.0,
                3.5,
                4.0,
                4.5,
                4.8,
                5.0,
                5.2,
                6.0,
                6.2,
                6.4,
                6.5,
                6.6,
                6.6,
                6.7,
                6.8,
                6.9,
                6.9,
                6.9,
                6.9,
                7.0,
                7.0,
                7.0,
                7.0,
                7.0,
                7.0,
                7.5,
                8.0,
                8.5,
                9.0,
                9.5,
                10.0,
                10.2,
                10.5,
                10.6,
                10.7,
                10.7,
                10.7,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.8,
                10.9,
                11.0,
                11.2,
                11.5,
                11.8,
                12.0,
                13.0,
                14.0,
                15.0,
                17.5,
                20.0,
                22.5,
                25.0,
            ]
        ),
        "power_curve_values": pd.Series(
            [
                70.0,
                302.0,
                595.1,
                964.9,
                1185.1,
                1429.2,
                1695.2,
                2656.3,
                2957.2,
                3275.7,
                3442.7,
                3528.6,
                3615.0,
                3791.2,
                3972.0,
                4155.6,
                4192.4,
                4210.8,
                4228.8,
                4247.2,
                4265.5,
                4283.9,
                4302.0,
                4320.3,
                4339.3,
                5338.8,
                6481.1,
                7774.6,
                9229.2,
                10855.0,
                12661.2,
                13638.2,
                14660.7,
                14994.8,
                14994.7,
                14994.6,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.5,
                14994.6,
                14994.5,
                14994.4,
                14994.3,
                14994.0,
                14994.1,
                14994.2,
                14994.2,
                14994.8,
                14994.8,
                14994.8,
                14994.8,
                14994.8,
                14996.3,
                14997.6,
            ]
        ),
        "wind_speed_height": 10,  # Height for which the parameter
        # `wind_speed` applies.
        "obstacle_height": 0,
        "air_density": 1.3,  # np.array([1.3, 1.3, 1.3]),
    }


def inits_turbine_1T_15kw():
    return {}


# power coffecient preset


# def params_turbine_n131_3kw():
#     """Params for a Turbuine type with 3 kw nominal power
#     Nominal power  in W .
#     """
#     return {
#         "rotor_diameter": 131,
#         "turbine_type": "N131/3000",
#         "nominal_power": 3e6,  # in W
#         "use_air_density_correction": True,
#         "power_coefficient_curve_wind_speeds": pd.Series(
#             [
#                 3.0,
#                 3.5,
#                 4.0,
#                 4.5,
#                 5.0,
#                 5.5,
#                 6.0,
#                 6.5,
#                 7.0,
#                 7.5,
#                 8.0,
#                 8.5,
#                 9.0,
#                 9.5,
#                 10.0,
#                 10.5,
#                 11.0,
#                 11.5,
#                 12.0,
#                 12.5,
#                 13.0,
#                 13.5,
#                 14.0,
#                 14.5,
#                 15.0,
#                 15.5,
#                 16.0,
#                 16.5,
#                 17.0,
#                 17.5,
#                 18.0,
#                 18.5,
#                 19.0,
#                 19.5,
#                 20.0,
#             ]
#         ),
#         "power_coefficient_curve_values": pd.Series(
#             [
#                 0.148,
#                 0.294,
#                 0.367,
#                 0.407,
#                 0.428,
#                 0.442,
#                 0.45,
#                 0.455,
#                 0.458,
#                 0.458,
#                 0.453,
#                 0.444,
#                 0.421,
#                 0.387,
#                 0.349,
#                 0.31,
#                 0.273,
#                 0.239,
#                 0.21,
#                 0.186,
#                 0.165,
#                 0.148,
#                 0.132,
#                 0.119,
#                 0.108,
#                 0.098,
#                 0.089,
#                 0.081,
#                 0.074,
#                 0.068,
#                 0.062,
#                 0.057,
#                 0.053,
#                 0.049,
#                 0.045,
#             ]
#         ),
#         "density": pd.Series(data=[1.3, 1.3, 1.3]),
#         # "density_correction": False,
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 3.0,
#                 3.5,
#                 4.0,
#                 4.5,
#                 5.0,
#                 5.5,
#                 6.0,
#                 6.5,
#                 7.0,
#                 7.5,
#                 8.0,
#                 8.5,
#                 9.0,
#                 9.5,
#                 10.0,
#                 10.5,
#                 11.0,
#                 11.5,
#                 12.0,
#                 12.5,
#                 13.0,
#                 13.5,
#                 14.0,
#                 14.5,
#                 15.0,
#                 15.5,
#                 16.0,
#                 16.5,
#                 17.0,
#                 17.5,
#                 18.0,
#                 18.5,
#                 19.0,
#                 19.5,
#                 20.0,
#             ]
#         ),
#         "power_curve_values": pd.Series(
#             [
#                 33.0,
#                 104.0,
#                 194.0,
#                 306.0,
#                 442.0,
#                 607.0,
#                 802.0,
#                 1032.0,
#                 1298.0,
#                 1595.0,
#                 1915.0,
#                 2250.0,
#                 2533.0,
#                 2740.0,
#                 2881.0,
#                 2965.0,
#                 2997.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#                 3000.0,
#             ]
#         ),
#         "wind_speed_height": 10,  # Height for which the parameter
#  `wind_speed` applies.
#         "obstacle_height": 0,
#         "air_density": 1.3,  # np.array([1.3, 1.3, 1.3]),
#     }


# def inits_turbine_2T_3kw():
#     return {}


# def params_turbine_ad116_5kw():
#     """Params for a Turbuine type with 3 kw nominal power
#     Nominal power  in W .
#     """
#     return {
#         "name": "M5000-116",
#         "nominal_power": 5000,
#         "power_curve_values": pd.Series(
#             [
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 50.0,
#                 165.0,
#                 280.0,
#                 410.0,
#                 540.0,
#                 705.0,
#                 870.0,
#                 1102.5,
#                 1335.0,
#                 1630.0,
#                 1925.0,
#                 2270.0,
#                 2615.0,
#                 3115.0,
#                 3615.0,
#                 4205.0,
#                 4795.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 5000.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#                 0.0,
#             ]
#         ),
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 0.0,
#                 0.5,
#                 1.0,
#                 1.5,
#                 2.0,
#                 2.5,
#                 3.0,
#                 3.5,
#                 4.0,
#                 4.5,
#                 5.0,
#                 5.5,
#                 6.0,
#                 6.5,
#                 7.0,
#                 7.5,
#                 8.0,
#                 8.5,
#                 9.0,
#                 9.5,
#                 10.0,
#                 10.5,
#                 11.0,
#                 11.5,
#                 12.0,
#                 12.5,
#                 13.0,
#                 13.5,
#                 14.0,
#                 14.5,
#                 15.0,
#                 15.5,
#                 16.0,
#                 16.5,
#                 17.0,
#                 17.5,
#                 18.0,
#                 18.5,
#                 19.0,
#                 19.5,
#                 20.0,
#                 20.5,
#                 21.0,
#                 21.5,
#                 22.0,
#                 22.5,
#                 23.0,
#                 23.5,
#                 24.0,
#                 24.5,
#                 25.0,
#                 25.5,
#                 26.0,
#                 26.5,
#                 27.0,
#                 27.5,
#                 28.0,
#                 28.5,
#                 29.0,
#                 29.5,
#                 30.0,
#             ]
#         ),
#         "rotor_diameter": 116,
#         "turbine_type": "AD116/5000",
#     }


# def params_turbine_v164_8kw2():
#     """Params for a Turbuine type with 3 kw nominal power
#     Nominal power  in W .
#     """
#     return {
#         "name": "V164-8.0 MW",
#         "nominal_power": 8000,
#         "power_curve_values": pd.Series(
#             [
#                 0.0,
#                 0.0,
#                 0.0,
#                 91.8,
#                 526.7,
#                 1123.1,
#                 2043.9,
#                 3134.6,
#                 4486.4,
#                 6393.2,
#                 7363.8,
#                 7834.4,
#                 8026.4,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#                 8077.2,
#             ]
#         ),
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 0.0,
#                 1.0,
#                 2.0,
#                 3.0,
#                 4.0,
#                 5.0,
#                 6.0,
#                 7.0,
#                 8.0,
#                 9.0,
#                 10.0,
#                 11.0,
#                 12.0,
#                 13.0,
#                 14.0,
#                 15.0,
#                 16.0,
#                 17.0,
#                 18.0,
#                 19.0,
#                 20.0,
#                 21.0,
#                 22.0,
#                 23.0,
#                 24.0,
#                 25.0,
#             ]
#         ),
#         "rotor_diameter": 164,
#         "turbine_type": "V164/8000",
#     }


# def params_turbine_scd168_8kw():
#     """Params for a Turbuine type with 3 kw nominal power
#     Nominal power  in W .
#     """
#     return {
#         "name": "SCD 168 8000",
#         "nominal_power": 8000,
#         "power_curve_values": pd.Series(
#             [
#                 0.0,
#                 0.0,
#                 0.0,
#                 100.0,
#                 500.0,
#                 1000.0,
#                 2000.0,
#                 3000.0,
#                 4000.0,
#                 5000.0,
#                 6000.0,
#                 7500.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#                 8000.0,
#             ]
#         ),
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 1.0,
#                 2.0,
#                 3.0,
#                 4.0,
#                 5.0,
#                 6.0,
#                 7.0,
#                 8.0,
#                 9.0,
#                 10.0,
#                 11.0,
#                 12.0,
#                 13.0,
#                 14.0,
#                 15.0,
#                 16.0,
#                 17.0,
#                 18.0,
#                 19.0,
#                 20.0,
#                 21.0,
#                 22.0,
#                 23.0,
#                 24.0,
#             ]
#         ),
#         "rotor_diameter": 168,
#         "turbine_type": "SCD168/8000",
#     }


# def params_turbine_v90_2kw():
#     """Params for a Turbuine type with 3 kw nominal power using power curve
#     Nominal power  in W.
#     """
#     return {
#         "name": "V90/2000 GS",
#         "nominal_power": 2000,
#         "power_curve_values": pd.Series(
#             [
#                 75.0,
#                 128.0,
#                 190.0,
#                 265.0,
#                 354.0,
#                 459.0,
#                 582.0,
#                 723.0,
#                 883.0,
#                 1058.0,
#                 1240.0,
#                 1427.0,
#                 1604.0,
#                 1762.0,
#                 1893.0,
#                 1968.0,
#                 2005.0,
#                 2021.0,
#                 2027.0,
#                 2029.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#                 2030.0,
#             ]
#         ),
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 4.0,
#                 4.5,
#                 5.0,
#                 5.5,
#                 6.0,
#                 6.5,
#                 7.0,
#                 7.5,
#                 8.0,
#                 8.5,
#                 9.0,
#                 9.5,
#                 10.0,
#                 10.5,
#                 11.0,
#                 11.5,
#                 12.0,
#                 12.5,
#                 13.0,
#                 13.5,
#                 14.0,
#                 14.5,
#                 15.0,
#                 15.5,
#                 16.0,
#                 16.5,
#                 17.0,
#                 17.5,
#                 18.0,
#                 18.5,
#                 19.0,
#                 19.5,
#                 20.0,
#                 20.5,
#                 21.0,
#                 21.5,
#                 22.0,
#                 22.5,
#                 23.0,
#                 23.5,
#                 24.0,
#                 24.5,
#                 25.0,
#             ]
#         ),
#         "rotor_diameter": 90,
#         "turbine_type": "V90/2000/GS",
#     }


# def params_turbine_v90_2kw2():
#     """Params for a Turbuine type with 2 kw nominal power using power
# coefficient
#     Nominal power  in W.
#     """
#     return {
#         "name": "V90/2000 GS",
#         "nominal_power": 2000,
#         "power_coefficient_curve_values": pd.Series(
#             [
#                 0.301,
#                 0.36,
#                 0.39,
#                 0.409,
#                 0.421,
#                 0.429,
#                 0.435,
#                 0.44,
#                 0.443,
#                 0.442,
#                 0.437,
#                 0.427,
#                 0.412,
#                 0.391,
#                 0.365,
#                 0.332,
#                 0.298,
#                 0.266,
#                 0.237,
#                 0.212,
#                 0.19,
#                 0.171,
#                 0.154,
#                 0.14,
#                 0.127,
#                 0.116,
#                 0.106,
#                 0.097,
#                 0.089,
#                 0.082,
#                 0.076,
#                 0.07,
#                 0.065,
#                 0.06,
#                 0.056,
#                 0.052,
#                 0.049,
#                 0.046,
#                 0.043,
#                 0.04,
#                 0.038,
#                 0.035,
#                 0.033,
#             ]
#         ),
#         "power_coefficient_curve_wind_speeds": pd.Series(
#             [
#                 4.0,
#                 4.5,
#                 5.0,
#                 5.5,
#                 6.0,
#                 6.5,
#                 7.0,
#                 7.5,
#                 8.0,
#                 8.5,
#                 9.0,
#                 9.5,
#                 10.0,
#                 10.5,
#                 11.0,
#                 11.5,
#                 12.0,
#                 12.5,
#                 13.0,
#                 13.5,
#                 14.0,
#                 14.5,
#                 15.0,
#                 15.5,
#                 16.0,
#                 16.5,
#                 17.0,
#                 17.5,
#                 18.0,
#                 18.5,
#                 19.0,
#                 19.5,
#                 20.0,
#                 20.5,
#                 21.0,
#                 21.5,
#                 22.0,
#                 22.5,
#                 23.0,
#                 23.5,
#                 24.0,
#                 24.5,
#                 25.0,
#             ]
#         ),
#         "rotor_diameter": 90,
#         "turbine_type": "V90/2000/GS",
#     }


# def params_turbine_e82_2kw2():
#     """Params for a Turbuine type with 2 kw nominal power using power curve
#     Nominal power  in W.
#     """
#     return {
#         "name": "E-82/2000 E2",
#         "nominal_power": 2000,
#         "power_coefficient_curve_values": pd.Series(
#             [
#                 0.0,
#                 0.12,
#                 0.29,
#                 0.4,
#                 0.43,
#                 0.46,
#                 0.48,
#                 0.49,
#                 0.5,
#                 0.49,
#                 0.42,
#                 0.35,
#                 0.29,
#                 0.23,
#                 0.19,
#                 0.15,
#                 0.13,
#                 0.11,
#                 0.09,
#                 0.08,
#                 0.07,
#                 0.06,
#                 0.05,
#                 0.05,
#                 0.04,
#             ]
#         ),
#         "power_coefficient_curve_wind_speeds": pd.Series(
#             [
#                 1.0,
#                 2.0,
#                 3.0,
#                 4.0,
#                 5.0,
#                 6.0,
#                 7.0,
#                 8.0,
#                 9.0,
#                 10.0,
#                 11.0,
#                 12.0,
#                 13.0,
#                 14.0,
#                 15.0,
#                 16.0,
#                 17.0,
#                 18.0,
#                 19.0,
#                 20.0,
#                 21.0,
#                 22.0,
#                 23.0,
#                 24.0,
#                 25.0,
#             ]
#         ),
#         "rotor_diameter": 82,
#         "turbine_type": "E-82/2000",
#     }


# def params_turbine_e82_2kw3():
#     """Params for a Turbuine type with 2 kw nominal power using power curve
#     Nominal power  in W.
#     """
#     return {
#         "name": "E-82/2000 E2",
#         "nominal_power": 2000,
#         "power_curve_values": pd.Series(
#             [
#                 0.0,
#                 3.0,
#                 25.0,
#                 82.0,
#                 174.0,
#                 321.0,
#                 532.0,
#                 815.0,
#                 1180.0,
#                 1580.0,
#                 1810.0,
#                 1980.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#                 2050.0,
#             ]
#         ),
#         "power_curve_wind_speeds": pd.Series(
#             [
#                 1.0,
#                 2.0,
#                 3.0,
#                 4.0,
#                 5.0,
#                 6.0,
#                 7.0,
#                 8.0,
#                 9.0,
#                 10.0,
#                 11.0,
#                 12.0,
#                 13.0,
#                 14.0,
#                 15.0,
#                 16.0,
#                 17.0,
#                 18.0,
#                 19.0,
#                 20.0,
#                 21.0,
#                 22.0,
#                 23.0,
#                 24.0,
#                 25.0,
#             ]
#         ),
#         "rotor_diameter": 82,
#         "turbine_type": "E-82/2000",
#     }


# def params_turbine_2T_2kw():
#     """Params for a Turbuine type with 2 kw nominal power using power curve
#     Nominal power  in W.
#     """
#     return (
#         {
#             "name": "V90-3.0 MW",
#             "nominal_power": 3000,
#             "power_coefficient_curve_values": nan,
#             "power_coefficient_curve_wind_speeds": nan,
#             "rotor_diameter": 90,
#             "turbine_type": "V90/3000",
#         },
#     )


# def params_turbine_s122_2kw():
#     """Params for a Turbuine type with 2 kw nominal power using power curve
#     Nominal power  in W.
#     """
#     return {
#         "name": "3.0M122",
#         "nominal_power": 3000,
#         "power_coefficient_curve_values": pd.Series(
#             [
#                 0.186,
#                 0.358,
#                 0.415,
#                 0.442,
#                 0.46,
#                 0.453,
#                 0.43,
#                 0.387,
#                 0.312,
#                 0.242,
#                 0.191,
#                 0.153,
#                 0.124,
#                 0.102,
#                 0.085,
#                 0.072,
#                 0.061,
#                 0.052,
#                 0.045,
#                 0.039,
#             ]
#         ),
#         "power_coefficient_curve_wind_speeds": pd.Series(
#             [
#                 3.0,
#                 4.0,
#                 5.0,
#                 6.0,
#                 7.0,
#                 8.0,
#                 9.0,
#                 10.0,
#                 11.0,
#                 12.0,
#                 13.0,
#                 14.0,
#                 15.0,
#                 16.0,
#                 17.0,
#                 18.0,
#                 19.0,
#                 20.0,
#                 21.0,
#                 22.0,
#             ]
#         ),
#         "rotor_diameter": 122,
#         "turbine_type": "S122/3000",
#     }


def load_static_data():
    data_path = os.path.abspath(
        os.path.join(__file__, "..", "static_data.csv")
    )
    curves_path = os.path.abspath(
        os.path.join(__file__, "..", "static_curves.csv")
    )
    data = {}
    with open(data_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                cols = row
            else:
                key = row[0]
                data[key] = {}
                for k, v in zip(cols, row):
                    try:
                        v = int(v)
                    except ValueError:
                        try:
                            v = float(v)
                        except ValueError:
                            if v == "false":
                                v = False
                            elif v == "true":
                                v = True
                    data[key][k] = v
    with open(curves_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                cols = row
            else:
                key = row[0]
                ts_type = row[1]
                ts = []
                for v in row[2:]:
                    ts.append(float(v))
                data[key][ts_type] = ts
    return data


# if __name__ == "__main__":
# params = [
#     params_turbine_e82_2kw,
#     params_turbine_e82_2kw2,
#     params_turbine_e82_2kw3,
#     params_turbine_s122_2kw,
#     params_turbine_e82_3kw,
#     params_turbine_n131_3kw,
#     params_turbine_ad116_5kw,
#     params_turbine_v164_8kw,
#     params_turbine_scd168_8kw,
# ]
# path = os.path.abspath(os.path.join(__file__, "..", "static_curves2.
# csv"))
# with open(path, "a") as csvfile:
#     writer = csv.writer(
#         csvfile,
#         delimiter=",",
#         # quotechar='"',
#         # quoting=csv.QUOTE_MINIMAL,
#     )

#     for fnc in params:
#         p = fnc()
#         line = []
#         ttype = p.get("turbine_type",p.get("name", ""))
#         if "power_curve_values" in p:

#             line = []
#             line.append(ttype)
#             power_curve = p.get("power_curve_values", pd.Series([]))
#             if not power_curve.empty:
#                 line.append("power_curve")
#                 for val in power_curve.values/power_curve.max():
#                     line.append(f"{val}")
#             writer.writerow(line)
#         if "power_curve_wind_speeds" in p:
#             line = []
#             line.append(ttype)
#             wind_speeds = p["power_curve_wind_speeds"]
#             if not wind_speeds.empty:
#                 line.append("wind_speeds")
#                 for val in wind_speeds.values:
#                     line.append(f"{val}")
#             writer.writerow(line)
#         if "power_coefficient_curve_values" in p:
#             line = []
#             line.append(ttype)
#             coeff = p["power_coefficient_curve_values"]
#             if not coeff.empty:
#                 line.append("power_coefficient")
#                 for val in coeff.values:
#                     line.append(f"{val}")
#             writer.writerow(line)
#         if "power_coefficient_curve_wind_speeds" in p:
#             line = []
#             line.append(ttype)
#             wind_speeds = p["power_coefficient_curve_wind_speeds"]
#             if not wind_speeds.empty:
#                 line.append("wind_speeds")
#                 for val in wind_speeds.values:
#                     line.append(f"{val}")
#             writer.writerow(line)
# p, i = turbine_preset(pn_max_kw=3)
# p2, i2 = turbine_preset(pn_max_kw=8)
# print()

# p, i = wind_power_plant_preset(pn_max_kw=2.6)
# print(p)
