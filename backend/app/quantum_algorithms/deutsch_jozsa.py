from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def execute_deutsch_jozsa(num_qubits, boolean_function_inputs):
    print(num_qubits)
    print(boolean_function_inputs)
