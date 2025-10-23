import os
import requests

"""Skeleton adapter for NOAA (geomagnetic / space weather) data.

Usage:
 - Set NOAA_API_KEY in environment
 - Replace fetch functions with actual endpoints and parsing

This module intentionally contains minimal code and safe defaults for staging.
"""

NOAA_API_KEY = os.getenv('NOAA_API_KEY')

def fetch_geomagnetic_data():
    """Fetch geomagnetic data. Return a dict with 'storm_level' and 'kp_index'.
    In staging, returns deterministic neutral values.
    """
    if not NOAA_API_KEY:
        # Deterministic neutral fallback for staging
        return {
            'storm_level': 0.5,
            'kp_index': 3.0,
            'activity': 'quiet'
        }

    # Example placeholder - implement real NOAA API calls here
    try:
        # Example endpoint (replace with actual NOAA endpoint and params)
        url = 'https://api.weather.gov/alerts'  # NOT the geomag endpoint; placeholder
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            # Parse response into expected shape
            return {
                'storm_level': 0.4,
                'kp_index': 2.5,
                'activity': 'quiet'
            }
    except Exception:
        pass

    # Fallback neutral
    return {
        'storm_level': 0.5,
        'kp_index': 3.0,
        'activity': 'quiet'
    }
