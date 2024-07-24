from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def create_oracle(num_qubits, function_values):
    oracle = QuantumCircuit(num_qubits + 1)
    for i, value in enumerate(function_values):
        if value == '1':
            binary_index = format(i, f'0{num_qubits}b')
            for j, bit in enumerate(binary_index):
                if bit == '0':
                    oracle.x(j)
            oracle.mcx(list(range(num_qubits)), num_qubits)
            for j, bit in enumerate(binary_index):
                if bit == '0':
                    oracle.x(j)
    return oracle

def execute_deutsch_jozsa(num_qubits, string):
    oracle = create_oracle(num_qubits, string)
    qc = QuantumCircuit(num_qubits + 1, num_qubits)

    qc.h(range(num_qubits))

    qc.x(num_qubits)
    qc.h(num_qubits)

    qc.barrier()

    qc.append(oracle, range(num_qubits + 1))

    qc.barrier()

    qc.h(range(num_qubits))

    qc.barrier()

    qc.measure(range(num_qubits), range(num_qubits))

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()

    print(counts)
    if '0' * num_qubits in counts and counts['0' * num_qubits] == 1024:
        constant_or_balanced = 'constant'
    else:
        constant_or_balanced = 'balanced'

    return constant_or_balanced, qc.draw()
