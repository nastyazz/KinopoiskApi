"""Configuration module for the Flask application."""

import os


class Config:
    """Configuration class for the Flask application."""

    FLASK_PORT = os.getenv('FLASK_PORT', 8080)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://test:test@localhost:37891/test')
    KINOTOKEN = os.getenv('KINOTOKEN', 'Q3CD9A4-PX14BWS-J7GM161-DMYD85E')

    HEADERS = {
        'accept': 'application/json',
        'X-API-KEY': KINOTOKEN,
    }

    OK = 200
    MOVED = 302

    POST = 'POST'
    GET = 'GET'
