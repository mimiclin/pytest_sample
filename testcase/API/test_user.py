import allure
import pytest

from pylib.api import ApiController
from pylib.data_loader import TestDataReader
from pylib.allure_decorator import allure_decorator

test_data = TestDataReader()
test_data.read_json5('test_user.json5', file_side='web')


######################
#  setup & teardown  #
######################


######################
#      testCase      #
######################
@allure.epic('API')
@allure.feature('User')
class TestUser:
    @staticmethod
    @allure_decorator(story="/api/v1/login", title="{test[scenario]}")
    @pytest.mark.parametrize("test", test_data.get_case('user_login'))
    def test_user_login(test):
        json_replace = test_data.replace_json(test['json'], test['target'])

        api = ApiController(platform='web')
        resp = api.send_request(method=test['req_method'],
                                url=test['req_url'],
                                json=json_replace,
                                params=test['params'],
                                token=None)

        assert resp.status_code == test['code_status'], resp.text
        # assert test['keyword'] in resp.text

    @staticmethod
    @allure_decorator(story="/api/v1/users/me", title="{test[scenario]}")
    @pytest.mark.parametrize("test", test_data.get_case('user_me'))
    def test_user_me(test, get_web_token):
        json_replace = test_data.replace_json(test['json'], test['target'])

        api = ApiController(platform='web')
        resp = api.send_request(method=test['req_method'],
                                url=test['req_url'],
                                json=json_replace,
                                params=test['params'],
                                token=get_web_token)

        assert resp.status_code == test['code_status'], resp.text
        # assert test['keyword'] in resp.text

    @staticmethod
    @allure_decorator(story="/api/v1/logout", title="{test[scenario]}")
    @pytest.mark.parametrize("test", test_data.get_case('user_logout'))
    def test_user_logout(test, get_web_token):
        json_replace = test_data.replace_json(test['json'], test['target'])

        api = ApiController(platform='web')
        resp = api.send_request(method=test['req_method'],
                                url=test['req_url'],
                                json=json_replace,
                                params=test['params'],
                                token=get_web_token)

        assert resp.status_code == test['code_status'], resp.text
        # assert test['keyword'] in resp.text