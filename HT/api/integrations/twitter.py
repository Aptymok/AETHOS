import os
import requests

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
TWITTER_SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'

def search_tweets(query, max_results=10):
    """Search recent tweets (v2). Returns list of tweets or [] on missing token/failure."""
    if not TWITTER_BEARER_TOKEN:
        return []

    headers = {
        'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
    }
    params = {
        'query': query,
        'max_results': max_results
    }
    try:
        r = requests.get(TWITTER_SEARCH_URL, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get('data', [])
    except Exception:
        pass
    return []
