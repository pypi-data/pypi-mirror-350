from pysimmods.model.model import Model


class Consumer(Model):
    """A consumer subtype model.

    This class provides unified access to set_percent for all
     generators. A generator returns negative power values in the
     consumer reference arrow system (passive sign convention), which
     is hided if one uses *set_percent*, i.e. calling set_percent
     with, e.g., a value of 50 will always set the power of the
     generator to 50 percent, independently of the reference system
     used.

    """

    def set_p_kw(self, p_kw: float) -> None:
        if p_kw is not None:
            self.inputs.p_set_kw = abs(p_kw)
        else:
            self.inputs.p_set_kw = None

    def get_p_kw(self) -> float:
        return self.state.p_kw * self.config.lsign
