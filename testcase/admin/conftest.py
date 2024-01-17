import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pylib.slack import slack_message


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def handle_failed_case(request, chrome_driver):
    yield
    if request.node.rep_call.failed:
        allure.attach(chrome_driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        slack_message(f"{request.node.rep_call}\n")


@pytest.fixture(scope="function")
def chrome_driver(get_url):
    chrome_option = __get_chrome_options(width=1900, height=1000, is_wap=False, is_headless=False)
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(url=get_url)

    yield driver

    driver.close()


@pytest.fixture(scope="function")
def get_url():
    return "https://admin-gu-chat-uat.idc.pstdsf.com/login"


def __is_element_found(chrome_driver, locator):
    try:
        WebDriverWait(chrome_driver, 3).until(EC.visibility_of_element_located(locator), message=f'element {str(locator)} not found')
        return True
    except TimeoutException:
        print(f'Can not find element: {locator}')
        return False


def __get_chrome_options(width, height, is_wap, is_headless=1):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=%s,%s' % (str(width), str(height)))
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_experimental_option('w3c',False)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    # 限制selenium本身的Error LOG噴出(無關測試腳本問題)
    chrome_options.add_argument("--log-level=3")

    if is_wap:
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 850, "pixelRatio": 3.0},  # 定義設備高寬，象素比
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "  # 通過UA來模擬
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    if is_headless:
        chrome_options.add_argument('--headless')

    return chrome_options


@pytest.fixture(scope="function")
def is_element_found(chrome_driver):
    return lambda locator: __is_element_found(chrome_driver, locator)
