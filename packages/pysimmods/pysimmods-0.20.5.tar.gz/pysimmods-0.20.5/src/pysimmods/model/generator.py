from typing import Optional

from .model import Model


class Generator(Model):
    """A generator subtype model.

    A generator returns negative power values in the
    consumer reference arrow system.

    """

    def set_p_kw(self, p_kw: Optional[float]) -> None:
        if p_kw is not None:
            self.inputs.p_set_kw = abs(p_kw)
        else:
            self.inputs.p_set_kw = None

    def get_p_kw(self) -> float:
        return self.state.p_kw * self.config.gsign

    def get_qn_min_kvar(self) -> float:
        return 0

    def get_qn_max_kvar(self) -> float:
        return 0
