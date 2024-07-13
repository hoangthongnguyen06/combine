from flask import Blueprint, request, jsonify
# from app.services.topic import update_topics_from_api, create_topic, update_topic, delete_topic, get_topic, get_all_topics
from app.services.topic import update_topics_from_api

bp_topics = Blueprint('topics', __name__)

@bp_topics.route('/update', methods=['POST'])
def update_topics_route():
    api_url = request.json['api_url']
    headers = request.json.get('headers')
    update_topics_from_api(api_url, headers)
    return jsonify({'message': 'Topics updated successfully'})

@bp_topics.route('/', methods=['POST'])
def create_topic_route():
    data = request.json
    topic = create_topic(data)
    return jsonify(topic.serialize())

@bp_topics.route('/<int:id>', methods=['PUT'])
def update_topic_route(id):
    data = request.json
    topic = update_topic(id, data)
    if topic:
        return jsonify(topic.serialize())
    return jsonify({'message': 'Topic not found'})

@bp_topics.route('/<int:id>', methods=['DELETE'])
def delete_topic_route(id):
    success = delete_topic(id)
    if success:
        return jsonify({'message': 'Topic deleted successfully'})
    return jsonify({'message': 'Topic not found'})

@bp_topics.route('/<int:id>', methods=['GET'])
def get_topic_route(id):
    topic = get_topic(id)
    if topic:
        return jsonify(topic.serialize())
    return jsonify({'message': 'Topic not found'})

@bp_topics.route('/', methods=['GET'])
def get_all_topics_route():
    topics = get_all_topics()
    return jsonify([topic.serialize() for topic in topics])
