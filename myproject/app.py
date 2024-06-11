"""A module, which contains the main Flask app."""
import requests
from flask import Flask, jsonify, render_template, request

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

STATUS_CODE_SEARCH_MOVIE = 200


def get_info_for_actor(data: dict, name: str, default_value):
    return data.get(name, default_value)


def get_info_list(data: dict, first_name: str, default_value, second_name: str):
    data_actor = data.get(first_name, [])
    if data_actor is None:
        return []
    return [actor.get(second_name, default_value) for actor in data.get(first_name, [])]


def get_actor_info(actor):
    res = {}
    keys_for_value = (
        ('name', 'N/A'),
        ('enName', 'N/A'),
        ('photo', 'N/A'),
        ('sex', 'N/A'),
        ('growth', 'N/A'),
        ('birthday', 'N/A'),
        ('age', 'N/A'),
        ('spouses', 'N/A'),
    )
    keys_for_list = (
        ('birthPlace', 'value', 'N/A'),
        ('facts', 'value', 'N/A'),
    )
    for first_name, default_value in keys_for_value:
        res[first_name] = get_info_for_actor(actor, first_name, default_value)

    for first_name, second_name, default_value in keys_for_list:
        res[first_name] = get_info_list(actor, first_name, default_value, second_name)

    res['movies'] = [
                {
                    'id': movie.get('id', 'N/A'),
                    'name': movie.get('name', 'N/A'),
                    'alternativeName': movie.get('alternativeName', 'N/A'),
                    'rating': movie.get('rating', 'N/A'),
                    'description': movie.get('description', 'N/A'),
                }
                for movie in actor.get('movies', 'N/A')
                if movie.get('enProfession') == 'actor'
            ]
    return res


def get_movie_value(data: dict, movie_name: str, default_value):
    return data.get(movie_name, default_value)


def get_movie_list(data: dict, first_name: str, default_value, second_name: str):
    data_movie = data.get(first_name, [])
    if data_movie is None:
        return []
    return [movie.get(second_name, default_value) for movie in data.get(first_name, [])]


def get_movie_info(movie):
    res = {}
    keys_for_value_m = (('name', 'N/A'), ('year', 'N/A'), ('description', 'N/A'), ('url', 'N/A'))
    keys_for_list_m = (('genres', 'name', 'N/A'), ('countries', 'name', 'N/A'))

    for first_name, default_value in keys_for_value_m:
        res[first_name] = get_movie_value(movie, first_name, default_value)

    for first_name, second_name, default_value in keys_for_list_m:
        res[first_name] = get_movie_list(movie, first_name, default_value, second_name)

    res['rating'] = movie.get('rating', {}).get('kp', 'N/A')

    res['actors'] = [
        {
            'id': actor.get('id', 'N/A'),
            'name': actor.get('name', 'N/A'),
            'photo': actor.get('photo', 'N/A'),
        }
        for actor in movie.get('persons', [])
        if actor.get('enProfession') == 'actor'
    ]

    return res


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
        movie_info = get_movie_info(movie)
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
        actor_info = get_actor_info(actor)
        return render_template('actor_details.html', actor=actor_info)
    return render_template('error.html', message='Unable to fetch data'), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=app.config['FLASK_PORT'])
