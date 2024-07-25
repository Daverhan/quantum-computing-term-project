from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

def qft(circuit, n):
    for qubit in range(n):
        circuit.h(qubit)
        for other_qubit in range(qubit + 1, n):
            angle = np.pi / (2 ** (other_qubit - qubit))
            circuit.cp(angle, other_qubit, qubit)
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)


def execute_quantum_fourier_transform(bitstring):
    num_qubits = len(bitstring)
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    for i, bit in enumerate(reversed(bitstring)):
        if bit == '1':
            qc.x(i)
    
    qft(qc, num_qubits)
    
    qc.measure(range(num_qubits), range(num_qubits))
    
    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024)

    result = job.result()
    counts = result.get_counts()
    
    new_bitstring = max(counts, key=counts.get)
    
    return new_bitstring, qc.draw()

