import requests
from app.models import Post
from app import db

def update_posts_from_api(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        posts_data = response.json()
        for post_data in posts_data:
            post = Post.query.filter_by(id=post_data['id']).first()
            if post:
                post.update(**post_data)
            else:
                Post.create(**post_data)
    else:
        print(f"Failed to fetch posts: {response.status_code}")

def create_post(data):
    post = Post.create(**data)
    return post

def update_post(id, data):
    post = Post.query.get(id)
    if post:
        post.update(**data)
        return post
    return None

def delete_post(id):
    post = Post.query.get(id)
    if post:
        post.delete()
        return True
    return False

def get_post(id):
    return Post.query.get(id)

def get_all_posts():
    return Post.query.all()
