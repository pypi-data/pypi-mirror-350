"""This module contains the state model for pv."""

from pysimmods.model.state import ModelState


class WindPowerPlantState(ModelState):
    """State parameters of Wind model.

    See :class:`pysimmods.model.state.ModelState` for additional
    information.

    Parameters
    ----------
    inits : dict
        Contains the initial configuration of this wind plant. See
        attributes section for specific to the wind plant.

    Attributes
    ----------
    t_module_deg_celsius : float
        Temperature of the module in [°C].

    """

    def __init__(self, inits):
        super().__init__(inits)

        self.wind_hub_v_m_per_s: float
        self.t_air_hub_deg_kelvin: float
        self.air_density_hub_kg_per_m3: float
