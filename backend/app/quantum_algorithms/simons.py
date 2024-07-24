from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np


def execute_simons(num_qubits, string):
    qc = QuantumCircuit(2 * num_qubits, num_qubits)
    
    qc.h(range(num_qubits))

    qc.barrier()
    
    qc.h(range(num_qubits))

    for i, bit in enumerate(string):
        if bit == '1':
            qc.cx(i, i + num_qubits)

    qc.barrier()
    
    qc.h(range(num_qubits))
    
    qc.measure(range(num_qubits), range(num_qubits))
    

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024)

    result = job.result()
    counts = result.get_counts()
    
    return counts, qc.draw()
