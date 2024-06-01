"""A module, which contains the main Flask app."""
import requests
from flask import Flask, jsonify, render_template, request

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

STATUS_CODE_SEARCH_MOVIE = 200


@app.route('/')
def index():
    """
    Render the index.html template.

    Args:
        None

    Returns:
        HTML: The rendered index.html template.
    """
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    """
    Endpoint for favicon.ico.

    Args:
        None

    Returns:
        str: An empty string with status code 204.
    """
    return '', 204


@app.route('/search', methods=['GET'])
def search_movie():
    """
    Search for movies based on the provided query.

    Args:
        None

    Returns:
        HTML: The rendered search_results.html template.
        JSON: Error message if unable to fetch data.
    """
    query = request.args.get('query')
    url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={query}'
    headers = {
        'accept': 'application/json',
        'X-API-KEY': Config.KINOTOKEN,
    }

    response = requests.get(url, headers=headers)
    message_error = {'error': 'Unable to fetch data', 'status_code': response.status_code}
    if response.status_code == STATUS_CODE_SEARCH_MOVIE:
        data_movie = response.json()
        movies = data_movie.get('docs', [])
        return render_template('search_results.html', movies=movies)
    return jsonify(message_error), response.status_code


@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Get details of a specific movie by its ID.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        HTML: The rendered movie_details.html template.
        HTML: Error message if unable to fetch data.
    """
    url = f'https://api.kinopoisk.dev/v1.4/movie/{movie_id}'
    headers = {
        'accept': 'application/json',
        'X-API-KEY': Config.KINOTOKEN,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == STATUS_CODE_SEARCH_MOVIE:
        movie = response.json()
        movie_info = {
            'name': movie.get('name', 'N/A'),
            'year': movie.get('year', 'N/A'),
            'description': movie.get('description', 'N/A'),
            'rating': movie.get('rating', {}).get('kp', 'N/A'),
            'url': movie.get('url', 'N/A'),
            'genres': [genre.get('name', 'N/A') for genre in movie.get('genres', [])],
            'countries': [country.get('name', 'N/A') for country in movie.get('countries', [])],
            'actors':
            [
                {
                    'id': actor.get('id', 'N/A'),
                    'name': actor.get('name', 'N/A'),
                    'photo': actor.get('photo', 'N/A'),
                }
                for actor in movie.get('persons', 'N/A')
                if actor.get('enProfession') == 'actor'
            ],
        }
        return render_template('movie_details.html', movie=movie_info)
    return render_template('error.html', message='Unable to fetch data'), response.status_code


@app.route('/actor/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    """
    Get details of a specific actor by their ID.

    Args:
        actor_id (int): The ID of the actor.

    Returns:
        HTML: The rendered actor_details.html template.
        HTML: Error message if unable to fetch data.
    """
    url = f'https://api.kinopoisk.dev/v1.4/person/{actor_id}'
    headers = {
        'accept': 'application/json',
        'X-API-KEY': Config.KINOTOKEN,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == STATUS_CODE_SEARCH_MOVIE:
        actor = response.json()
        actor_info = {
            'name': actor.get('name', 'N/A'),
            'enName': actor.get('enName', 'N/A'),
            'photo': actor.get('photo', 'N/A'),
            'sex': actor.get('sex', 'N/A'),
            'growth': actor.get('growth', 'N/A'),
            'birthday': actor.get('birthday', 'N/A'),
            'age': actor.get('age', 'N/A'),
            'birthPlace': [place.get('value', 'N/A') for place in actor.get('birthPlace', [])],
            'spouses': actor.get('spouses', []),
            'facts': [fact.get('value', 'N/A') for fact in actor.get('facts', [])],
            'movies':
            [
                {
                    'id': movie.get('id', 'N/A'),
                    'name': movie.get('name', 'N/A'),
                    'alternativeName': movie.get('alternativeName', 'N/A'),
                    'rating': movie.get('rating', 'N/A'),
                    'description': movie.get('description', 'N/A'),
                }
                for movie in actor.get('movies', 'N/A')
                if movie.get('enProfession') == 'actor'
            ],
        }
        return render_template('actor_details.html', actor=actor_info)
    return render_template('error.html', message='Unable to fetch data'), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=app.config['FLASK_PORT'])
