import requests
from app.endpoints import APIPlatformEndpoints
from app.config import Config


def login_to_api():
    login_url = APIPlatformEndpoints.LOGIN.value
    payload = {'username': Config.USERNAME_PLATFORM,
               'password': Config.PASSWORD_PLATFORM}

    # send to server to login
    response = requests.post(login_url, json=payload, verify=False)

    if response.status_code == 200:
        # Lưu trữ session
        session_token = response.cookies.get('X_AUTH')
        return session_token
    else:
        return None


def get_data_from_api(api_url, session_token):
    headers = {'Authorization': f'Bearer {session_token}'}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


def post_api_from_api(api_url, session_token, payload):
    headers = {'Authorization': f'Bearer {session_token}'}

    try:
        response = requests.post(
            api_url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
