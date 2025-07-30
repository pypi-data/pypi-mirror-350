"""This module contains different DummyModels, which only implement the
the model interfaces. Their purpose is mainly for testing.

"""

from typing import Any, Dict

from pysimmods.model.config import ModelConfig
from pysimmods.model.inputs import ModelInputs
from pysimmods.model.model import Model
from pysimmods.model.state import ModelState


class DummyConfig(ModelConfig):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)

        self.p_max_kw: float = params.get("p_max_kw", 500)
        self.p_min_kw: float = params.get("p_min_kw", 250)
        self.q_min_kvar: float = params.get("q_min_kvar", -550)
        self.q_max_kvar: float = params.get("q_max_kvar", 550)
        self.default_p_schedule = [375.0] * 24
        self.default_q_schedule = [125.0] * 24


class DummyState(ModelState):
    pass


class DummyInputs(ModelInputs):
    pass


class DummyModel(Model):
    """The dummy base model."""

    def __init__(self, params, inits):
        self.config = DummyConfig(params)
        self.state = DummyState(inits)
        self.inputs = DummyInputs()

    def step(self):
        self.state.p_kw = self.inputs.p_set_kw
        self.state.q_kvar = self.inputs.q_set_kvar
        if self.state.p_kw is None:
            self.state.p_kw = 0.0
        if self.state.q_kvar is None:
            self.state.q_kvar = 0.0

    def get_pn_max_kw(self):
        return self.config.p_max_kw

    def get_pn_min_kw(self):
        return self.config.p_min_kw

    def get_qn_max_kvar(self):
        return self.config.q_max_kvar

    def get_qn_min_kvar(self):
        return self.config.q_min_kvar

    def set_p_kw(self, p_kw: float) -> None:
        self.inputs.p_set_kw = p_kw

    def get_p_kw(self):
        return self.state.p_kw

    def set_q_kvar(self, q_kvar: float) -> None:
        self.inputs.q_set_kvar = q_kvar

    def get_q_kvar(self):
        return self.state.q_kvar

    # def set_percent(self, percentage):
    #     self.inputs.p_set_kw = (
    #         self.config.p_min_kw
    #         + percentage * (self.config.p_max_kw -
    # self.config.p_min_kw) / 100
    #     )

    # def get_percent_in(self) -> float:
    #     raise NotImplementedError()

    def get_percent_out(self) -> float:
        raise NotImplementedError()
