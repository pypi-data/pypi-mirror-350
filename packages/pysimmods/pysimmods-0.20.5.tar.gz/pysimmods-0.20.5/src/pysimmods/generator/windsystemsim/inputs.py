"""This module contains the input model for the Wind Turbine System."""

from typing import Optional

from ...model.inputs import ModelInputs


class WindSystemInputs(ModelInputs):
    def __init__(self):
        super().__init__()

        self.cos_phi_set: Optional[float] = None
        self.inverter_inductive: Optional[bool] = None

        self.t_air_deg_celsius: Optional[float] = None
        self.wind_v_m_per_s: Optional[float] = None
        self.air_pressure_hpa: Optional[float] = None

        # Not used yet
        self.wind_dir_deg: Optional[float] = None
