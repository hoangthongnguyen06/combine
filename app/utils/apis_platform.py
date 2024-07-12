import requests

def login_to_api(username, password):
    login_url = 'https://example.com/api/login'
    payload = {'username': username, 'password': password}
    
    #send to server to login
    response = requests.post(login_url, data=payload)
    
    if response.status_code == 200:
        # Lưu trữ session
        session_token = response.cookies.get('session_token')
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
