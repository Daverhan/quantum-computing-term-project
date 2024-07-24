from flask import Blueprint, request, jsonify
from app.quantum_algorithms.bernstein_vazirani import execute_bernstein_vazirani
from app.quantum_algorithms.deutsch_jozsa import execute_deutsch_jozsa
from app.quantum_algorithms.simons import execute_simons

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


@algorithms_bp.route('/bernstein-vazirani', methods=['POST'])
def bernstein_vazirani():
    request_json = request.get_json()

    secret_bitstring = request_json.get('secret_bitstring')

    if not secret_bitstring:
        return jsonify({'error': 'The secret bitstring was not found in the request'}), 400

    secret_bitstring, quantum_circuit = execute_bernstein_vazirani(
        secret_bitstring)

    print(f'The secret bitstring is {secret_bitstring}')
    print(quantum_circuit)

    return jsonify({'message': "Route successfully ran"}), 200
