from flask import Blueprint, request, jsonify
from app.services.post import update_posts_from_api, create_post, update_post, delete_post, get_post, get_all_posts

bp_posts = Blueprint('posts', __name__)

@bp_posts.route('/update', methods=['POST'])
def update_posts_route():
    api_url = request.json['api_url']
    headers = request.json.get('headers')
    update_posts_from_api(api_url, headers)
    return jsonify({'message': 'Posts updated successfully'})

@bp_posts.route('/', methods=['POST'])
def create_post_route():
    data = request.json
    post = create_post(data)
    return jsonify(post.serialize())

@bp_posts.route('/<int:id>', methods=['PUT'])
def update_post_route(id):
    data = request.json
    post = update_post(id, data)
    if post:
        return jsonify(post.serialize())
    return jsonify({'message': 'Post not found'})

@bp_posts.route('/<int:id>', methods=['DELETE'])
def delete_post_route(id):
    success = delete_post(id)
    if success:
        return jsonify({'message': 'Post deleted successfully'})
    return jsonify({'message': 'Post not found'})

@bp_posts.route('/<int:id>', methods=['GET'])
def get_post_route(id):
    post = get_post(id)
    if post:
        return jsonify(post.serialize())
    return jsonify({'message': 'Post not found'})

@bp_posts.route('/', methods=['GET'])
def get_all_posts_route():
    posts = get_all_posts()
    return jsonify([post.serialize() for post in posts])
