import requests

TMDB_API_KEY = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details_by_title(title):
    search_url = f'{TMDB_BASE_URL}/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'language': 'en-US'
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            movie_id = results[0]['id']
            return get_movie_details(movie_id)
    return None

def get_movie_details(tmdb_id):
    url = f'{TMDB_BASE_URL}/movie/{tmdb_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movie_data = response.json()
        # Fetch director information
        credits_url = f'{TMDB_BASE_URL}/movie/{tmdb_id}/credits'
        credits_response = requests.get(credits_url, params=params)
        if credits_response.status_code == 200:
            credits_data = credits_response.json()
            directors = [member['name'] for member in credits_data['crew'] if member['job'] == 'Director']
            movie_data['director'] = ', '.join(directors)
        return movie_data
    return None