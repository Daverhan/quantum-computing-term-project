from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def create_simon_oracle(num_qubits, function_values):
    oracle = QuantumCircuit(num_qubits * 2)
    for input_str, output_str in function_values.items():
        for qubit in range(num_qubits):
            if input_str[qubit] == '0':
                oracle.x(qubit)
        for qubit in range(num_qubits):
            if output_str[qubit] == '1':
                oracle.cx(qubit, qubit + num_qubits)
        for qubit in range(num_qubits):
            if input_str[qubit] == '0':
                oracle.x(qubit)
    return oracle


def binary_string_to_list(s):
    return [int(bit) for bit in s]


def xor_lists(list1, list2):
    return [list1[i] ^ list2[i] for i in range(len(list1))]


def execute_simons(num_qubits, function_values):
    qc = QuantumCircuit(2 * num_qubits, num_qubits)
    oracle = create_simon_oracle(num_qubits, function_values)
    
    qc.h(range(num_qubits))

    qc.barrier()
    
    qc.h(range(num_qubits))

    qc.append(oracle, range(num_qubits * 2))

    qc.barrier()
    
    qc.h(range(num_qubits))
    
    qc.measure(range(num_qubits), range(num_qubits))
    
    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024)

    result = job.result()
    counts = result.get_counts()

    measurement_results = list(counts.keys())

    equations = [binary_string_to_list(result) for result in measurement_results]

    input_output_map = {}
    for key in measurement_results:
        if key in function_values:
            input_output_map[key] = function_values[key]

    pairs = {}
    for key, value in input_output_map.items():
        if value in pairs:
            pairs[value].append(key)
        else:
            pairs[value] = [key]

    result = None
    for output, inputs in pairs.items():
        if len(inputs) == 2:
            x1 = binary_string_to_list(inputs[0])
            x2 = binary_string_to_list(inputs[1])
            result = xor_lists(x1, x2)
            break

    if result is None:
        return "not obtainable from this data", qc.draw()

    hidden_string = ''.join(map(str, result))
    return hidden_string, qc.draw()


