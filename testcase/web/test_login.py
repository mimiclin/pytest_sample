import allure
import pytest

from pages.web.login_page import LoginPageLocator, WelcomePageLocator, LoginPage
from pages.web.chatroom_page import ChatroomPageLocator
from pylib.allure_decorator import allure_decorator


######################
#  setup & teardown  #
######################


######################
#      testCase      #
######################
@allure_decorator(epic="Web", feature="產品", story="登入頁")
class TestLogin(object):
    @pytest.fixture(autouse=True)
    def __initialize(self, chrome_driver, is_element_found):
        self.driver = chrome_driver
        self.login_page = LoginPage(chrome_driver)
        self.is_element_found = is_element_found

    @allure.title("檢查登入頁元件是否存在")
    def test_login_page_elements(self):
        items = [item for item in dir(LoginPageLocator) if not item.startswith('_')]
        for item in items:
            print(f'Found element [{item}]: {getattr(LoginPageLocator, item)}')
            assert self.is_element_found(getattr(LoginPageLocator, item)) is True
        assert self.driver.title == 'PROD-WEB'

    @allure.title("輸入錯誤的帳號密碼，登入失敗")
    def test_login_fail(self):
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc123456')
        self.login_page.click_login_button()
        assert self.is_element_found(LoginPageLocator._alert_phone_and_password_not_match) is True

    @allure.title("輸入正確的帳號密碼，登入成功")
    def test_login_success(self):
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc12345')
        self.login_page.click_login_button()
        assert self.is_element_found(WelcomePageLocator.welcome_title) is True
        self.login_page.click_login_confirm_button()
        assert self.is_element_found(ChatroomPageLocator.chatroom_pic) is True

    @allure.title("輸入正確的帳號密碼，登入成功-failed case")
    def test_login_success_failed_case(self):
        self.login_page.input_phone_number('2260000004')
        self.login_page.input_password('abc12345')
        self.login_page.click_login_button()
        assert self.is_element_found(WelcomePageLocator.welcome_title) is True
        self.login_page.click_login_confirm_button()
        assert self.is_element_found(ChatroomPageLocator.fake_chatroom_pic) is True
