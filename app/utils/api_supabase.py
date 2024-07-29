import requests
from app.endpoints import APISupabase


def get_chu_de():
    chu_de_url = APISupabase.CHU_DE.value

    try:
        response = requests.get(chu_de_url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f'Supabase api error: {e}')
        return None
