"""This module contains the state model for the PV system."""

from pysimmods.model.state import ModelState


class PVSystemState(ModelState):
    """State variables of PV plant system model.

    Parameters
    ----------
    inits : dict
        A *dict* containing initialization parameters.

    Attributes
    ----------
    t_module_deg_celsius : float
        See :attr:`~.PVState.t_module_deg_celsius`
    p_kw : float
        See :attr:`~.ModelState.p_kw`
    q_kvar : float
        See :attr:`~.ModelState.q_kvar`
    p_possible_max_kw: float
        Power output of the PV module before inverter gets active.

    """

    def __init__(self, inits):
        super().__init__(inits)

        self.t_module_deg_celsius = inits["pv"]["t_module_deg_celsius"]
        self.p_possible_max_kw = 0
