import pytest
from json import JSONDecodeError
from pylib.web_api import WebApi


@pytest.fixture(scope="function")
def get_web_token():
    api = WebApi()
    resp = api.login()
    try:
        token = resp.json()['result']['access_token']
    except JSONDecodeError:
        print(f'Login failed, receive unknown response: {resp.json()}')
        raise
    return token
