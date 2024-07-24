from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


# WRONG! DO NOT BELIEVE ITS LIES.
def execute_deutsch_jozsa(num_qubits, boolean_function_inputs):
    qc = QuantumCircuit(num_qubits + 1, num_qubits)

    qc.h(range(num_qubits))

    qc.x(num_qubits)
    qc.h(num_qubits)

    qc.barrier()

    for i, bit in enumerate(boolean_function_inputs):
        if bit == '1':
            qc.cx(i, num_qubits)

    qc.barrier()

    qc.h(range(num_qubits))

    qc.barrier()

    qc.measure(range(num_qubits), range(num_qubits))

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts()

    print("Measurement results:", counts)

    constant_or_balanced = 'constant' if '0' * num_qubits in counts else 'balanced'

    circuit_diagram = qc.draw()
    
    return constant_or_balanced, circuit_diagram
