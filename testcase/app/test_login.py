import allure
import pytest

from pages.app.login_page import LoginPageLocator, LoginPage, MainPageLocator, MainPage
from pylib.allure_decorator import allure_decorator


######################
#  setup & teardown  #
######################


######################
#      testCase      #
######################
@allure_decorator(epic="APP", feature="產品", story="登入頁")
class TestAppLogin(object):
    @pytest.fixture(autouse=True)
    def __initialize(self, app_driver, is_element_found):
        self.driver = app_driver
        self.login_page = LoginPage(app_driver)
        self.main_page = MainPage(app_driver)
        self.is_element_found = is_element_found

    @allure.title("輸入錯誤的帳號密碼，登入失敗")
    def test_login_fail(self):
        self.login_page.click_login_button()
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc123456')
        self.login_page.click_login_button()
        assert self.is_element_found(LoginPageLocator._alert_phone_and_password_not_match) is True

    @allure.title("輸入錯誤的帳號密碼，登入失敗_failed_case")
    def test_login_fail_failed_case(self):
        self.login_page.click_login_button()
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc123456')
        self.login_page.click_login_button()
        assert self.is_element_found(MainPageLocator.friend_button) is True

    @allure.title("輸入正確的帳號密碼，登入成功")
    def test_login_success(self):
        self.login_page.click_login_button()
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc12345')
        self.login_page.click_login_button()
        assert self.is_element_found(MainPageLocator.friend_button) is True

    @allure.title("從選單登出")
    def test_logout_success(self):
        self.main_page.click_me_button()
        self.main_page.click_account_and_safety()
        self.main_page.click_logout_button()
        self.main_page.click_logout_confirm_button()
        assert self.is_element_found(LoginPageLocator.login_button)
