from apscheduler.schedulers.background import BackgroundScheduler
from app.services.target import update_targets_from_api
from app.services.post import update_posts_from_api
from app.services.topic import update_topics_from_api
from app.services.object import update_objects_from_api
from app.services.result import update_results_from_api
from app import config

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_targets_from_api, trigger="interval", minutes=30, args=("https://api.example.com/targets", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_posts_from_api, trigger="interval", minutes=30, args=("https://api.example.com/posts", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_topics_from_api, trigger="interval", minutes=30, args=("https://"+config.Config.platformUrl+"/api/platform/topic/search", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_objects_from_api, trigger="interval", minutes=30, args=("https://api.example.com/objects", {"Authorization": "Bearer token"}))
    scheduler.add_job(func=update_results_from_api, trigger="interval", minutes=30, args=("https://api.example.com/results", {"Authorization": "Bearer token"}))
    scheduler.start()
