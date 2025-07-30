"""This module contains the :class:`.Schedule` that is used by the
:class:`.ForecastModel` and :class:`.FlexibilityModel`.

"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from io import StringIO
from typing import Dict, Optional

import numpy as np
import pandas as pd

from pysimmods.util.date_util import GER, TZ

LOG = logging.getLogger(__name__)


class Schedule:
    """Schedule class for the :class:`.ScheduleModel`.

    Calling the schedule obj like this::

        df = schedule()

    returns the data frame that stores the schedule.


    Parameters
    ----------

    """

    def __init__(
        self,
        step_size: int = 1,
        horizon_hours: float = 1,
        start_date: Optional[datetime] = None,
        p_name: str = "p_kw",
        q_name: str = "q_kvar",
        p_set_name: Optional[str] = None,
        q_set_name: Optional[str] = None,
        store_min_and_max: bool = False,
    ):
        self._data: pd.DataFrame

        self.step_size = step_size
        self.horizon_hours = horizon_hours
        self.now_dt = start_date

        self.p_name = p_name
        self.q_name = q_name
        self.p_set_name = p_set_name
        self.q_set_name = q_set_name
        self.p_min_name = "p_min"
        self.p_max_name = "p_max"
        self.q_min_name = "q_min"
        self.q_max_name = "q_max"

        self.store_min_and_max = store_min_and_max

    def init(self):
        """Initialize the schedule data frame.

        After initialization, the schedule's data frame should have
        three columns *target*, *p_kw*, and *q_kvar* and a number of
        rows, each value initialized with np.nan.

        The number of rows is defined by the
        :attr:`_forecast_horizon_hours` as seconds divided by the
        :attr:`step_size`.

        """
        LOG.debug(
            "Creating new schedule dataframe (and wiping any existing data)."
        )
        columns = [self.p_name, self.q_name]

        if self.store_min_and_max:
            columns.extend(
                [
                    self.p_min_name,
                    self.p_max_name,
                    self.q_min_name,
                    self.q_max_name,
                ]
            )

        if self.p_set_name is None:
            unit = self.p_name.rsplit("_", 1)[1]
            self.p_set_name = f"p_set_{unit}"
        if self.q_set_name is None:
            unit = self.q_name.rsplit("_", 1)[1]
            self.q_set_name = f"q_set_{unit}"

        columns.insert(0, self.q_set_name)
        columns.insert(0, self.p_set_name)

        if self.now_dt is not None:
            index = pd.date_range(
                self.now_dt,
                self.now_dt
                + timedelta(hours=self.horizon_hours)
                - timedelta(seconds=self.step_size),
                freq=f"{self.step_size}s",
            )
        else:
            index = None

        self._data = pd.DataFrame(columns=columns, index=index)
        self._data.index = pd.to_datetime(self._data.index)

    def update(self, other):
        """Update this schedules' data with another dataframe.

        Parameters
        ----------
        other : pandas.DataFrame
            A dataframe with datetime as index and values for the
            columns *"target"*, *"p_kw"*, and *"q_kvar"*. Note that
            :attr:`pname` and :attr:`qname` match in both data frames.

        """

        if self._data is None:
            self.init()

        if isinstance(other, Schedule):
            other = other._data

        for col in other.columns:
            if col not in self._data.columns:
                raise ValueError(
                    f"Column '{col}' from other schedule is too much."
                )

        for index, _ in other.iterrows():
            if not self.has_index(index):
                break

        self._data.update(other.loc[:index])
        other = other.loc[index:]
        # https://stackoverflow.com/questions/77254777/alternative-to-concat-
        # of-empty-dataframe-now-that-it-is-being-deprecated
        self._data = pd.concat(
            [df for df in [self._data, other] if not df.empty]
        )
        self._data = self._data[~self._data.index.duplicated()]
        self._data.index = pd.to_datetime(self._data.index, utc=True)

    def update_row(
        self,
        index: datetime,
        p_set: float,
        q_set: Optional[float],
        p_val: float,
        q_val: float,
        p_min: float = 0,
        p_max: float = 0,
        q_min: float = 0,
        q_max: float = 0,
    ):
        if index in self._data.index:
            self._data.loc[index, self.p_set_name] = p_set
            self._data.loc[index, self.q_set_name] = q_set
            self._data.loc[index, self.p_name] = p_val
            self._data.loc[index, self.q_name] = q_val

            if self.store_min_and_max:
                self._data.loc[index, self.p_min_name] = p_min
                self._data.loc[index, self.p_max_name] = p_max
                self._data.loc[index, self.q_min_name] = q_min
                self._data.loc[index, self.q_max_name] = q_max

        else:
            tmp_df = pd.DataFrame(
                data={
                    self.p_set_name: p_set,
                    self.q_set_name: q_set,
                    self.p_name: p_val,
                    self.q_name: q_val,
                },
                index=[index],
            )

            if self.store_min_and_max:
                self._data.loc[index, self.p_min_name] = p_min
                self._data.loc[index, self.p_max_name] = p_max
                self._data.loc[index, self.q_min_name] = q_min
                self._data.loc[index, self.q_max_name] = q_max

            self._data = pd.concat([self._data, tmp_df])

        self._data.sort_index(inplace=True)
        self._data.index = pd.to_datetime(self._data.index)
        # self._data = self._data.ffill()
        # WTF pandas?!?
        self._data = self._data.astype(np.float64).fillna(value=np.nan)

    def update_entry(self, index, col, val):
        if col not in self._data.columns:
            raise ValueError(
                f"Invalid column '{col}'. Supported columns are "
                f"{self._data.columns}."
            )
        if index not in self._data.index:
            self._data = pd.concat(
                [self._data, pd.DataFrame({col: val}, index=[index])]
            )
        self._data.loc[index, col] = val
        self._data.sort_index(inplace=True)
        self._data = self._data.infer_objects(copy=False).fillna(value=np.nan)

    def has_index(self, index):
        return index in self._data.index

    def reschedule_required(self):
        """Check if a reschedule is required.

        The current schedule is checked for the next hours, specified
        by :attr:`_forecast_horizon_hours*. A reschedule is required
        when on of the indices is missing of one of the values within
        the limit is np.nan.

        Returns
        -------
        bool
            *True* when a reschedule is required and *False* otherwise.
        """
        now = self.now_dt + timedelta(seconds=self.step_size)
        limit = int(self.horizon_hours * 3_600 / self.step_size)

        for _ in range(limit):
            if now not in self._data.index:
                return True
            if self.get(now, self.p_set_name) is None:
                return True
            if self.get(now, self.q_set_name) is None:
                return True
            if self.get(now, self.p_name) is None:
                return True
            elif self.get(now, self.q_name) is None:
                return True
            if self.store_min_and_max:
                if self.get(now, self.p_min_name) is None:
                    return True
                if self.get(now, self.p_max_name) is None:
                    return True
                if self.get(now, self.q_min_name) is None:
                    return True
                if self.get(now, self.q_max_name) is None:
                    return True

            now += timedelta(seconds=self.step_size)

        return False

    def prune(self):
        self._data = self._data.loc[self.now_dt :]

    def get(self, now, col) -> Optional[float]:
        """Return the value for a certain column.

        If no time index is provided, the current datetime object of
        the schedule is used.

        Returns
        -------
        np.float
            The value of the specified column at index *now*.

        """
        if now is None:
            now = self.now_dt
        elif isinstance(now, str):
            now = datetime.strptime(now, GER).astimezone(timezone.utc)

        if now not in self._data.index:
            return None
        val = self._data.loc[now][col]

        if np.isnan(val):
            return None
        else:
            return val

    def to_dict(
        self,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        keep_datetime: bool = False,
    ) -> Dict[str, str]:
        if start_dt is None:
            start_dt = self._data.index[0]

        if end_dt is None:
            end_dt = self._data.index[-1]

        partition = self._data.loc[start_dt:end_dt]

        if not keep_datetime:
            partition.index = partition.index.astype(np.int64)

        return partition.to_dict()

    def from_dict(self, dict_of_schedules: Dict[str, str]) -> Schedule:
        df = pd.DataFrame(dict_of_schedules)
        df.index = pd.to_datetime(
            df.index.astype(np.int64), utc=True, origin="unix"
        )
        self.from_dataframe(df)

        return self

    def to_json(
        self,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
    ) -> str:
        if start_dt is None:
            start_dt = self._data.index[0]

        if end_dt is None:
            end_dt = self._data.index[-1]

        return self._data.loc[start_dt:end_dt].to_json()

    def from_json(self, schedule_json) -> Schedule:
        schedule_df = pd.read_json(StringIO(schedule_json)).tz_localize("UTC")
        self.from_dataframe(schedule_df)

    def __call__(self):
        return self._data

    def from_dataframe(self, dataframe: pd.DataFrame):
        self._data = dataframe
        self._data.index = pd.to_datetime(self._data.index).tz_convert(TZ)
        if "target" in self._data.columns:
            self.use_absolute_setpoints = False
            self.p_set_name = None
            self.q_set_name = None
        else:
            self.use_absolute_setpoints = True

        for col in self._data.columns:
            if "p_set" in col:
                self.p_set_name = col
            elif "q_set" in col:
                self.q_set_name = col
            elif "p_min" in col:
                self.p_min_name = col
                self.store_min_and_max = True
            elif "p_max" in col:
                self.p_max_name = col
                self.store_min_and_max = True
            elif "q_min" in col:
                self.q_min_name = col
                self.store_min_and_max = True
            elif "q_max" in col:
                self.q_max_name = col
                self.store_min_and_max = True
            elif "p_" in col:
                self.p_name = col
            elif "q_" in col:
                self.q_name = col

        self.now_dt = self._data.index[0].to_pydatetime()
        self.step_size = max(
            1,
            int(
                (self._data.index[-1] - self._data.index[0]).total_seconds()
                / (len(self._data.index) - 1)
            ),
        )
        return self

    def __repr__(self):
        return self._data.__repr__()

    def is_empty(self):
        if not hasattr(self, "_data"):
            return True

        return self._data.empty

    def compare(self, other: Schedule):
        return self._data.compare(other._data)
