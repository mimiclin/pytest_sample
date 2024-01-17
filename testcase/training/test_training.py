import allure
import pytest

from pylib.data_loader import TestDataReader
from pylib.allure_decorator import allure_decorator

test_data = TestDataReader()
test_data.read_json5('test_sample.json5', file_side='web')

######################
#  setup & teardown  #
######################


######################
#      testCase      #
######################
@allure.epic('TestFixture')
@allure.feature('案例-fixture')
class TestFixture:
    @staticmethod
    @allure_decorator(story="測試setup and teardown的效果 - 案例1", title="看右邊的訊息 →")
    def test_fixture_1(print_function_message, print_class_message):
        print(f'這裡是test case 1的實作部份')
        assert 1 == 1

    @staticmethod
    @allure_decorator(story="測試setup and teardown的效果 - 案例2", title="看右邊的訊息 →")
    def test_fixture_2(print_function_message):
        print(f'這裡是test case 2的實作部份')
        assert 2 == 2

    @staticmethod
    @allure_decorator(story="測試setup and teardown的效果 - 案例3", title="看右邊的訊息 →")
    def test_fixture_3(get_my_name):
        print(f'這裡是test case 3的實作部份')
        print(f'get_my_name回傳的是: {get_my_name}')
        assert get_my_name == 'Mimic'


@allure.epic('TestParametrize')
@allure.feature('案例 - 參數化的導入方式')
class TestParametrize:
    @staticmethod
    @pytest.mark.smoke
    @allure_decorator(story="1. 測試單一參數的案例", title="{value} = {value}")
    @pytest.mark.parametrize("value", [1, 2, 3])
    def test_single_param(value):
        assert value * 1 == value

    @staticmethod
    @allure_decorator(story="2. 測試求平方的數值", title="{value} 的平方 = {answer}")
    @pytest.mark.parametrize("value, answer", [(1, 1), (2, 4), (3, 9), (4, 15)])
    def test_square(value, answer):
        assert value ** 2 == answer

    @staticmethod
    @allure_decorator(story="3. 測試從外部檔案載入測試資料", title="{source[scenario]}")
    @pytest.mark.parametrize("source", test_data.get_case('get_sample_data'))
    def test_get_data(source):
        td = test_data.replace_json(source['json'], source['target'])
        country = td['country']
        phone = td['phone']
        password = td['password']
        expected_result = source['expected_result']
        print(f"country: {country}, phone: {phone}, password: {password}")
        assert expected_result == 'pass'

    @staticmethod
    @pytest.mark.skip(reason='還沒開發完QQ')
    @pytest.mark.parametrize("value, answer", [(1, 1), (2, 8), (3, 27), (4, 64)])
    @allure_decorator(story="4. 測試skip的效果", title="{value} 的立方= {answer}")
    def test_cube(value, answer):
        assert value ** 3 == answer
