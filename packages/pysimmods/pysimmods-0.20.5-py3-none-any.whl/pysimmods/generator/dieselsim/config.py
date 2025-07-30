from typing import List

from pysimmods.model.config import ModelConfig

DEFAULT_SCHEDULE: List[float] = (
    [50, 50, 50, 50, 50, 100, 100, 100]
    + [100, 50, 50, 50, 100, 100, 50, 50]
    + [50, 100, 100, 100, 100, 50, 50, 50]
)


class DieselGenConfig(ModelConfig):
    def __init__(self, params):
        super().__init__(params)

        self.p_max_kw = params["p_max_kw"]
        self.p_min_kw = 0.1 * params["p_max_kw"]
        self.q_max_kvar = params["q_max_kvar"]
        self.q_min_kvar = params["q_min_kvar"]

        self.default_p_schedule: List[float] = [
            self.p_min_kw + dv * self.p_max_kw / 100 for dv in DEFAULT_SCHEDULE
        ]
        self.default_q_schedule: List[float] = [0.0] * 24

    # @property
    # def p_max_kw(self):
    #     if self.psc:
    #         return self._p_min_kw * self.gsign
    #     else:
    #         return self._p_max_kw * self.gsign

    # @property
    # def p_min_kw(self):
    #     if self.psc:
    #         return self._p_max_kw * self.gsign
    #     else:
    #         return self._p_min_kw * self.gsign

    # @property
    # def q_max_kvar(self):
    #     return self._q_max_kvar

    # @property
    # def q_min_kvar(self):
    #     return self._q_min_kvar
