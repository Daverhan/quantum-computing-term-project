from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

def create_simon_oracle(num_qubits, hidden_string):
    oracle = QuantumCircuit(num_qubits)
    for qubit in range(num_qubits):
        if hidden_string[qubit] == '1':
            target_qubit = qubit + 1 % num_qubits
            if qubit != target_qubit:
                oracle.cx(qubit, target_qubit)
    return oracle


def execute_simons(num_qubits, string):
    qc = QuantumCircuit(2 * num_qubits, num_qubits)
    oracle = create_simon_oracle(num_qubits, string)
    
    qc.h(range(num_qubits))

    qc.barrier()
    
    qc.h(range(num_qubits))

    qc.append(oracle, range(num_qubits))

    qc.barrier()
    
    qc.h(range(num_qubits))
    
    qc.measure(range(num_qubits), range(num_qubits))
    

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024)

    result = job.result()
    counts = result.get_counts()

    hidden_string = max(counts, key=counts.get)
    
    return hidden_string, qc.draw()
