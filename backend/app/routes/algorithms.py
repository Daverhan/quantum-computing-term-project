from flask import Blueprint, request, jsonify
from app.quantum_algorithms.bernstein_vazirani import execute_bernstein_vazirani
from app.quantum_algorithms.deutsch_jozsa import execute_deutsch_jozsa
from app.quantum_algorithms.simons import execute_simons
from app.quantum_algorithms.quantum_fourier_transform import execute_quantum_fourier_transform

algorithms_bp = Blueprint('algorithms', __name__)


@algorithms_bp.route('/deutsch-jozsa', methods=['POST'])
def deutsch_jozsa():
    request_json = request.get_json()

    num_qubits = request_json.get('numQubits')
    boolean_function_inputs = request_json.get('booleanFunctionInputs')

    if not num_qubits:
        return jsonify({'error': 'The number of qubits was not found in the request'}), 400

    execute_deutsch_jozsa(num_qubits, boolean_function_inputs)

    return jsonify({'result': 'constant'}), 200


@algorithms_bp.route('/simons', methods=['POST'])
def simons():
    request_json = request.get_json()

    num_qubits = request_json.get('numQubits')
    boolean_function_inputs = request_json.get('booleanFunctionInputs')

    if not num_qubits:
        return jsonify({'error': 'The number of qubits was not found in the request'}), 400

    execute_simons(num_qubits, boolean_function_inputs)

    return jsonify({'result': 'N/A'}), 200


@algorithms_bp.route('/quantum-fourier-transform', methods=['POST'])
def quantum_fourier_transform():
    request_json = request.get_json()

    bitstring = request_json.get('bitstring')

    if not bitstring:
        return jsonify({'error': 'The bitstring was not found in the request'}), 400

    execute_quantum_fourier_transform(bitstring)

    return jsonify({'result': 'N/A'}), 200


@algorithms_bp.route('/bernstein-vazirani', methods=['POST'])
def bernstein_vazirani():
    request_json = request.get_json()

    secret_bitstring = request_json.get('bitstring')

    if not secret_bitstring:
        return jsonify({'error': 'The bitstring was not found in the request'}), 400

    secret_bitstring, quantum_circuit = execute_bernstein_vazirani(
        secret_bitstring)

    print(quantum_circuit)

    return jsonify({'result': f'{secret_bitstring}'}), 200
