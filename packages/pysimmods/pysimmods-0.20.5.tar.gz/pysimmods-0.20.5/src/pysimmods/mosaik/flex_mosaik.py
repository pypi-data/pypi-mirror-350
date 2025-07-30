"""This module contains a :class:`mosaik_api.Simulator` for the
flexiblity model, which is a wrapper for all models of the
pysimmods package.

"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union

import mosaik_api_v3
import numpy as np
import pandas as pd
from midas.util.dict_util import tobool
from midas.util.logging import set_and_init_logger
from midas.util.runtime_config import RuntimeConfig

from pysimmods.mosaik import LOG
from pysimmods.other.flexibility.flexibility_model import FlexibilityModel
from pysimmods.other.flexibility.forecast_model import ForecastModel
from pysimmods.other.flexibility.schedule_model import ScheduleModel
from pysimmods.util.date_util import GER

from .meta import MODELS
from .pysim_mosaik import PysimmodsSimulator


class FlexibilitySimulator(PysimmodsSimulator):
    """The generic flexiblity mosaik simulator for all pysimmods."""

    def __init__(self):
        super().__init__()

        self.models: Dict[str, ScheduleModel] = {}
        self.num_models: Dict[str, int] = {}

        self.sid: str
        self.step_size: int
        self.now_dt: datetime

        self.unit: str
        self.use_decimal_percent: bool
        self.prioritize_setpoint: bool
        self.provide_forecasts: bool
        self.provide_flexibilities: bool
        self.forecast_horizon_hours: float
        self.planning_horizon_hours: float
        self.flexibility_horizon_hours: float
        self.num_schedules: int
        self.rng: np.random.RandomState

    def init(self, sid: str, **sim_params: Dict[str, Any]):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        start_date : str
            The start date as UTC ISO 8601 date string.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.
        unit: str

        use_decimal_percent

        prioritize_setpoint

        provide_forecasts

        forecast_horizon_hours

        provide_flexibilities

        planning_horizon_hours

        flexibility_horizon_hours

        num_schedules

        seed

        key_value_logs

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).

        """
        self.sid = sid
        self.step_size = sim_params.get("step_size", 900)
        self.now_dt = datetime.strptime(
            sim_params["start_date"], GER
        ).astimezone(timezone.utc)

        self.unit = sim_params.get("unit", "kw")
        self.use_decimal_percent = tobool(
            sim_params.get("use_decimal_percent", False)
        )

        self.prioritize_setpoint = tobool(
            sim_params.get("prioritize_setpoint", False)
        )
        self.provide_forecasts = tobool(
            sim_params.get("provide_forecasts", False)
        )
        self.forecast_horizon_hours = sim_params.get(
            "forecast_horizon_hours", self.step_size / 3_600
        )

        self.provide_flexibilities = tobool(
            sim_params.get("provide_flexibilities", False)
        )
        self.planning_horizon_hours = sim_params.get(
            "planning_horizon_hours", 1.0
        )
        self.flexibility_horizon_hours = sim_params.get(
            "flexibility_horizon_hours", 2.0
        )
        self.num_schedules = sim_params.get("num_schedules", 10)
        self.rng = np.random.RandomState(sim_params.get("seed", None))

        self.key_value_logs = sim_params.get(
            "key_value_logs", RuntimeConfig().misc.get("key_value_logs", False)
        )
        self._update_meta()

        return self.meta

    def create(
        self,
        num: int,
        model: str,
        params: Dict[str, Any],
        inits: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.
        params: Dict[str, Any]
            The parameters dictionary for the model to create.
        inits: Dict[str, Any]
            The initial state dictionary for the model to create.

        Returns
        -------
        List[Dict[str, str]]
            A list with information on the created entity.

        """
        entities: List[Dict[str, str]] = []
        params.setdefault("use_decimal_percent", self.use_decimal_percent)
        self.num_models.setdefault(model, 0)

        for _ in range(num):
            eid = f"{model}-{self.num_models[model]}"

            if self.provide_flexibilities:
                self.models[eid] = FlexibilityModel(
                    MODELS[model](params, inits),
                    unit=self.unit,
                    prioritize_setpoint=self.prioritize_setpoint,
                    forecast_horizon_hours=self.forecast_horizon_hours,
                    seed=self.rng.randint(2**32 - 1),
                )

            elif self.provide_forecasts:
                self.models[eid] = ForecastModel(
                    MODELS[model](params, inits),
                    unit=self.unit,
                    prioritize_setpoint=self.prioritize_setpoint,
                    forecast_horizon_hours=self.forecast_horizon_hours,
                )

            else:
                self.models[eid] = ScheduleModel(
                    MODELS[model](params, inits),
                    unit=self.unit,
                    prioritize_setpoint=self.prioritize_setpoint,
                )

            self.num_models[model] += 1
            entities.append({"eid": eid, "type": model})
        return entities

    def step(
        self,
        time: int,
        inputs: Dict[str, Dict[str, Dict[str, Any]]],
        max_advance: int = 0,
    ) -> int:
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        if not self.key_value_logs:
            LOG.debug("At step %d: Received inputs: %s.", time, inputs)

        self._set_default_inputs()

        for eid, attrs in inputs.items():
            for attr, src_ids in attrs.items():
                if "forecast" in attr:
                    self._set_attr_forecast(eid, src_ids)
                elif attr == "schedule":
                    self._set_attr_schedule(eid, src_ids)
                elif attr == "local_time":
                    self._set_attr_local_time(eid, src_ids)
                else:
                    attr_sum = self._aggregate_attr(src_ids)
                    self._set_remaining_attrs(eid, attr, attr_sum)

        for model in self.models.values():
            model.step()

        self.now_dt += timedelta(seconds=self.step_size)
        self._generate_flexibilities()

        return time + self.step_size

    def get_data(
        self, outputs: Dict[str, List[str]]
    ) -> Dict[str, Dict[str, Any]]:
        """Returns the requested outputs (if feasible)"""

        data: Dict[str, Dict[str, Any]] = {}
        for eid, attrs in outputs.items():
            data[eid] = {}

            log_msg = {
                "id": f"{self.sid}_{eid}",
                "name": eid,
                "type": eid.split("-")[0],
            }

            for attr in attrs:
                if attr == "flexibilities":
                    value = self._get_attr_flexibilities(eid)
                    log_msg[attr] = json.loads(value)

                elif attr == "schedule":
                    value = self._get_attr_schedule(eid)
                    log_msg[attr] = json.loads(value)

                else:
                    value = self._get_remaining_attrs(eid, attr)
                    log_msg[attr] = value

                data.setdefault(eid, dict())[attr] = value

            if self.key_value_logs:
                LOG.info(json.dumps(log_msg))

        if not self.key_value_logs:
            LOG.debug("Gathered outputs: %s.", data)
        else:
            LOG.debug(data)

        return data

    def _update_meta(self):
        for model in self.meta["models"].keys():
            self.meta["models"][model]["attrs"].extend(
                ["flexibilities", "schedule", "target"]
            )

        self.meta["models"]["Photovoltaic"]["attrs"].extend(
            [
                "forecast_t_air_deg_celsius",
                "forecast_bh_w_per_m2",
                "forecast_dh_w_per_m2",
            ]
        )
        self.meta["models"]["CHP"]["attrs"].extend(
            ["forecast_day_avg_t_air_deg_celsius"]
        )
        self.meta["models"]["HVAC"]["attrs"].extend(
            ["forecast_t_air_deg_celsius"]
        )

    def _set_attr_forecast(self, eid: str, src_ids: Dict[str, Any]):
        for forecast in src_ids.values():
            if not isinstance(forecast, pd.DataFrame):
                forecast = pd.read_json(forecast).tz_localize("UTC")
            self.models[eid].update_forecasts(forecast)

    def _set_attr_schedule(self, eid: str, src_ids: Dict[str, Any]):
        for schedule in src_ids.values():
            if schedule is not None:
                schedule = deserialize_schedule(schedule)

                if not schedule.empty:
                    self.models[eid].update_schedule(schedule)

    def _get_attr_schedule(self, eid: str) -> str:
        value = self.models[eid].schedule.to_json(
            self.now_dt,
            self.now_dt
            + timedelta(hours=self.forecast_horizon_hours)
            - timedelta(seconds=self.step_size),
        )

        return value

    def _get_attr_flexibilities(self, eid: str) -> str:
        dict_of_json = self.models[eid].flexibilities.to_json()
        # value = json.dumps(dict_of_json)
        return dict_of_json

    def _generate_flexibilities(self):
        if self.provide_flexibilities:
            for model in self.models.values():
                model.generate_schedules(
                    (
                        self.now_dt
                        + timedelta(hours=self.planning_horizon_hours)
                    ).strftime(GER),
                    self.flexibility_horizon_hours,
                    self.num_schedules,
                )


def deserialize_schedule(
    schedule: Union[pd.DataFrame, Dict[str, Any], str],
) -> pd.DataFrame:
    """Convert the schedule provided by mosaik to DataFrame"""

    if isinstance(schedule, pd.DataFrame):
        return schedule

    if isinstance(schedule, dict):
        # The schedule might be nested into the schedule because of an
        # ICT simulator
        return deserialize_schedule(list(schedule.values())[0])

    if isinstance(schedule, str):
        return pd.read_json(schedule).tz_localize("UTC")

    raise ValueError(
        f"Unsupported schedule format {type(schedule)}: {schedule}"
    )


if __name__ == "__main__":
    set_and_init_logger(
        0, "pysimmods-logfile", "pysimmods-flex.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api_v3.start_simulation(FlexibilitySimulator())
