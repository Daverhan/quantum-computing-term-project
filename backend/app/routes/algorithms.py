from flask import Blueprint, request, jsonify
from app.quantum_algorithms.bernstein_vazirani import execute_bernstein_vazirani

algorithms_bp = Blueprint('algorithms', __name__)


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
