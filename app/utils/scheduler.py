import requests
from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.target import update_targets_from_api
# from app.services.post import update_posts_from_api
# from app.services.topic import update_topics_from_api
# from app.services.topic_new import update_topics_new_from_api
from app.services.tinhthanh_ngay import update_location_post_counts_from_api
from app.services.target import fetch_and_update_data_target
from app.services.topic_day import update_sentiment_topic_from_api
from app.services.bot import fetch_and_update_bot_data
from app.services.serverCT import update_server_status
from app.services.muctieubaove_ngay import update_sentiment_target_from_api
from app import config, endpoints
import requests
from urllib3.exceptions import InsecureRequestWarning

# from app.services.post import update_posts_from_api   

# Bỏ qua cảnh báo không xác minh yêu cầu không an toàn
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_access_token(username, password, system):
    if system == "platform":
        login_url = endpoints.APIPlatformEndpoints.LOGIN.value
        print(login_url)
        login_data = {
            'username': username,
            'password': password,
        }
        print(login_data)
        response = requests.post(login_url, json=login_data, verify=False)
        print(response.json())
        if response.status_code == 200:
            access_token = response.json().get('data', {}).get('data', {}).get('token')
            #access_token = "eyJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25faWQiOjYzMCwidmlldHRlbC5wbGEudG9rZW4uaXMuZmlyc3QubG9naW4iOmZhbHNlLCJzdWIiOiJCVEw4Nl9UVERIOzYzMCIsImV4cCI6MTcyNTAzOTIzOSwiaWF0IjoxNzI0NDM0NDM5fQ.zDr6f5f6Y24KwNx4tKc1Qkbl2YPHK-Fv14a19ZxaN8vh7AxxYof56JR6zm1ruDHoJu2QLl5_Y8wBoDBIK001lQ"
            print("Platform: Successfully obtained access token.")
            print(access_token)
            return access_token
        else:
            print(
                f"Platform: Failed to obtain access token. Status code: {response.status_code}")
            return None
    elif system == "spyder":
        login_url = endpoints.APISpyderEndpoints.LOGIN.value
        login_data = {
            'username': username,
            'password': password,
        }
        response = requests.post(login_url, json=login_data, verify=False)

        if response.status_code == 200:
            access_token = response.json().get('result', {}).get('access_token')
            print("Spyder: Successfully obtained access token.")
            return access_token
        else:
            print(
                f"Spyder: Failed to obtain access token. Status code: {response.status_code}")
            return None
    return None


def start_scheduler(app):
    scheduler = BackgroundScheduler()

    with app.app_context():
        # Get access token
        access_token_platform = get_access_token(
            config.Config.USERNAME_PLATFORM, config.Config.PASSWORD_PLATFORM, "platform")
        print(access_token_platform)
        access_token_spyder = get_access_token(
            config.Config.USERNAME_SPYDER, config.Config.PASSWORD_SPYDER, "spyder")
        print(access_token_spyder)
        # if not access_token_spyder or not access_token_platform:
        if not access_token_platform:
            print("Failed to start scheduler. Could not obtain access token.")
            return
        # access_token_spyder = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc3QTVCRDZERDBDNTkyODA4QkYzRTQzODZGNTEzRDhEIiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwOi8vMTAuOS4xLjE1MTozMTI1OCIsIm5iZiI6MTcyMjY3MDg4MywiaWF0IjoxNzIyNjcwODgzLCJleHAiOjE3MjMyNzU2ODMsImF1ZCI6IkFkbWluQ2xpZW50SWRfYXBpIiwic2NvcGUiOlsiQWRtaW5DbGllbnRJZF9hcGkiLCJyb2xlcyIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiQWRtaW5DbGllbnRJZCIsInN1YiI6ImU4YjdkMGE5LWY5ZTgtNGIxYi1iZTM2LTJiZWYwODA1ZDVlZSIsImF1dGhfdGltZSI6MTcyMjY3MDg4MywiaWRwIjoibG9jYWwiLCJuYW1lIjoiYWRtaW44NiJ9.KTCrZkrHh6HBgFUeswOlNBA-f0qfdYTCcQ4K0OHGxyWB0UeD6Xgi-G1Xo1mb84P_nAflE63T43mZKSuYkqQBLEdokpwyRrZUeK-22nbKrw7QT3w5Ft9KYpTpbAzfspiePIBPR9M3AVB-4KLjPMA20_ttUwEyqF9BGUN6FZckE2GaVAbuZkbXDjd2PTu-b97A6JijwOWgHe0P4to9l4huHaIVd1UbCHvEvOo_58AemFvqr0C4mnehgkAcG4LumTunQcHoCQqUn4gr8Hc71vtaHcWwXQ-kWxRJqHzD1JyFrf6xwxTns6BSt03MYC9STFaBYvLXbI6UuqPb-yxXb5hXig"
        headers_platform = {"Authorization": f"Bearer {access_token_platform}"}
        headers_spyder = {"Authorization": f"Bearer {access_token_spyder}"}
        # # Schedule jobs with updated functions
        try:
            # scheduler.add_job(func=update_topics_from_api, trigger="interval", minutes=0.5, args=(
            #     endpoints.APIPlatformEndpoints.GET_TOPIC.value, headers, app))
            # # scheduler.add_job(func=update_posts_from_api, trigger="interval", minutes=0.5, args=(
            # #     endpoints.APIPlatformEndpoints.POST.value, headers_platform, headers_spyder, app))
            # scheduler.add_job(func=update_topics_new_from_api, trigger="interval", minutes=5, args=(
            #     endpoints.APIPlatformEndpoints.GET_TOPIC.value, headers_platform, app))
            scheduler.add_job(func=update_sentiment_topic_from_api, trigger="interval", minutes=5, args=(
                endpoints.APIPlatformEndpoints.SAC_THAI_THEO_CHU_DE.value, endpoints.APIPlatformEndpoints.LUOT_TUONG_TAC_THEO_CHU_DE.value, headers_platform, app))
            scheduler.add_job(func=update_sentiment_target_from_api, trigger="interval", minutes=5, args=(
                endpoints.APIPlatformEndpoints.SAC_THAI_THEO_CHU_DE.value, endpoints.APIPlatformEndpoints.LUOT_TUONG_TAC_THEO_CHU_DE.value, headers_platform, app))
            scheduler.add_job(func=update_sentiment_topic_from_api, trigger="interval", minutes=5, args=(
                endpoints.APISpyderEndpoints.SAC_THAI_THEO_CHU_DE.value, None, headers_spyder, app))
            scheduler.add_job(func=fetch_and_update_data_target, trigger="interval", minutes=1, args=(app,))
            scheduler.add_job(func=fetch_and_update_bot_data, trigger="interval", minutes=1, args=(app,))
            scheduler.add_job(func=update_server_status, trigger="interval", minutes=1, args=(app,))
            scheduler.add_job(func=update_location_post_counts_from_api, trigger="interval", minutes=5, args=(
                endpoints.APIPlatformEndpoints.GET_POST_NUMBER_WITH_LOCATION.value, headers_platform, app))
            scheduler.start()
            print("Scheduler started successfully.")
        except Exception as e:
            print(f"Error starting scheduler: {e}")
