from pylib.app_driver import AppDriver


class LoginPageLocator:
    login = {'type_kind': 'text', 'type_name': '登录'}
    login_button = {'type_kind': 'name', 'type_name': 'app.guchat.android.uat:id/btn_login'}
    register_button = {'type_kind': 'text', 'type_name': '注册'}
    logout = {'type_kind': 'text', 'type_name': '登出'}
    logout_popup = {'type_kind': 'text', 'type_name': '登出后不会删除任何资料纪录，下次登入依然可以使用本帐号。'}
    input_phone_number = {'type_kind': 'text', 'type_name': '请填写手机号码'}
    input_password = {'type_kind': 'text', 'type_name': '请填写密码'}
    _alert_phone_and_password_not_match = {'type_kind': 'text', 'type_name': '手机号/密码错误，请重新输入'}


class MainPageLocator:
    friend_button = {'type_kind': 'name', 'type_name': 'app.guchat.android.uat:id/friend_navigation'}
    me_button = {'type_kind': 'name', 'type_name': 'app.guchat.android.uat:id/personal_navigation'}
    account_and_safety = {'type_kind': 'name', 'type_name': 'app.guchat.android.uat:id/cl_account'}
    logout_button = {'type_kind': 'name', 'type_name': 'app.guchat.android.uat:id/btn_logout'}
    logout_confirm_button = {'type_kind': 'name', 'type_name': 'android:id/button1'}


class LoginPage(AppDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def input_phone_number(self, phone_number):
        self.send_key(LoginPageLocator.input_phone_number, phone_number)

    def input_password(self, password):
        self.send_key(LoginPageLocator.input_password, password)

    def click_login_button(self):
        self.click_element(LoginPageLocator.login_button)


class MainPage(AppDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def click_me_button(self):
        self.click_element(MainPageLocator.me_button)

    def click_account_and_safety(self):
        self.click_element(MainPageLocator.account_and_safety)

    def click_logout_button(self):
        self.click_element(MainPageLocator.logout_button)

    def click_logout_confirm_button(self):
        self.click_element(MainPageLocator.logout_confirm_button)