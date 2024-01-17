import allure
import pytest

from pages.admin.login_page import LoginPageLocator, DashboardPageLocator, LoginPage
from pylib.allure_decorator import allure_decorator


######################
#  setup & teardown  #
######################


######################
#      testCase      #
######################
@allure_decorator(epic="Admin", feature="股聊", story="登入頁")
class TestAdminLogin(object):
    @pytest.fixture(autouse=True)
    def __initialize(self, chrome_driver, is_element_found):
        self.driver = chrome_driver
        self.login_page = LoginPage(chrome_driver)
        self.is_element_found = is_element_found

    @allure.title("檢查登入頁元件是否存在")
    def test_login_page_elements(self):
        items = [item for item in dir(LoginPageLocator) if not item.startswith('__')]
        for item in items:
            print(f'Found element [{item}]: {getattr(LoginPageLocator, item)}')
            assert self.is_element_found(getattr(LoginPageLocator, item)) is True
        assert self.driver.title == '股聊-登入'

    @allure.title("輸入錯誤的帳號密碼，登入失敗")
    def test_login_fail(self):
        self.login_page.input_account('mimic001')
        self.login_page.input_password('abc123456')
        self.login_page.click_login_button()
        assert self.is_element_found(DashboardPageLocator.dashboard_title) is False

    @allure.title("輸入正確的帳號密碼，登入成功")
    def test_login_success(self):
        self.login_page.input_account('mimic001')
        self.login_page.input_password('abc123')
        self.login_page.click_login_button()
        assert self.is_element_found(DashboardPageLocator.dashboard_title) is True
