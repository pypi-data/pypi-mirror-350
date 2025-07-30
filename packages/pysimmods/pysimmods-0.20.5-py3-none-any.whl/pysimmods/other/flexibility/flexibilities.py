from __future__ import annotations

import json
from typing import Dict

from .schedule import Schedule


class Flexibilities:
    def __init__(self):
        self._schedules: Dict[str, Schedule] = {}

    def add_schedule(self, schedule_id, schedule):
        self._schedules[f"{schedule_id}"] = schedule

    def __len__(self):
        return len(self._schedules)

    def items(self):
        for key, val in self._schedules.items():
            yield key, val

    def to_json(self):
        d = {key: val.to_dict() for key, val in self._schedules.items()}

        return json.dumps(d)

    def from_json(self, json_str: str) -> Flexibilities:
        self._schedules = {}
        d = json.loads(json_str)

        for key, schedule_dict in d.items():
            self._schedules[key] = Schedule().from_dict(schedule_dict)

        return self

    def __getitem__(self, key):
        return self._schedules[key]
