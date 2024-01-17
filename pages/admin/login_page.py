from selenium.webdriver.common.by import By
from pylib.web_driver import WebDriver


class LoginPageLocator:
    login_pic = (By.XPATH, "//img[@src='https://admin-gu-chat-uat.idc.pstdsf.com/assets/large.035f7eeb.png']")
    login_title = (By.XPATH, "//h1[contains(text(), '股聊管理后台')]")
    input_account = (By.XPATH, "//input[@type='text']")
    input_password = (By.XPATH, "//input[@type='password']")
    login_button = (By.XPATH, "//button[@type='button']")


class DashboardPageLocator:
    dashboard_title = (By.XPATH, "//div[@class='dashboard-title' and contains(text(), '股聊仪表板')]")


class LoginPage(WebDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def input_account(self, phone_number):
        self.send_key(LoginPageLocator.input_account, phone_number)

    def input_password(self, password):
        self.send_key(LoginPageLocator.input_password, password)

    def click_login_button(self):
        self.click_element(LoginPageLocator.login_button)
