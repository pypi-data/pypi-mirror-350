"""
QASM2Parser Module

This module provides the QASM2Parser class, which is designed to parse OpenQASM 2.0 code into
a tokenized format and extract information about the quantum circuit, such as the number of qubits and
the quantum operations performed. The class utilizes the Qiskit library to interpret and manipulate
quantum circuits.

Classes:
    :class:`QASM2Parser`: A class for parsing QASM 2.0 strings and tokenizing quantum operations.

Basic Examples:
    Parse a simple QASM string and retrieve tokens:

    >>> from qiskit import QuantumCircuit
    >>> from quantum_parser.qasm2_parser import QASM2Parser
    >>> qasm_code = '''
    ... OPENQASM 2.0;
    ... include "qelib1.inc";
    ... qreg q[2];
    ... h q[0];
    ... cx q[0], q[1];
    ... '''
    >>> parser = QASM2Parser(qasm_code)
    >>> print(parser.tokens)
    [['H', 0], ['CX', 0, 1]]

    Parse a nested circuit with a custom gate:

    >>> qasm_nested = '''
    ... OPENQASM 2.0;
    ... include "qelib1.inc";
    ... qreg q[2];
    ... gate custom_gate a, b {
    ...     h a;
    ...     cx a, b;
    ... }
    ... custom_gate q[0], q[1];
    ... '''
    >>> parser_nested = QASM2Parser(qasm_nested)
    >>> print(parser_nested.tokens)
    [['H', 0], ['CX', 0, 1]]

Note:
    - This parser currently does not support classical bit operations or measurement operations.
    - The tokens are provided in a simplified format and do not cover all possible gate parameters.
"""

import qiskit.qasm2
from qiskit import QuantumCircuit


class QASM2Parser:
    """
    A parser for OpenQASM 2.0 files that translates quantum assembly instructions into a list of tokens
    and provides information about the quantum circuit.

    Attributes:
        _tokens (list): Internal list of tokens representing the quantum instructions.
        qc (QuantumCircuit): The QuantumCircuit object generated from the QASM string.
        _nq (int): Number of qubits in the quantum circuit.
    """

    def __init__(self, qasm2: str) -> None:
        """
        Initialize the QASM2Parser with a QASM 2.0 string.

        Args:
            qasm2 (str): The QASM 2.0 string representing the quantum circuit.
        """
        self._tokens = []
        self.qc: QuantumCircuit = qiskit.qasm2.loads(qasm2)
        self._nq = self.qc.num_qubits
        # TODO: qmap
        # TODO: measure
        self.tokenize()

    def tokenize(
        self, qc: QuantumCircuit | None = None, qmap: list | None = None
    ) -> None:
        """
        Tokenize the quantum circuit instructions into a list of tokens.

        Args:
            qc (QuantumCircuit | None): The quantum circuit to tokenize. If None, uses the main circuit.
            qmap (list | None): Optional list mapping qubits for nested circuits. Defaults to None.

        Raises:
            Exception: If the circuit contains classical bits or measurement operations,
                       or if an instruction is applied without qubits.
        """
        if qc is None:
            qc = self.qc
        for cir_inst in qc:
            qubits = {qubit: i for i, qubit in enumerate(qc.qubits)}
            inst = cir_inst.operation
            if inst.name == "measure":
                raise Exception("Measure not supported yet.")
            # clbits is used for measure.
            if cir_inst.clbits:
                raise Exception("Classical bits not supported yet.")
            if not cir_inst.qubits:
                raise Exception("Cannot apply instruction without qubits.")
            if inst.name in ["h", "x", "y", "z", "s", "t", "sdg", "tdg", "cx", "cy", "cz", "rx",
                             "ry", "rz"]:  # fmt: skip
                gate_data = []
                if inst.name == "sdg":
                    gate_data.append("SD")
                elif inst.name == "tdg":
                    gate_data.append("TD")
                else:
                    gate_data.append(inst.name.upper())
                if qmap is None:
                    new_qmap = [qubits[tup] for tup in cir_inst.qubits]
                    gate_data.extend(new_qmap)
                else:
                    new_qmap = [qmap[qubits[tup]] for tup in cir_inst.qubits]
                    gate_data.extend(new_qmap)
                if inst.is_parameterized:
                    gate_data.extend(inst.params)
                self._tokens.append(gate_data)
            else:
                new_qmap = [qubits[tup] for tup in cir_inst.qubits]
                self.tokenize(inst.definition, new_qmap)

    @property
    def tokens(self) -> list:
        """
        Get the list of tokens representing the quantum instructions.

        Returns:
            list: A list of tokens where each token is a list containing the gate name and qubit indices.
        """
        return self._tokens

    @tokens.setter
    def tokens(self, *arg, **kw):
        """
        Prevent modification of the tokens property.

        Raises:
            AttributeError: Always raised to indicate tokens cannot be modified.
        """
        raise AttributeError("Cannot modify `tokens`.")

    @property
    def nq(self) -> int:
        """
        Get the number of qubits in the quantum circuit.

        Returns:
            int: The number of qubits.
        """
        return self._nq

    @nq.setter
    def nq(self, *arg, **kw):
        """
        Prevent modification of the nq property.

        Raises:
            AttributeError: Always raised to indicate nq cannot be modified.
        """
        raise AttributeError("Cannot modify `nq`.")
