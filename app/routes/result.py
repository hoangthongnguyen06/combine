from flask import Blueprint, request, jsonify
from app.services.result import update_results_from_api, create_result, update_result, delete_result, get_result, get_all_results

bp_results = Blueprint('results', __name__)

@bp_results.route('/update', methods=['POST'])
def update_results_route():
    api_url = request.json['api_url']
    headers = request.json.get('headers')
    update_results_from_api(api_url, headers)
    return jsonify({'message': 'Results updated successfully'})

@bp_results.route('/', methods=['POST'])
def create_result_route():
    data = request.json
    result = create_result(data)
    return jsonify(result.serialize())

@bp_results.route('/<int:id>', methods=['PUT'])
def update_result_route(id):
    data = request.json
    result = update_result(id, data)
    if result:
        return jsonify(result.serialize())
    return jsonify({'message': 'Result not found'})

@bp_results.route('/<int:id>', methods=['DELETE'])
def delete_result_route(id):
    success = delete_result(id)
    if success:
        return jsonify({'message': 'Result deleted successfully'})
    return jsonify({'message': 'Result not found'})

@bp_results.route('/<int:id>', methods=['GET'])
def get_result_route(id):
    result = get_result(id)
    if result:
        return jsonify(result.serialize())
    return jsonify({'message': 'Result not found'})

@bp_results.route('/', methods=['GET'])
def get_all_results_route():
    results = get_all_results()
    return jsonify([result.serialize() for result in results])
