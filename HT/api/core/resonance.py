import requests
import os
import json
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional

class ExternalResonanceEngine:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY', '')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID', '')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
        
    async def fetch_global_resonance(self) -> Dict:
        """Captura resonancia de múltiples fuentes externas"""
        resonance_data = {
            'temporal_markers': [],
            'collective_emotions': {},
            'emerging_patterns': [],
            'resonance_frequency': 0.0
        }
        
        try:
            # 1. Noticias globales (NewsAPI)
            from integrations.newsapi import fetch_top_headlines
            articles = fetch_top_headlines(country='us', page_size=20)
            if articles:
                news_resonance = self._process_news_articles(articles)
            else:
                news_resonance = await self._analyze_news_resonance()
            resonance_data['temporal_markers'].extend(news_resonance['trends'])
            
            # 2. Tendencias de redes sociales
            social_resonance = await self._analyze_social_resonance()
            resonance_data['collective_emotions'] = social_resonance['emotions']
            
            # 3. Datos astronómicos y cósmicos
            cosmic_resonance = await self._fetch_cosmic_data()
            resonance_data['resonance_frequency'] = cosmic_resonance['frequency']
            
            # 4. Análisis de patrones emergentes
            patterns = self._detect_emerging_patterns(
                news_resonance, 
                social_resonance, 
                cosmic_resonance
            )
            resonance_data['emerging_patterns'] = patterns
            
        except Exception as e:
            print(f"Error fetching external resonance: {e}")
            
        return resonance_data
    
    async def _analyze_news_resonance(self) -> Dict:
        """Analiza resonancia en noticias globales"""
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'country': 'us',
                'pageSize': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return self._process_news_articles(articles)
                
        except Exception as e:
            print(f"News API error: {e}")
            
        return {'trends': [], 'sentiment': 0.5}
    
    def _process_news_articles(self, articles: List) -> Dict:
        """Procesa artículos para extraer resonancia"""
        keywords = []
        sentiments = []
        
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            
            # Análisis simple de keywords
            words = title.lower().split() + description.lower().split()
            keywords.extend([w for w in words if len(w) > 5])
            
            # Análisis de sentimiento básico
            sentiment = self._analyze_text_sentiment(title + " " + description)
            sentiments.append(sentiment)
        
        # Calcular tendencias
        trends = self._extract_trends(keywords)
        avg_sentiment = np.mean(sentiments) if sentiments else 0.5
        
        return {
            'trends': trends[:5],
            'sentiment': avg_sentiment,
            'collective_mood': 'positive' if avg_sentiment > 0.6 else 'negative' if avg_sentiment < 0.4 else 'neutral'
        }
    
    async def _analyze_social_resonance(self) -> Dict:
        """Analiza resonancia en redes sociales (simulado)"""
        # EN PRODUCCIÓN: integrar con Twitter API, Reddit API, etc.
        # Para staging, usar RNG determinista por fecha para reproducibilidad.
        from datetime import datetime
        seed = int(datetime.now().strftime('%Y%m%d'))
        rng = np.random.RandomState(seed)
        emotions = {
            'joy': float(rng.uniform(0.1, 0.8)),
            'fear': float(rng.uniform(0.1, 0.6)),
            'anger': float(rng.uniform(0.1, 0.5)),
            'anticipation': float(rng.uniform(0.3, 0.9)),
            'trust': float(rng.uniform(0.2, 0.7))
        }

        return {
            'emotions': emotions,
            'dominant_emotion': max(emotions.items(), key=lambda x: x[1])[0],
            'social_coherence': float(rng.uniform(0.3, 0.8))
        }
    
    async def _fetch_cosmic_data(self) -> Dict:
        """Obtiene datos cósmicos y astronómicos"""
        try:
            # Datos solares (NASA API)
            solar_data = await self._fetch_solar_data()
            
            # Fases lunares
            moon_phase = self._calculate_moon_phase()
            
            # Campos geomagnéticos
            geomagnetic = self._simulate_geomagnetic_data()  # TODO: Integrar con NOAA API en producción
            
            return {
                'solar_activity': solar_data.get('activity', 0.5),
                'moon_phase': moon_phase,
                'geomagnetic_storm': geomagnetic['storm_level'],
                'frequency': self._calculate_cosmic_frequency(solar_data, moon_phase, geomagnetic)
            }
            
        except Exception as e:
            print(f"Cosmic data error: {e}")
            return {'frequency': 0.5}
    
    def _calculate_cosmic_frequency(self, solar_data: Dict, moon_phase: float, geomagnetic: Dict) -> float:
        """Calcula frecuencia cósmica basada en datos astronómicos"""
        base_freq = 432.0  # Hz base
        
        # Modificadores
        solar_mod = solar_data.get('activity', 0.5) * 10
        moon_mod = moon_phase * 5
        geo_mod = geomagnetic.get('storm_level', 0.5) * 3
        
        return base_freq + solar_mod + moon_mod + geo_mod
    
    def _detect_emerging_patterns(self, news: Dict, social: Dict, cosmic: Dict) -> List[str]:
        """Detecta patrones emergentes cruzando múltiples fuentes"""
        patterns = []
        
        # Patrones basados en coherencia emocional
        if social['dominant_emotion'] == 'joy' and news['sentiment'] > 0.7:
            patterns.append("colectivo_expansivo")
            
        if cosmic['frequency'] > 440 and social['social_coherence'] > 0.7:
            patterns.append("resonancia_alta")
            
        if news['collective_mood'] == 'negative' and cosmic['geomagnetic_storm'] > 0.7:
            patterns.append("tension_colectiva")
            
        return patterns
    
    def _analyze_text_sentiment(self, text: str) -> float:
        """Análisis básico de sentimiento (en producción usar modelo ML)"""
        positive_words = ['good', 'great', 'amazing', 'positive', 'hope', 'progress']
        negative_words = ['bad', 'terrible', 'crisis', 'war', 'death', 'fear']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.5
            
        return pos_count / total
    
    def _extract_trends(self, keywords: List[str]) -> List[str]:
        """Extrae tendencias de lista de keywords"""
        from collections import Counter
        return [word for word, count in Counter(keywords).most_common(10)]
    
    def _calculate_moon_phase(self) -> float:
        """Calcula fase lunar actual (0 = nueva, 1 = llena)"""
        from datetime import datetime
        import math
        
        now = datetime.now()
        # Cálculo simplificado de fase lunar
        days_in_cycle = 29.53
        known_new_moon = datetime(2024, 1, 11)  # Fecha de luna nueva conocida
        days_since_new = (now - known_new_moon).days
        phase = (days_since_new % days_in_cycle) / days_in_cycle
        return phase
    
    def _simulate_geomagnetic_data(self) -> Dict:
        """Stub determinista para datos geomagnéticos.

        EN PRODUCCIÓN: reemplazar por adaptador a NOAA/servicio real. Hasta entonces
        devolveremos valores neutrales reproducibles para evitar fluctuaciones aleatorias
        en staging.
        """
        # Valores deterministas (neutrales) para staging
        return {
            'storm_level': 0.5,
            'kp_index': 3.0,
            'activity': 'quiet'
        }
    
    async def _fetch_solar_data(self) -> Dict:
        """Obtiene datos solares (stub determinista).

        EN PRODUCCIÓN: usar NASA/NOAA endpoints.
        """
        from datetime import datetime
        seed = int(datetime.now().strftime('%Y%m%d')) + 42
        rng = np.random.RandomState(seed)
        return {
            'activity': float(rng.uniform(0.1, 0.9)),
            'flares_today': int(rng.randint(0, 5)),
            'sunspots': int(rng.randint(0, 100))
        }