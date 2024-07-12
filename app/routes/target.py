from flask import Blueprint, request, jsonify
from app.services.target import update_targets_from_api, create_target, update_target, delete_target, get_target, get_all_targets

bp_targets = Blueprint('targets', __name__)

@bp_targets.route('/update', methods=['POST'])
def update_targets_route():
    api_url = request.json['api_url']
    headers = request.json.get('headers')
    update_targets_from_api(api_url, headers)
    return jsonify({'message': 'Targets updated successfully'})

@bp_targets.route('/', methods=['POST'])
def create_target_route():
    data = request.json
    target = create_target(data)
    return jsonify(target.serialize())

@bp_targets.route('/<int:id>', methods=['PUT'])
def update_target_route(id):
    data = request.json
    target = update_target(id, data)
    if target:
        return jsonify(target.serialize())
    return jsonify({'message': 'Target not found'})

@bp_targets.route('/<int:id>', methods=['DELETE'])
def delete_target_route(id):
    success = delete_target(id)
    if success:
        return jsonify({'message': 'Target deleted successfully'})
    return jsonify({'message': 'Target not found'})

@bp_targets.route('/<int:id>', methods=['GET'])
def get_target_route(id):
    target = get_target(id)
    if target:
        return jsonify(target.serialize())
    return jsonify({'message': 'Target not found'})

@bp_targets.route('/', methods=['GET'])
def get_all_targets_route():
    targets = get_all_targets()
    return jsonify([target.serialize() for target in targets])
