from selenium.webdriver.common.by import By
from pylib.web_driver import WebDriver


class LoginPageLocator:
    login_pic = (By.XPATH, "//p[@class='form-entry__title__text' and contains(text(), '登录')]")
    input_phone_number = (By.XPATH, "//input[@type='tel']")
    input_password = (By.XPATH, "//input[@type='password']")
    login_button = (By.XPATH, "//button[@type='button']")
    _alert_phone_and_password_not_match = (By.XPATH, "//p[@class='alert__text' and contains(text(), '手机号/密码错误，请重新输入')]")


class WelcomePageLocator:
    welcome_title = (By.XPATH, "//p[contains(text(), '已成功连线')]")
    confirm_button = (By.XPATH, "//button[@type='button']")


class LoginPage(WebDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def input_phone_number(self, phone_number):
        self.send_key(LoginPageLocator.input_phone_number, phone_number)

    def input_password(self, password):
        self.send_key(LoginPageLocator.input_password, password)

    def click_login_button(self):
        self.click_element(LoginPageLocator.login_button)
        # self.find_element(LoginPageLocator.login_button).click()

    def click_login_confirm_button(self):
        self.click_element(WelcomePageLocator.confirm_button)
