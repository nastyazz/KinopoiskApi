"""Tests for the API routes."""
import pytest
import requests

STATUS_CODE_SEARCH_MOVIE = 200


@pytest.fixture
def api_url():
    """
    Fixture for the API URL.

    Returns:
        str: The base URL of the API.
    """
    return 'http://127.0.0.1:8080'


def test_index(api_url):
    """
    Test the index route.

    Args:
        api_url (str): The base URL of the API.

    Return:
        None
    """
    response = requests.get(f'{api_url}/')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Movie Search' in response.text


def test_search_movie(api_url):
    """
    Test the search_movie route.

    Args:
        api_url (str): The base URL of the API.

    Return:
        None
    """
    response = requests.get(f'{api_url}/search?query=черная любовь')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Черная любовь' in response.text


def test_get_movie(api_url):
    """
    Test the get_movie route.

    Args:
        api_url (str): The base URL of the API.

    Return:
        None
    """
    response = requests.get(f'{api_url}/movie/266311')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Черная любовь' in response.text


def test_get_actor(api_url):
    """
    Test the get_actor route.

    Args:
        api_url (str): The base URL of the API.

    Return:
        None
    """
    response = requests.get(f'{api_url}/actor/1455007')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Бурак Озчивит' in response.text
