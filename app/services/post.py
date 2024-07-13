import requests
from app.models import Post
from app import db
from datetime import datetime

payload = {
    "trends": [],
    "keywords": [],
    "sources": [
        1,
        2,
        4,
        5,
        8,
        9,
        12
    ],
    "sentiments": [],
    "domains": [],
    "author_names": [],
    "author_ids": [],
    "wall_ids": [],
    "article_types": [],
    "date_from": "2024/07/13 00:00:00",
    "date_to": "2024/07/13 23:59:59",
    "pinned": "null",
    "get_snippet": "true",
    "order": 3,
    "similar_master": 0,
    "is_spam": "false",
    "flow_ids": [],
    "topic_ids": [],
    "profile_group_id": "null",
    "page": 0,
    "size": 5000
}


def update_posts_from_api(api_url, headers=None, app=None):
    with app.app_context():
        response = requests.post(api_url, json=payload,
                                 headers=headers, verify=False)
        if response.status_code == 200:
            api_data = response.json()
            print(api_data)
            for hit in api_data["data"]["hits"]:
                post_data = {
                    "id": hit["id"],
                    "account_id": hit["author_id"],
                    "content": hit["content"],
                    "likes": hit["like_count"],
                    "comments": hit["comment_count"],
                    "shares": hit["share_count"],
                    "domain": hit["domain"],
                    "link": hit["url"],
                    "type": hit["article_type"],
                    "description": hit["description"],
                }
                # Xử lý sắc thái
                if hit.get('sentiment') == -1:
                    post_data["nuance"] = 'Tiêu cực'
                elif hit.get('sentiment') == 0:
                    post_data["nuance"] = 'Trung tính'
                elif hit.get('sentiment') == 1:
                    post_data["nuance"] = 'Tích cực'
                # Xử lý hashtag
                if hit.get('keywords'):
                    post_data["hashtag"] = ', '.join(hit.get('keywords'))
                # Xử lý
                if hit.get('published_timestamp'):
                    dt_object = datetime.fromtimestamp(
                        hit['published_timestamp'] / 1000.0)
                    post_data['date'] = dt_object.strftime("%Y/%m/%d %H:%M:%S")
                top = Post.query.filter_by(id=post_data['id']).first()
                if top:
                    for key, value in post_data.items():
                        setattr(top, key, value)
                    db.session.commit()
                else:
                    new_obj = Post(**post_data)
                    db.session.add(new_obj)
                    db.session.commit()
        else:
            print(f"Failed to fetch posts: {response.status_code}")


# def create_post(data):
#     post = Post.create(**data)
#     return post


# def update_post(id, data):
#     post = Post.query.get(id)
#     if post:
#         post.update(**data)
#         return post
#     return None


# def delete_post(id):
#     post = Post.query.get(id)
#     if post:
#         post.delete()
#         return True
#     return False


# def get_post(id):
#     return Post.query.get(id)


# def get_all_posts():
#     return Post.query.all()
