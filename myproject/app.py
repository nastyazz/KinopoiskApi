"""A module, which contains the main Flask app."""
import requests
from flask import Flask, jsonify, render_template, request

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

STATUS_CODE_SEARCH_MOVIE = 200


def get_info_for_actor(data_dict: dict, name: str):
    """
    Retrieve actor information by specified key.

    Parameters:
        data_dict (dict): Dictionary containing actor data.
        name (str): Key name to retrieve the value for.

    Returns:
        The value associated with the key or the default value if the key is not found.
    """
    return data_dict.get(name, 'N/A')


def get_info_list(data_dlist: dict, value_key: str, list_key: str):
    """
    Retrieve a list of values from nested dictionaries.

    Parameters:
        data_dlist (dict): Dictionary containing data.
        value_key (str): Key name for the outer dictionary.
        list_key (str): Key name for the inner dictionaries.

    Returns:
        list: A list of values associated with the internal key for each item in the external list.
    """
    data_actor = data_dlist.get(value_key, [])
    if data_actor is None:
        return []
    return [actor.get(list_key, 'N/A') for actor in data_dlist.get(value_key, [])]


def get_actor_info(actor):
    """
    Retrieve complete actor information.

    Parameters:
        actor (dict): Dictionary containing actor data.

    Returns:
        dict: Dictionary with actor information, including their movies.
    """
    res = {}
    keys_for_value = (
        'name', 'enName', 'photo', 'sex',
        'growth', 'birthday', 'age', 'spouses',
    )
    keys_for_list = (
        ('birthPlace', 'value',),
        ('facts', 'value',),
    )
    for value_key in keys_for_value:
        res[value_key] = get_info_for_actor(actor, value_key)

    for list_key, second_name in keys_for_list:
        res[list_key] = get_info_list(actor, list_key, second_name)

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


def get_movie_value(data_dict: dict, movie_name: str):
    """
    Retrieve movie information by specified key.

    Parameters:
        data_dict (dict): Dictionary containing movie data.
        movie_name (str): Key name to retrieve the value for.

    Returns:
        The value associated with the key or the default value if the key is not found.
    """
    return data_dict.get(movie_name, 'N/A')


def get_movie_list(data_dlist: dict, value_key_m: str, list_key_m: str):
    """
    Retrieve a list of values from nested dictionaries.

    Parameters:
        data_dlist (dict): Dictionary containing data.
        value_key_m (str): Key name for the outer dictionary.
        list_key_m (str): Key name for the inner dictionaries.

    Returns:
        list: List of values associated with the inner key for each item in the outer list.
    """
    data_movie = data_dlist.get(value_key_m, [])
    if data_movie is None:
        return []
    return [movie.get(list_key_m, 'N/A') for movie in data_dlist.get(value_key_m, [])]


def get_movie_info(movie):
    """
    Retrieve complete movie information.

    Parameters:
        movie (dict): Dictionary containing movie data.

    Returns:
        dict: Dictionary with movie information, including its actors.
    """
    res = {}
    keys_for_value_m = (
        'name', 'year', 'description', 'url')
    keys_for_list_m = (('genres', 'name'), ('countries', 'name'))

    for value_key_m in keys_for_value_m:
        res[value_key_m] = get_movie_value(movie, value_key_m)

    for list_key_m, second_name in keys_for_list_m:
        res[list_key_m] = get_movie_list(movie, list_key_m, second_name)

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

    response = requests.get(url, headers=headers, timeout=1)
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
    response = requests.get(url, headers=headers, timeout=1)
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
    response = requests.get(url, headers=headers, timeout=1)
    if response.status_code == STATUS_CODE_SEARCH_MOVIE:
        actor = response.json()
        actor_info = get_actor_info(actor)
        return render_template('actor_details.html', actor=actor_info)
    return render_template('error.html', message='Unable to fetch data'), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=app.config['FLASK_PORT'])
