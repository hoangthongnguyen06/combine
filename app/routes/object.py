from flask import Blueprint, request, jsonify
from app.services.object import update_objects_from_api, create_object, update_object, delete_object, get_object, get_all_objects

bp_objects = Blueprint('objects', __name__)

@bp_objects.route('/update', methods=['POST'])
def update_objects_route():
    api_url = request.json['api_url']
    headers = request.json.get('headers')
    update_objects_from_api(api_url, headers)
    return jsonify({'message': 'Objects updated successfully'})

@bp_objects.route('/', methods=['POST'])
def create_object_route():
    data = request.json
    obj = create_object(data)
    return jsonify(obj.serialize())

@bp_objects.route('/<int:id>', methods=['PUT'])
def update_object_route(id):
    data = request.json
    obj = update_object(id, data)
    if obj:
        return jsonify(obj.serialize())
    return jsonify({'message': 'Object not found'})

@bp_objects.route('/<int:id>', methods=['DELETE'])
def delete_object_route(id):
    success = delete_object(id)
    if success:
        return jsonify({'message': 'Object deleted successfully'})
    return jsonify({'message': 'Object not found'})

@bp_objects.route('/<int:id>', methods=['GET'])
def get_object_route(id):
    obj = get_object(id)
    if obj:
        return jsonify(obj.serialize())
    return jsonify({'message': 'Object not found'})

@bp_objects.route('/', methods=['GET'])
def get_all_objects_route():
    objects = get_all_objects()
    return jsonify([obj.serialize() for obj in objects])
