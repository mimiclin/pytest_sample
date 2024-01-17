import allure
import os
import yaml
import pytest
from airtest.core.api import stop_app, clear_app, start_app, auto_setup, snapshot
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from pylib.slack import slack_message


@pytest.fixture(scope="function")
def app_driver():
    # app = AppDriver()
    # poco, _ = app.airtest_connect_phone()

    phone_name = 'Pixel5_31'
    connect_type = 'local'
    connection = None
    cap_method = 'javacap'
    connection = get_phone_connect_link(phone_name, '', connect_type)

    while True:
        try:
            auto_setup(__file__, logdir=False, devices=[f'{connection}?cap_method={cap_method}'])  # Airtest 連線手機
            break
        except Exception:
            print('failed')

    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)

    choose_app()

    yield poco

    package_name = 'app.product.android.uat'
    stop_app(package_name)
    poco_name = 'com.netease.open.pocoservice'
    clear_app(poco_name)


@pytest.fixture(scope="function", autouse=True)
def handle_failed_case(request, app_driver):
    yield
    if request.node.rep_call.failed:
        snapshot(filename=r'.\screenshot.png')
        allure.attach.file(source=r'.\screenshot.png', name="screenshot", attachment_type=allure.attachment_type.PNG)
        slack_message(f"{request.node.rep_call}\n")


def get_device_conf():
    root_path = str(os.path.abspath(__file__).split('pytest_sample')[0]) + 'pytest_sample'
    path = os.path.join(root_path, "configs", "app", "phone_config.yml")
    with open(path, 'r', encoding='utf-8') as phone_config:
        cfg = yaml.load(phone_config, Loader=yaml.FullLoader)
    return cfg


def get_phone_connect_link(phone_name, ip='', connect_type='local'):
    phone_platform = 'Android'
    conf = get_device_conf()['Phone_conf']
    connection = ''
    if connect_type == 'remote':
        if phone_platform == 'Android':
            connection = f'Android://127.0.0.1:5037/{ip}'
        elif phone_platform == 'iOS':
            connection = f'ios:///http://{ip}:{conf[phone_name]["port"]}'
    elif connect_type == 'local':
        if phone_platform == 'Android':
            connection = f'Android:///{conf[phone_name]["udid"]}'
        elif phone_platform == 'iOS':
            connection = f'ios:///http://127.0.0.1:{conf[phone_name]["port"]}'  # 主機端預設位置
    else:
        raise ValueError(f'connect_type undefined: {connect_type}')

    return connection


def __is_element_found(app_driver, locator):
    if app_driver(**{locator['type_kind']: locator['type_name']}).exists():
        return True
    else:
        return False


@pytest.fixture(scope="function")
def is_element_found(app_driver):
    return lambda locator: __is_element_found(app_driver, locator)


def choose_app():
    package_name = 'app.product.android.uat'
    stop_app(package_name)
    start_app(package_name)


@pytest.fixture(scope='function')
def quick_login(app_driver):
    from pages.app.login_page import LoginPage
    login_page = LoginPage(app_driver)
    login_page.click_login_button()
    login_page.input_phone_number('2260000004')
    login_page.input_password('abc12345')
    login_page.click_login_button()
