from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def execute_random_number_generator(num_bits):
    qc = QuantumCircuit(num_bits, num_bits)

    qc.h(range(num_bits))

    qc.measure(range(num_bits), range(num_bits))

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1)

    result = job.result()
    counts = result.get_counts()

    random_bitstring = list(counts.keys())[0]

    return random_bitstring, qc.draw()
