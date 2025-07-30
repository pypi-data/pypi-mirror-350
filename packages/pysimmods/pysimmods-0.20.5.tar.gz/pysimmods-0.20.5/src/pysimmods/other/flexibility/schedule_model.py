from datetime import datetime
from typing import Optional, Tuple

import numpy as np

from pysimmods.model.model import Model
from pysimmods.other.flexibility.schedule import Schedule


class ScheduleModel:
    """A wrapper for pysimmods, which allows models to use schedules.

    Parameters
    ----------
    model: :class:`.Model`
        The model that should be wrapped by the schedule model.
    unit: str, optional
        The unit to be used by the schedule. Default is `kw` for kilo
        watt. Other options are `w` and `mw`.
    prioritize_setpoint: bool, optional
        If set to True, this model will prefer setpoints rather than
        schedule values if setpoints are present. Default is False.
    """

    def __init__(
        self,
        model: Model,
        unit: str = "kw",
        prioritize_setpoint: bool = False,
        step_size: Optional[int] = None,
        now_dt: Optional[datetime] = None,
    ):
        self._model = model
        self._prioritize_setpoint = prioritize_setpoint

        if unit == "mw":
            self._unit_factor = 1e-3
            unit_str = "m"

        elif unit == "w":
            self._unit_factor = 1e3
            unit_str = ""
        else:
            self._unit_factor = 1
            unit_str = "k"

        self._pname = f"p_{unit_str}w"
        self._qname = f"q_{unit_str}var"
        self._psetname = f"p_set_{unit_str}w"
        self._qsetname = f"q_set_{unit_str}var"

        self.schedule: Schedule = Schedule()
        self._step_size: Optional[float] = step_size
        self._now_dt: Optional[datetime] = now_dt
        self._percent_factor: float

        if self._model.config.use_decimal_percent:
            self._percent_factor = 0.01
        else:
            self._percent_factor = 1.0

    def update_schedule(self, schedule):
        if self.schedule.is_empty():
            self._check_inputs()
        self.schedule.update(schedule)

    def step(self):
        """Perform a simulation step of the underlying model."""

        self._check_inputs()

        p_set, q_set = self._get_setpoints()
        self._model.set_p_kw(p_set)
        self._model.set_q_kvar(q_set)

        self._model.step()

        if p_set is None:
            p_set = self._model.get_p_kw()
        if q_set is None:
            q_set = self._model.get_q_kvar()

        self.schedule.update_row(
            self._now_dt,
            p_set * self._unit_factor,
            q_set * self._unit_factor,
            self._model.get_p_kw() * self._unit_factor,
            self._model.get_q_kvar() * self._unit_factor,
        )
        self.schedule.now_dt = self._now_dt
        self.schedule.prune()

    def _check_inputs(self) -> None:
        # Check if model has a different step size
        if (
            self._model.inputs.step_size is not None
            and self._model.inputs.step_size != self._step_size
        ):
            self._step_size = self._model.inputs.step_size

        # Check if model uses a different time
        if (
            self._model.inputs.now_dt is not None
            and self._model.inputs.now_dt != self._now_dt
        ):
            self._now_dt = self._model.inputs.now_dt

        # Initialize schedule if necessary
        if self.schedule.is_empty():
            self.schedule.p_name = self._pname
            self.schedule.q_name = self._qname
            self.schedule.now_dt = self._now_dt
            self.schedule.step_size = self._step_size
            self.schedule.p_set_name = self._psetname
            self.schedule.q_set_name = self._qsetname

            self.schedule.horizon_hours = self._step_size / 3_600
            self.schedule.init()

    def _get_setpoints(self) -> Tuple[Optional[float], Optional[float]]:
        try:
            schedule_p = (
                self.schedule.get(self._now_dt, self._psetname)
                / self._unit_factor
            )
        except TypeError:
            schedule_p = None
        try:
            schedule_q = (
                self.schedule.get(self._now_dt, self._qsetname)
                / self._unit_factor
            )
        except TypeError:
            schedule_q = None

        model_p = self._model.get_p_set_kw()
        model_q = self._model.get_q_set_kvar()

        default_p = self._model.get_default_p_set(self._now_dt.hour)
        default_q = self._model.get_default_q_set(self._now_dt.hour)

        priority = [(schedule_p, schedule_q), (model_p, model_q)]
        if self._prioritize_setpoint:
            priority = priority[::-1]
        priority.append((default_p, default_q))

        setpoint = (None, None)
        for setvals in priority[::-1]:
            if setvals[0] is not None and ~np.isnan(setvals[0]):
                setpoint = (setvals[0], setpoint[1])
            if setvals[1] is not None and ~np.isnan(setvals[1]):
                setpoint = (setpoint[0], setvals[1])

        return setpoint

    def set_step_size(self, step_size):
        self._model.set_step_size(step_size)
        self._step_size = self._model.inputs.step_size

    def set_now_dt(self, now_dt):
        self._model.set_now_dt(now_dt)
        self._now_dt = self._model.inputs.now_dt

    def set_p_kw(self, p_kw):
        self._model.set_p_kw(p_kw)

    def set_q_kvar(self, q_kvar):
        self._model.set_q_kvar(q_kvar)

    def get_now_dt(self):
        return self._model.get_now_dt()

    def get_p_kw(self):
        return self._model.get_p_kw()

    def get_q_kvar(self):
        return self._model.get_q_kvar()

    def get_pn_max_kw(self):
        return self._model.get_pn_max_kw()

    def get_pn_min_kw(self):
        return self._model.get_pn_min_kw()

    def get_qn_max_kvar(self):
        return self._model.get_qn_max_kvar()

    def get_qn_min_kvar(self):
        return self._model.get_qn_min_kvar()

    @property
    def inputs(self):
        return self._model.inputs

    @property
    def config(self):
        return self._model.config

    @property
    def state(self):
        return self._model.state
