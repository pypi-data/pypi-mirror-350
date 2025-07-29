"""
This module provides a class :class:`QcisParser` for parsing quantum control instruction set (QCIS).

QCIS is a representation of quantum circuits, specifying operations to be performed
on qubits using various quantum gates.

Examples:
    1. Simple gate operations:

    In this example, we demonstrate how to parse a simple QCIS string that includes a
    Hadamard gate on qubit Q0, a controlled-Z (CZ) gate between qubits Q0 and Q1,
    and a measurement operation on qubit Q0. The `QcisParser` class processes this
    input and outputs a list of tokens representing the parsed instructions.

    >>> from quantum_parser.qcis_parser import QcisParser
    >>> qcis = "H Q0\\nCZ Q0 Q1\\nM Q0"
    >>> parser = QcisParser(qcis)
    >>> print(parser.tokens)
    [['H', 0], ['CZ', 0, 1], ['M', 0]]

    2. Including rotation gates:

    This example illustrates the usage of rotation gates in the QCIS. The gates `RX`, `RY`,
    and `RZ` are applied to qubits Q0, Q1, and Q2 respectively, with specified rotation angles.
    Additionally, qubit Q1 is measured. The `QcisParser` parses these instructions, providing
    tokens that include the gate type, target qubit, and rotation angle.

    >>> qcis = "RX Q0 1.57\\nRY Q1 3.14\\nRZ Q2 0.78\\nM Q1"
    >>> parser = QcisParser(qcis)
    >>> print(parser.tokens)
    [['RX', 0, 1.57], ['RY', 1, 3.14], ['RZ', 2, 0.78], ['M', 1]]

    3. Topological checks enabled:

    Here, the `is_check_topo` parameter is set to True. This instructs the `QcisParser`
    to perform additional checks on the topology of the quantum circuit, such as verifying
    that the specified qubits exist and are correctly connected for two-qubit operations.
    Since the methods `check_topo_valid` and `check_topo_adj` are not implemented, setting
    `is_check_topo=True` will result in a `NotImplementedError`.

    >>> qcis = "H Q0\\nCZ Q1 Q2"
    >>> parser = QcisParser(qcis, is_check_topo=True)
    >>> # This will raise NotImplementedError because check_topo_valid and check_topo_adj are not implemented
    >>> print(parser.tokens)
    Traceback (most recent call last):
        ...
    NotImplementedError

Note:
    - The :class:`QcisParser` class currently does not implement the methods `check_topo_valid` and
      `check_topo_adj`, and these methods will raise ``NotImplementedError`` if invoked.
    - The parser is designed to be extended with additional gate types and validation logic.
"""

import re

TOKEN_REGEX = {
    # Single qubit gates and measurement
    # Matches gates: H, X, Y, Z, S, T, SD, TD, X2M, X2P, Y2M, Y2P
    # or measurement (M) applied to a single qubit.
    # Example: "H Q0" or "M Q1"
    "SINGLE": r"^\s*(?P<GATE>H|X|Y|Z|S|T|SD|TD|X2M|X2P|Y2M|Y2P|M)\s+Q(?P<INDEX>\d+)\s*$",
    # Two-qubit gates
    # Matches gates: CZ, CX, CY, CNOT applied to two qubits.
    # Example: "CX Q0 Q1"
    "DOUBLE": r"^\s*(?P<GATE>CZ|CX|CY|CNOT)\s+Q(?P<INDEX1>\d+)\s+Q(?P<INDEX2>\d+)\s*$",
    # Rotation gates
    # Matches rotation gates: RX, RY, RZ applied to a single qubit with a specified angle.
    # Example: "RX Q0 1.57"
    "ROTATION": r"^\s*(?P<GATE>RX|RY|RZ)\s+Q(?P<INDEX>\d+)\s+(?P<DEG>\S+)\s*$",
    # RXY gate
    # Matches the RXY gate applied to a single qubit with two specified angles.
    # Example: "RXY Q0 1.57 3.14"
    "RXY": r"^\s*(?P<GATE>RXY)\s+Q(?P<INDEX>\d+)\s+(?P<DEG1>\S+)\s+(?P<DEG2>\S+)\s*$",
    # U3 gate
    # Matches the U3 gate applied to a single qubit with three specified angles.
    # Example: "U3 Q0 0.5 1.0 1.5"
    "U3": r"^\s*(?P<GATE>U3)\s+Q(?P<INDEX>\d+)\s+(?P<DEG1>\S+)\s+(?P<DEG2>\S+)\s+(?P<DEG3>\S+)\s*$",
    # Example: "I Q0 10"
    "I": r"^\s*(?P<GATE>I)\s+Q(?P<INDEX>\d+)\s+(?P<TIME>\d+)\s*$",
    # Example: "B Q0 Q1"
    "B": r"^\s*(?P<GATE>B)\s+Q(?P<INDEX1>\d+)\s+Q(?P<INDEX2>\d+)\s*$",
    # Empty line
    # Matches an empty line or lines with only whitespace, which should be ignored.
    "EMPTY_LINE": r"^\s*$",
}


class QcisParser:
    """
    QcisParser is a class for parsing quantum control instruction set (QCIS) strings.

    This class provides functionalities to tokenize QCIS strings into a list of operations
    and map qubits, including optional topological validation checks.

    Attributes:
        _tokens (list): A list of parsed tokens representing the quantum instructions.
        _nq (int): The number of unique qubits used in the QCIS.
        _qmap (dict): A dictionary mapping qubit indices from the QCIS to internal indices.
        _mq (list): A list of qubits that are measured in the circuit.
    """

    def __init__(self, qcis: str, is_check_topo: bool = False, **kw) -> None:
        """
        Initializes the QcisParser with a QCIS string.

        Args:
            qcis (str): The quantum control instruction set string to be parsed.
            is_check_topo (bool): If True, enables topological checks for the quantum circuit.
                                  Default is False.
            **kw: Additional keyword arguments passed to the tokenization process.

        The constructor initializes the internal token list, qubit count, qubit map, and
        measurement list, and then tokenizes the provided QCIS string. The `is_check_topo`
        parameter controls whether topological validity checks are performed during tokenization.
        """
        self._tokens = []
        self._nq = 0
        self._qmap = {}
        self._mq = []
        self.tokenize(qcis, is_check_topo=is_check_topo, **kw)

    @property
    def tokens(self) -> list:
        return self._tokens

    @tokens.setter
    def tokens(self, *arg, **kw):
        raise AttributeError("Cannot modify `tokens`.")

    @property
    def nq(self) -> int:
        return self._nq

    @nq.setter
    def nq(self, *arg, **kw):
        raise AttributeError("Cannot modify `nq`.")

    @property
    def qmap(self) -> dict[int, int]:
        return self._qmap

    @qmap.setter
    def qmap(self, *arg, **kw):
        raise AttributeError("Cannot modify `qmap`.")

    @property
    def mq(self) -> list[int]:
        return self._mq

    @mq.setter
    def mq(self, *arg, **kw):
        raise AttributeError("Cannot modify `mq`.")

    @staticmethod
    def tokenize_line(line: str, line_num: int, **kw) -> list:
        """
        Tokenizes a single line of the QCIS string into a list of components.

        This method takes a line from the quantum control instruction set (QCIS) and
        parses it into a structured list representing the gate operation and its associated
        qubits and parameters. It supports single-qubit gates, two-qubit gates, rotation gates,
        and special gates like `I` and `B`.

        Args:
            line (str): A line from the QCIS string containing a quantum gate instruction.
            line_num (int): The line number of the QCIS string for error reporting.
            **kw: Additional keyword arguments for evaluating parameters, if needed.

        Returns:
            list: A list representing the parsed gate and its parameters. The structure of the list
                  depends on the type of gate (e.g., ['H', 0] for a Hadamard gate on Q0).

        Raises:
            ValueError: If the line contains a syntax error or an unsupported gate, a ValueError is raised
                        with a message indicating the line number and content.

        Examples:
            >>> QcisParser.tokenize_line("H Q0", 1)
            ['H', 0]

            >>> QcisParser.tokenize_line("CX Q0 Q1", 2)
            ['CX', 0, 1]

            >>> QcisParser.tokenize_line("RX Q0 1.57", 3)
            ['RX', 0, 1.57]

        Note:
            - The method uses regular expressions defined in `TOKEN_REGEX` to identify and extract
              the gate type and parameters from the input line.
            - The `**kw` arguments can be used for evaluating parameter values dynamically.
            - The method returns `None` for empty lines, which are ignored in the final token list.
        """
        token = []
        if match := re.match(TOKEN_REGEX["SINGLE"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX")))
        elif match := re.match(TOKEN_REGEX["DOUBLE"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX1")))
            token.append(int(match.group("INDEX2")))
        elif match := re.match(TOKEN_REGEX["ROTATION"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX")))
            token.append(eval(match.group("DEG"), kw))
        elif match := re.match(TOKEN_REGEX["RXY"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX")))
            token.append(eval(match.group("DEG1"), kw))
            token.append(eval(match.group("DEG2"), kw))
        elif match := re.match(TOKEN_REGEX["U3"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX")))
            token.append(eval(match.group("DEG1"), kw))
            token.append(eval(match.group("DEG2"), kw))
            token.append(eval(match.group("DEG3"), kw))
        elif match := re.match(TOKEN_REGEX["I"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX")))
            token.append(int(match.group("TIME")))
        elif match := re.match(TOKEN_REGEX["B"], line):
            token.append(match.group("GATE"))
            token.append(int(match.group("INDEX1")))
            token.append(int(match.group("INDEX2")))
        elif match := re.match(TOKEN_REGEX["EMPTY_LINE"], line):
            token = None
        else:
            raise ValueError(f"Syntax error in line {line_num}: '{line.strip()}'")
        return token

    @staticmethod
    def check_topo_valid(i: int):
        # TODO
        raise NotImplementedError

    @classmethod
    def check_topo_adj(cls, i: int, j: int):
        assert i != j
        cls.check_topo_valid(i)
        cls.check_topo_valid(j)
        i, j = min(i, j), max(i, j)
        # TODO
        raise NotImplementedError

    def check_mq(self) -> None:
        if self._mq:
            if sorted(set(self._mq)) != sorted(self._mq):
                raise ValueError(
                    "Repeated measurements of the same qubit are not supported."
                )
        else:
            self._mq = list(self.qmap.keys())

    def process_qmap(self, line_token: list, idx: int) -> None:
        if line_token[idx] not in self._qmap:
            self._qmap[line_token[idx]] = self._nq
            self._nq += 1

    def tokenize(self, qcis: str, is_check_topo: bool = False, **kw) -> None:
        """
        Parses the QCIS string into tokens and optionally performs topological checks.

        This method processes a quantum control instruction set (QCIS) string, tokenizing each line
        into a list of components representing the quantum gates and their associated qubits. It also
        updates internal mappings and lists to track qubits and measurements. If `is_check_topo` is
        set to True, the method performs additional topological checks on the qubits involved in the
        instructions.

        Args:
            qcis (str): The quantum control instruction set string to be parsed.
            is_check_topo (bool): If True, enables topological checks for the quantum circuit.
                                Default is False.
            **kw: Additional keyword arguments passed to the tokenization process, particularly
                useful for evaluating parameter expressions.

        Note:
            - The method iterates over each line of the QCIS string, parsing it into tokens.
            - For single-qubit gates and measurements, it updates the qubit map and measurement list.
            - For two-qubit gates, it validates adjacency if topological checks are enabled.
            - The `I` and `B` gates do not modify the qubit count or map.
            - If `is_check_topo` is True, the method calls `check_topo_valid` and `check_topo_adj`
              for topological validation, which currently raise `NotImplementedError`.
            - The method collects all tokens into `_tokens` and ensures that the measurement qubits
              are recorded in `_mq`.

        Example:
            >>> qcis = "H Q0\\nCX Q0 Q1\\nM Q0"
            >>> parser = QcisParser(qcis)
            >>> parser.tokenize(qcis)
            >>> print(parser._tokens)
            [['H', 0], ['CX', 0, 1], ['M', 0]]
        """
        for line_num, line in enumerate(qcis.split("\n")):
            line_token = self.tokenize_line(line, line_num + 1, **kw)
            if line_token is not None:
                if line_token[0] in ["H", "X", "Y", "Z", "S", "T", "SD", "TD", "X2M", "X2P", "Y2M",
                                    "Y2P", "RX", "RY", "RZ", "RXY", "U3", "M"]:  # fmt: skip
                    if is_check_topo:
                        self.check_topo_valid(line_token[1])
                    self.process_qmap(line_token, 1)
                    if line_token[0] == "M":
                        self._mq.append(line_token[1])
                elif line_token[0] in ["CX", "CY", "CZ", "CNOT"]:
                    if is_check_topo:
                        self.check_topo_adj(line_token[1], line_token[2])
                    self.process_qmap(line_token, 1)
                    self.process_qmap(line_token, 2)

                # Note: `I` and `B`gate should not affect qubit count and no qubits should be added
                # to the map.
                elif line_token[0] == "I":
                    if is_check_topo:
                        self.check_topo_valid(line_token[1])
                elif line_token[0] == "B":
                    if is_check_topo:
                        self.check_topo_adj(line_token[1], line_token[2])
                self._tokens.append(line_token)
        self.check_mq()
