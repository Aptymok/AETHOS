import os
import requests

NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
NEWSAPI_URL = 'https://newsapi.org/v2/top-headlines'

def fetch_top_headlines(country='us', q=None, page_size=20):
    """Fetch top headlines using NewsAPI.org. Returns list of articles or [] on failure."""
    if not NEWS_API_KEY:
        # fallback deterministic empty list for staging
        return []

    params = {
        'apiKey': NEWS_API_KEY,
        'country': country,
        'pageSize': page_size
    }
    if q:
        params['q'] = q

    try:
        r = requests.get(NEWSAPI_URL, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get('articles', [])
    except Exception:
        pass

    return []
