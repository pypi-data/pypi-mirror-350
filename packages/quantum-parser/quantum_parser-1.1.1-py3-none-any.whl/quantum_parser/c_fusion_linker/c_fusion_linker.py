from c_fusion import CFusion

from quantum_parser.qcis_parser import QcisParser


class CFusionLinker:
    def __init__(self, qcis: str, shots: int = 1024, **kw) -> None:

        self.qcis = qcis
        self.shots = shots
        self.kw = {k: v for k, v in kw.items() if k != "shots"}  # except for shots

        self.parser = QcisParser(self.qcis)
        self.simulator = CFusion(self.parser.nq)

        self._state = None
        self._probs = None
        self._measure = None
        self._sample = None
        self._pre_run()

    def _pre_run(self) -> None:

        qmap = self.parser.qmap
        tokens = self.parser.tokens
        mq = self.parser.mq

        for line in tokens:
            # fmt: off
            if line[0] in ["H", "X", "Y", "Z", "S", "SD", "T", "TD", "X2M", "X2P", "Y2M", "Y2P"]:
            # fmt: on
                getattr(self.simulator, line[0])(qmap[line[1]])
            elif line[0] in ["CX", "CY", "CZ"]:
                getattr(self.simulator, line[0])(qmap[line[1]], qmap[line[2]])
            elif line[0] in ["RX", "RY", "RZ"]:
                getattr(self.simulator, line[0])(qmap[line[1]], line[2])
            elif line[0] in ["U3"]:
                getattr(self.simulator, line[0])(qmap[line[1]], line[2], line[3], line[4])
            elif line[0] in ["M", "I", "B"]:
                 pass
            else:
                raise ValueError(f"Not support gete {line[0]}.")

        self._state = self.simulator.state()
        self._probs = self.simulator.probs()
        self._measure = self.simulator.measure([qmap[i] for i in mq])
        self._sample = self.simulator.sample(
            [qmap[i] for i in mq], shots=self.shots, **self.kw
        )

    @property
    def state(self):
        return self._state

    @property
    def probs(self):
        return self._probs

    @property
    def measure(self):
        return self._measure

    @property
    def sample(self):
        return self._sample
