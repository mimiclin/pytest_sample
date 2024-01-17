import os
import logging
import yaml
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import auto_setup


class AppDriver:
    def __init__(self, driver):
        self.driver = driver
        self.phone_platform = 'Android'
        self.phone_name = 'Pixel5_31'
        self.connect_type = 'local'
        self.connection = None
        self.cap_method = 'javacap'

    def click_element(self, locator, times=1):
        locator['times'] = times
        el = self.driver(**{locator['type_kind']: locator['type_name']})
        el.click()

    def send_key(self, locator, text):
        el = self.driver(**{locator['type_kind']: locator['type_name']})
        el.set_text(text)

    @staticmethod
    def get_device_conf():
        root_path = str(os.path.abspath(__file__).split('pytest_sample')[0]) + 'pytest_sample'
        path = os.path.join(root_path, "configs", "app", "phone_config.yml")
        with open(path, 'r', encoding='utf-8') as phone_config:
            cfg = yaml.load(phone_config, Loader=yaml.FullLoader)
        return cfg

    def get_phone_connect_link(self, phone_name, ip='', connect_type='local'):
        conf = self.get_device_conf()['Phone_conf']
        phone_platform = self.phone_platform
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

    # 注意func執行順序不可倒，要先執行過setting_test_data()
    def airtest_connect_phone(self):
        # 取得Airtest格式的手機連線link
        self.connection = self.get_phone_connect_link(self.phone_name, '', self.connect_type)

        while True:
            try:
                auto_setup(__file__, logdir=False, devices=[f'{self.connection}?cap_method={self.cap_method}'])  # Airtest 連線手機
                break
            except Exception:
                logging.exception('exception log')

        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
        parameter = (poco, '')

        # if gl.get_value("PHONE_PLATFORM") == 'Android':
        #     poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
        #     parameter = (poco, '')
        #
        # if gl.get_value("PHONE_PLATFORM") == 'iOS':
        #     if not cli_setup():
        #         auto_setup(__file__, logdir=True, devices=[self.connection, ])
        #     poco = iosPoco()
        #     wda_service = wda.Client(self.connection.split('///')[-1])
        #     parameter = (poco, wda_service)

        return parameter
