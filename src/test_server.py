from fastapi.testclient import TestClient
from .server import app
from .samples import (
    ANIME_PICS_URLS_TEST,
    RANDOM_PICS_URLS_TEST,
    FAULTY_URLS_TEST,
)

"""
This module defines tests for the API.
"""

client = TestClient(app)


def test_is_it_anime():
    """
    Runs tests for the /is_it_anime route 
    accordingly to the supposed usage thereof.

    Supposed usage: .../apime$ pytest --ignore=bin --ignore=lib
    """

    for url in ANIME_PICS_URLS_TEST:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert response.json() == {"conclusion": "Yes"}

    for url in RANDOM_PICS_URLS_TEST:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert response.json() == {"conclusion": "No"}

    for url in FAULTY_URLS_TEST:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert "detail" in response.json()
