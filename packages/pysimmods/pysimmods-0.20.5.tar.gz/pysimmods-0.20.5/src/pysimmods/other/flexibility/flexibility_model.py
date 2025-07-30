"""This module contains the flexibility model."""

import logging
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd

from pysimmods.util.date_util import GER

from .flexibilities import Flexibilities
from .forecast_model import ForecastModel
from .schedule import Schedule

LOG = logging.getLogger(__name__)


class FlexibilityModel(ForecastModel):
    """The flexibility model for all pysimmods."""

    def __init__(
        self,
        model,
        unit="kw",
        prioritize_setpoint: bool = False,
        step_size: Optional[int] = None,
        now_dt: Optional[datetime] = None,
        forecast_horizon_hours=1,
        seed=None,
        store_min_and_max: bool = False,
    ):
        super().__init__(
            model,
            unit,
            prioritize_setpoint,
            step_size,
            now_dt,
            forecast_horizon_hours,
        )

        self._store_min_and_max = store_min_and_max

        if seed is not None:
            self._rng = np.random.RandomState(seed)
        else:
            self._rng = np.random.RandomState()

    def generate_schedules(
        self, start, flexibility_horizon_hours, num_schedules
    ):
        """Perform sampling and generate a set of schedules for the
        specified time interval.

        Args:
            start (str): Is the start of the planning horizon for which
                the sampling is done. It has to be provided as ISO 8601
                timezone string such as '2020-06-22 12:00:00+0000'

            forecast_horizon_hours (int): The planning horizon is divided into.

        """
        state_backup = self._model.get_state()
        step_size = self._step_size

        now_dt = self._now_dt
        start_dt = datetime.strptime(start, GER)
        end_dt = (
            start_dt
            + timedelta(hours=flexibility_horizon_hours)
            - timedelta(seconds=step_size)
        )
        periods = int(flexibility_horizon_hours * 3_600 / step_size)

        # Fast forward to the planning interval
        while start_dt > now_dt:
            try:
                self._calculate_step(
                    now_dt,
                    self.schedule.get(now_dt, self._psetname),
                    self.schedule.get(now_dt, self._qsetname),
                )
                now_dt += timedelta(seconds=step_size)
            except KeyError as err:
                # raise err
                LOG.info("Could not create flexibilities: %s", err)
                return {}

        index = pd.date_range(start_dt, end_dt, periods=periods)

        self.flexibilities = Flexibilities()

        for schedule_id in range(num_schedules):
            self.flexibilities.add_schedule(schedule_id, self.sample(index))

        self._model.set_state(state_backup)
        return self.flexibilities

    def sample(self, index):
        dataframe = pd.DataFrame(
            columns=[self._psetname, self._qsetname, self._pname, self._qname],
            index=index,
        )
        dataframe[self._psetname] = self._rng.uniform(
            low=self.get_pn_min_kw(),
            high=self.get_pn_max_kw(),
            size=len(index),
        )
        dataframe[self._qsetname] = self._rng.uniform(
            low=self.get_qn_min_kvar(),
            high=self.get_qn_max_kvar(),
            size=len(index),
        )

        state_backup = self._model.get_state()
        for index, row in dataframe.iterrows():
            try:
                self._calculate_step(
                    index, row[self._psetname], row[self._qsetname]
                )
                dataframe.loc[index, self._pname] = (
                    self._model.get_p_kw() * self._unit_factor
                )
                dataframe.loc[index, self._qname] = (
                    self._model.get_q_kvar() * self._unit_factor
                )

            except KeyError:
                # Forecast is missing
                dataframe.loc[index, self._pname] = np.nan
                dataframe.loc[index, self._qname] = np.nan
                dataframe.loc[index, self._psetname] = np.nan
                dataframe.loc[index, self._qsetname] = np.nan
        self._model.set_state(state_backup)

        return Schedule().from_dataframe(dataframe)
