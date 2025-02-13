from flask import Blueprint, request, jsonify
from app.quantum_algorithms.bernstein_vazirani import execute_bernstein_vazirani
from app.quantum_algorithms.deutsch_jozsa import execute_deutsch_jozsa
from app.quantum_algorithms.simons import execute_simons
from app.quantum_algorithms.quantum_fourier_transform import execute_quantum_fourier_transform
from app.quantum_algorithms.random_number_generator import execute_random_number_generator

algorithms_bp = Blueprint('algorithms', __name__)


@algorithms_bp.route('/deutsch-jozsa', methods=['POST'])
def deutsch_jozsa():
    request_json = request.get_json()

    num_qubits = int(request_json.get('numQubits'))
    boolean_function_inputs = request_json.get('booleanFunctionInputs')
    string = ''.join(boolean_function_inputs.values())

    if not num_qubits:
        return jsonify({'error': 'The number of qubits was not found in the request'}), 400

    constant_or_balanced, quantum_circuit = execute_deutsch_jozsa(num_qubits, string)

    return jsonify({'result': constant_or_balanced, 'circuit': str(quantum_circuit)}), 200


@algorithms_bp.route('/simons', methods=['POST'])
def simons():
    request_json = request.get_json()

    num_qubits = int(request_json.get('numQubits'))
    boolean_function_inputs = request_json.get('booleanFunctionInputs')
    function_values = {key.replace("input_", ""): value for key, value in boolean_function_inputs.items()}

    if not num_qubits:
        return jsonify({'error': 'The number of qubits was not found in the request'}), 400

    hidden_string, quantum_circuit = execute_simons(num_qubits, function_values)

    return jsonify({'result': hidden_string, 'circuit': str(quantum_circuit)}), 200


@algorithms_bp.route('/quantum-fourier-transform', methods=['POST'])
def quantum_fourier_transform():
    request_json = request.get_json()

    bitstring = request_json.get('bitstring')

    if not bitstring:
        return jsonify({'error': 'The bitstring was not found in the request'}), 400

    probabilities, quantum_circuit = execute_quantum_fourier_transform(bitstring)

    return jsonify({'probabilities': probabilities, 'circuit': str(quantum_circuit)}), 200


@algorithms_bp.route('/bernstein-vazirani', methods=['POST'])
def bernstein_vazirani():
    request_json = request.get_json()

    secret_bitstring = request_json.get('secret_bitstring')

    if not secret_bitstring:
        return jsonify({'error': 'The bitstring was not found in the request'}), 400

    secret_bitstring, quantum_circuit = execute_bernstein_vazirani(
        secret_bitstring)

    return jsonify({'result': f'{secret_bitstring}', 'circuit': str(quantum_circuit)}), 200


@algorithms_bp.route('/random-number-generator', methods=['POST'])
def random_number_generator():
    request_json = request.get_json()

    num_bits = request_json.get('numBits')

    if not num_bits:
        return jsonify({'error': 'The number of bits was not found in the request'}), 400

    random_bitstring, quantum_circuit = execute_random_number_generator(num_bits)

    return jsonify({'result': int(random_bitstring, 2), 'circuit': str(quantum_circuit)}), 200
