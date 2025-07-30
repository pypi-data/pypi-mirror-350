import calendar
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import mosaik_api_v3
import numpy as np
from midas.util.dateformat import GER
from midas.util.logging import set_and_init_logger

from .meta import META

LOG = logging.getLogger(__name__)

SECONDS_PER_DAY = 24 * 60 * 60
SECONDS_PER_WEEK = SECONDS_PER_DAY * 7
SECONDS_PER_YEAR = SECONDS_PER_DAY * 365
SECONDS_PER_LEAP_YEAR = SECONDS_PER_DAY * 366


class TimeSimulator(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)

        self.sid: str
        self.eid: str
        self._sin_time_day: float
        self._cos_time_day: float
        self._sin_time_week: float
        self._cos_time_week: float
        self._sin_time_year: float
        self._cos_time_year: float

        self._step_size: int
        self._utc_now_dt: datetime
        self._local_now_dt: datetime

        self._day_dif_td: timedelta
        self._week_dif_td: timedelta
        self._year_dif_td: timedelta

        self._time_schedule: Optional[list[str]] = None
        self._current_schedule_idx: int = 0

    def init(self, sid: str, **sim_params):
        self.sid = sid
        self.eid = ""
        self._step_size = sim_params.get("step_size", 900)
        self._local_now_dt = datetime.strptime(
            sim_params.get("start_date", "2020-01-01 00:00:00+0100"), GER
        )
        self._utc_now_dt = self._local_now_dt.astimezone(timezone.utc)

        self._day_dif_td = self._local_now_dt - self._local_now_dt.replace(
            hour=0, minute=0, second=0
        )
        self._year_dif_td = self._local_now_dt - self._local_now_dt.replace(
            month=1, day=1, hour=0, minute=0, second=0
        )
        self._week_dif_td = timedelta(days=self._local_now_dt.weekday())

        self._time_schedule = sim_params.get("time_schedule", None)
        return self.meta

    def create(self, num: int, model: str, **model_params):
        errmsg = (
            "You should really not try to instantiate more than one ",
            "timegenerator.",
        )
        assert num == 1 and self.eid == "", errmsg

        self.eid = "Timegenerator-0"
        return [{"eid": self.eid, "type": model}]

    def step(self, time: int, inputs: Dict[str, Any], max_advance: int = 0):

        if self._time_schedule is not None and self._time_schedule:
            # Loop-iterating over the dates of the time schedule
            self._local_now_dt = datetime.strptime(
                self._time_schedule[self._current_schedule_idx], GER
            )
            self._utc_now_dt = self._local_now_dt.astimezone(timezone.utc)
            self._current_schedule_idx = (
                self._current_schedule_idx + 1
            ) % len(self._time_schedule)
        elif time > 0:
            # Setting the time for all simulators, so updating the
            # time ... but not in the first step.
            self._local_now_dt += timedelta(seconds=self._step_size)
            self._utc_now_dt += timedelta(seconds=self._step_size)

        if calendar.isleap(self._local_now_dt.year):
            seconds_per_year = SECONDS_PER_LEAP_YEAR
        else:
            seconds_per_year = SECONDS_PER_YEAR

        self.sin_time_day = np.sin(
            2
            * np.pi
            * (time + self._day_dif_td.total_seconds())
            / SECONDS_PER_DAY
        )
        self.sin_time_week = np.sin(
            2
            * np.pi
            * (time + self._week_dif_td.total_seconds())
            / SECONDS_PER_WEEK
        )
        self.sin_time_year = np.sin(
            2
            * np.pi
            * (time + self._year_dif_td.total_seconds())
            / seconds_per_year
        )
        self.cos_time_day = np.cos(
            2
            * np.pi
            * (time + self._day_dif_td.total_seconds())
            / SECONDS_PER_DAY
        )
        self.cos_time_week = np.cos(
            2
            * np.pi
            * (time + self._week_dif_td.total_seconds())
            / SECONDS_PER_WEEK
        )
        self.cos_time_year = np.cos(
            2
            * np.pi
            * (time + self._year_dif_td.total_seconds())
            / seconds_per_year
        )

        return time + self._step_size

    def get_data(self, outputs):
        data = {}
        data[self.eid] = {}
        data[self.eid]["sin_day_time"] = self.sin_time_day
        data[self.eid]["sin_week_time"] = self.sin_time_week
        data[self.eid]["sin_year_time"] = self.sin_time_year
        data[self.eid]["cos_day_time"] = self.cos_time_day
        data[self.eid]["cos_week_time"] = self.cos_time_week
        data[self.eid]["cos_year_time"] = self.cos_time_year
        data[self.eid]["utc_time"] = self._utc_now_dt.strftime(GER)
        data[self.eid]["local_time"] = self._local_now_dt.strftime(GER)
        data[self.eid]["unix_time"] = self._utc_now_dt.timestamp()

        return data


if __name__ == "__main__":
    set_and_init_logger(
        0, "timesim-logfile", "midas-timesim.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api_v3.start_simulation(TimeSimulator())
