from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_service import update_targets_from_api, update_posts_from_api, update_topics_from_api, update_objects_from_api, update_results_from_api

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_targets_from_api, trigger="interval", minutes=30, args=("https://api.example.com/targets", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_posts_from_api, trigger="interval", minutes=30, args=("https://api.example.com/posts", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_topics_from_api, trigger="interval", minutes=30, args=("https://api.example.com/topics", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_objects_from_api, trigger="interval", minutes=30, args=("https://api.example.com/objects", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_results_from_api, trigger="interval", minutes=30, args=("https://api.example.com/results", {"Authorization": "Bearer token"}))
    scheduler.start()
