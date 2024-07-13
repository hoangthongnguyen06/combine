import requests
from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.target import update_targets_from_api
from app.services.post import update_posts_from_api
from app.services.topic import update_topics_from_api
# from app.services.object import update_objects_from_api
# from app.services.result import update_results_from_api
from app import config, endpoints
import requests
from app import create_app
import urllib3
import certifi
from urllib3.exceptions import InsecureRequestWarning
# from app.services.post import update_posts_from_api

# Bỏ qua cảnh báo không xác minh yêu cầu không an toàn
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_access_token(username, password):
    login_url = endpoints.APIPlatformEndpoints.LOGIN.value
    login_data = {
        'username': username,
        'password': password,
    }
    response = requests.post(login_url, json=login_data, verify=False)

    if response.status_code == 200:
        access_token = response.json().get('data', {}).get('data', {}).get('token')
        print("Successfully obtained access token.")
        return access_token
    else:
        print(
            f"Failed to obtain access token. Status code: {response.status_code}")
        return None


def start_scheduler(app):
    scheduler = BackgroundScheduler()

    with app.app_context():
        # Get access token
        access_token = get_access_token(
            config.Config.USERNAME_PLATFORM, config.Config.PASSWORD_PLATFORM)
        if not access_token:
            print("Failed to start scheduler. Could not obtain access token.")
            return

        headers = {"Authorization": f"Bearer {access_token}"}
        # Schedule jobs with updated functions
        try:
            # scheduler.add_job(func=update_topics_from_api, trigger="interval", minutes=0.5, args=(
            #     endpoints.APIPlatformEndpoints.GET_TOPIC.value, headers, app))
            scheduler.add_job(func=update_posts_from_api, trigger="interval", minutes=0.5, args=(
                endpoints.APIPlatformEndpoints.POST.value, headers, app))

            scheduler.start()
            print("Scheduler started successfully.")
        except Exception as e:
            print(f"Error starting scheduler: {e}")
