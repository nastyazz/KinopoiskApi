"""Tests for the API routes."""
import pytest

from app import app

STATUS_CODE_SEARCH_MOVIE = 200
UTF8ENCODING = 'utf-8'


@pytest.fixture
def client():
    """
    Fixture for creating a test client.

    Yields:
        FlaskClient: The test client for the Flask application.
    """
    with app.test_client() as client:
        yield client


def test_index(client):
    """
    Test the index route.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Return:
        None
    """
    response = client.get('/')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Movie Search' in response.data.decode(UTF8ENCODING)


def test_search_movie(client):
    """
    Test the search_movie route.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Return:
        None
    """
    response = client.get('/search?query=черная любовь')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Черная любовь' in response.data.decode(UTF8ENCODING)


def test_get_movie(client):
    """
    Test the get_movie route.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Return:
        None
    """
    response = client.get('/movie/266311')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Черная любовь' in response.data.decode(UTF8ENCODING)


def test_get_actor(client):
    """
    Test the get_actor route.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Return:
        None
    """
    response = client.get('/actor/1455007')
    assert response.status_code == STATUS_CODE_SEARCH_MOVIE
    assert 'Бурак Озчивит' in response.data.decode(UTF8ENCODING)
