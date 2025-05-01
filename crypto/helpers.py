from functools import wraps
import requests

def user_authenticated(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            session_id = request.user.email
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

        # Store session_id into request so you can use it in the view
        request.session["user"] = session_id
        
        return func(request, *args, **kwargs)
    return wrapper

def get_indodax_tickers():
    url = 'https://indodax.com/api/tickers'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['tickers']
    else:
        print(f"Error: {response.status_code}")
        return None

def get_indodax_pairs():
    pairs_url = 'https://indodax.com/api/pairs'
    response = requests.get(pairs_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching pairs: {response.status_code}")
        return []