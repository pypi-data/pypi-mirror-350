"""This module contains the *mosaik_api* meta definition for pysimmods
models.
"""

from pysimmods.buffer.batterysim import Battery
from pysimmods.consumer.hvacsim import HVAC
from pysimmods.generator import WindPowerPlantSystem
from pysimmods.generator.biogassim import BiogasPlant
from pysimmods.generator.chplpgsystemsim import CHPLPGSystem
from pysimmods.generator.dieselsim import DieselGenerator
from pysimmods.generator.pvsystemsim import PVPlantSystem

_SHARED_ATTRS = [
    "p_set_mw",
    "p_set_kw",
    "p_mw",
    "p_kw",
    "q_mvar",
    "q_kvar",
    "local_time",
]


META = {
    "type": "time-based",
    "models": {
        "Battery": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": ["soc_percent"] + _SHARED_ATTRS,
        },
        "Photovoltaic": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "q_set_mvar",
                "q_set_kvar",
                "t_air_deg_celsius",
                "t_module_deg_celsius",
                "bh_w_per_m2",
                "dh_w_per_m2",
                "s_module_w_per_m2",
                "inverter_inductive",
                "p_possible_max_mw",
            ]
            + _SHARED_ATTRS,
        },
        "CHP": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "day_avg_t_air_deg_celsius",
                "p_th_mw",
                "e_th_demand_set_kwh",
                "e_th_demand_kwh",
            ]
            + _SHARED_ATTRS,
        },
        "HVAC": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": ["t_air_deg_celsius"] + _SHARED_ATTRS,
        },
        "Biogas": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": ["p_th_mw"] + _SHARED_ATTRS,
        },
        "DieselGenerator": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": _SHARED_ATTRS,
        },
        "WindTurbine": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "wind_v_m_per_s",
                "t_air_deg_celsius",
                "air_pressure_hpa",
                "inverter_inductive",
                "p_possible_max_mw",
            ]
            + _SHARED_ATTRS,
        },
    },
}

MODELS = {
    "Photovoltaic": PVPlantSystem,
    "HVAC": HVAC,
    "Battery": Battery,
    "CHP": CHPLPGSystem,
    "DieselGenerator": DieselGenerator,
    "Biogas": BiogasPlant,
    "WindTurbine": WindPowerPlantSystem,
}
