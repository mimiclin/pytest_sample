import os
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, locator, wait_time=6):
        if type(locator) is tuple:
            WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator),
                                                        message='fail to click element %s' % str(locator)).click()
        elif type(locator) is list:
            element = self.find_element(locator)
            element.click()

    def click_element_force(self, locator, wait_time=6):
        # self.find_invisible_element(locator)
        try:
            self.driver.find_element(locator).click()
            time.sleep(0.3)
        except:
            element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.3)

    def click_element_instantly(self, locator):
        '''Avoid to raise error when element is not clickable'''
        try:
            if locator[0] == 'xpath':
                self.driver.find_element(By.XPATH, locator[1]).click()
            if locator[0] == 'id':
                self.driver.find_element(By.ID, locator[1]).click()
        except:
            pass

    def find_element(self, locator, wait_time=6):
        element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator),
                                                              message='element %s invisible' % str(locator))  # 等待元素可见
        return element

    def find_elements(self, locator, wait_time=6):
        elements = []
        elements = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_all_elements_located(locator),
                                                               message='elements %s invisible' % str(locator))
        return elements

    # For whitelabel merchant selector
    def find_invisible_element(self, locator, wait_time=6):
        try:
            element = WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element_located(locator),
                                                                  message='element %s is invisible' % str(locator))
            return element
        except:
            ele = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            time.sleep(0.3)
            return ele

    def is_element_displayed(self, locator):
        try:
            return self.driver.find_element(By.XPATH, locator).is_displayed()
        except:
            return False

    def is_element_enabled(self, locator):
        return self.driver.find_element(By.XPATH, locator).is_enabled()

    def get_page_title(self):
        return self.driver.title

    def get_url(self, url):
        self.driver.get(url)

    def send_key(self, locator, text):
        element = self.find_element(locator)
        element.send_keys(text)

    def send_keys(self, locators, texts):
        elements = self.find_elements(locators)
        for element_index in range(len(elements)):
            elements[element_index].send_keys(texts[element_index])

    def html_selector(self, select_tag_locator, index=None, value=None, text=None):
        ''' HTML select tag. by index, value or text.'''
        html_selector = Select(self.driver.find_element(select_tag_locator[0], select_tag_locator[1]))
        if index is not None:
            html_selector.select_by_index(index)
        if value is not None:
            html_selector.select_by_value(value)
        if text is not None:
            html_selector.select_by_visible_text(text)

    def switch_to_new_window(self, wait_time=6):
        WebDriverWait(self.driver, wait_time).until(EC.new_window_is_opened(self.driver.window_handles), message='no pop-up window')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_first_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_webview(self):
        contexts = self.driver.contexts
        print(contexts)
        for content in contexts:
            if content != 'NATIVE_APP':
                self.driver.switch_to.context(content)
                print('switch to:', content)

    def keep_first_window(self):
        windows = self.driver.window_handles
        for i in windows[1:]:
            tab = self.driver.switch_to.window(i)
            self.driver.close()
        self.driver.switch_to.window(windows[0])

    def screenshot(self, path, file_name):
        # Create if screencap folder not exist
        if os.path.isdir(path) is False:
            os.makedirs(path)
        # Create file path
        t_time = time.strftime('%Y%m%d', time.localtime())
        file_name = '%s' % file_name + '_' + t_time + '.png'
        file_path = os.path.join(path, file_name)
        self.driver.save_screenshot(file_path)

    def refresh_current_page(self):
        self.driver.refresh()

    def clear_input(self, locator):
        input_box = self.driver.find_element(By.XPATH, locator[1])
        input_box.send_keys(Keys.CONTROL, 'a')  # ctrl+a
        input_box.send_keys(Keys.BACKSPACE)  # backspace

    def close(self, platform=None):
        self.driver.close()
        if platform == 'android':
            time.sleep(10)

    def quit(self):
        self.driver.quit()
