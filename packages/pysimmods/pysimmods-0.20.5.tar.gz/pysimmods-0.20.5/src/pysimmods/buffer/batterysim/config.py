"""This module contains the config model for the battery model."""

from typing import Any, Dict, List

from ...model.config import ModelConfig

DEFAULT_SCHEDULE: List[float] = (
    [50, 59.451814, 60, 60, 60, 60, 50, 50]
    + [50, 35, 35, 35, 35, 50, 50, 70]
    + [70, 50, 35, 35, 50, 51, 51, 54]
)


class BatteryConfig(ModelConfig):
    """Captures the configuration parameters of the battery model

    On intitialization a dictionay with values for all configuration
    parameters has to be passed.

    The configuration parameters are constant during the simulation
    process. That is they are not manipulated in the step-method of
    the battery model and should not be changed during simulation
    from outside.

    Attributes
    ----------
    cap_kwh : float
        Capacity of the battery in [kWh].
    p_charge_max_kw : float
        Maximum charging (consumption) power of battery in [kW].
    p_discharge_max_kw : float
        Maximum discharging (generation) power of battery in [kW].
    soc_min_percent : float
        Minimum state of charge of battery in [%] of capacity.
    eta_pc : list
        Polynomial coefficients for calculating set power dependent eta.
    """

    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)

        self.cap_kwh: float = abs(params["cap_kwh"])
        self.p_charge_max_kw: float = abs(params["p_charge_max_kw"])
        self.p_charge_min_kw: float = 0
        self.p_discharge_max_kw: float = abs(params["p_discharge_max_kw"])
        self.p_discharge_min_kw: float = 0
        self.soc_min_percent: float = params.get("soc_min_percent", 0.0)
        self.eta_pc: List[float] = params.get(
            "eta_pc", [-2.109566, 0.403556, 97.110770]
        )

        self.default_p_schedule: List[float] = []
        for val in params.get("default_p_schedule", DEFAULT_SCHEDULE):
            val = val * 2 - 100
            if val == 0:
                self.default_p_schedule.append(0.0)
            elif -100 <= val < 0:
                self.default_p_schedule.append(
                    val / 100.0 * self.p_discharge_max_kw
                )
            elif 0 < val <= 100:
                self.default_p_schedule.append(
                    val / 100.0 * self.p_charge_max_kw
                )

        self.default_q_schedule: List[float] = [0.0] * 24
