"""This module contains a model of a wind turbine and an inverter"""

from ...model.qgenerator import QGenerator
from ...other.invertersim.inverter import Inverter
from .. import WindPowerPlant
from .config import WindSystemConfig
from .inputs import WindSystemInputs
from .state import WindSystemState


class WindPowerPlantSystem(QGenerator):
    def __init__(self, params, inits):
        self.config = WindSystemConfig(params)
        self.inputs = WindSystemInputs()
        self.state = WindSystemState(inits)

        self.wind = WindPowerPlant(params["wind"], inits["wind"])
        self.inverter = Inverter(params["inverter"], inits["inverter"])

    def step(self):
        """Perform simulation step."""

        # Step the wind turbine
        self.wind.inputs.step_size = self.inputs.step_size
        self.wind.inputs.now_dt = self.inputs.now_dt
        self.wind.inputs.wind_v_m_per_s = self.inputs.wind_v_m_per_s
        self.wind.inputs.t_air_deg_celsius = self.inputs.t_air_deg_celsius
        self.wind.inputs.air_pressure_hpa = self.inputs.air_pressure_hpa
        self.wind.step()

        # Step the inverter
        self.inverter.inputs.p_in_kw = self.wind.state.p_kw
        self.inverter.inputs.p_set_kw = self.inputs.p_set_kw
        self.inverter.inputs.q_set_kvar = self.inputs.q_set_kvar
        self.inverter.inputs.cos_phi_set = self.inputs.cos_phi_set
        self.inverter.inputs.inductive = self.inputs.inverter_inductive
        self.inverter.step()

        # Update state
        self.state.p_kw = self.inverter.state.p_kw
        self.state.p_possible_max_kw = self.wind.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar
        self.state.cos_phi = self.inverter.state.cos_phi
        self.state.inverter_inductive = self.inverter.state.inductive
        self.state.wind_hub_v_m_per_s = self.wind.state.wind_hub_v_m_per_s
        self.state.t_air_hub_deg_kelvin = self.wind.state.t_air_hub_deg_kelvin
        self.state.air_density_hub_kg_per_m3 = (
            self.wind.state.air_density_hub_kg_per_m3
        )

        self.inputs.reset()

    def get_state(self):
        state_dict = {
            "wind": self.wind.get_state(),
            "inverter": self.inverter.get_state(),
        }
        return state_dict

    def set_state(self, state_dict):
        self.wind.set_state(state_dict["wind"])
        self.inverter.set_state(state_dict["inverter"])

        self.state.p_kw = self.inverter.state.p_kw
        self.state.p_possible_max_kw = self.wind.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar
        self.state.cos_phi = self.inverter.state.cos_phi
        self.state.inverter_inductive = self.inverter.state.inductive
        self.state.wind_hub_v_m_per_s = self.wind.state.wind_hub_v_m_per_s
        self.state.t_air_hub_deg_kelvin = self.wind.state.t_air_hub_deg_kelvin
        self.state.air_density_hub_kg_per_m3 = (
            self.wind.state.air_density_hub_kg_per_m3
        )

    def set_q_kvar(self, q_kvar: float):
        self.inputs.q_set_kvar = q_kvar
