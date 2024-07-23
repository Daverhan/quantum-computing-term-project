from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def execute_bernstein_vazirani(secret_bitstring):
    qc = QuantumCircuit(len(secret_bitstring) +
                        1, len(secret_bitstring))

    numbers = [i for i in range(len(secret_bitstring))]

    qc.h(numbers)
    qc.x(len(secret_bitstring))
    qc.h(len(secret_bitstring))

    qc.barrier()

    for index, bit in enumerate(secret_bitstring):
        if bit == '1':
            qc.cx(len(secret_bitstring) - 1 -
                  index, len(secret_bitstring))

    qc.barrier()

    qc.h(numbers)

    qc.barrier()

    qc.measure(numbers, numbers)

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1)

    result = job.result()
    counts = result.get_counts()

    for key in counts.keys():
        secret_string = key

    return secret_string, qc.draw()
