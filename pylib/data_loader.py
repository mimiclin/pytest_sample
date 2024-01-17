import os
import json5
import copy
import configparser

config = configparser.ConfigParser()
config.read('configs/config.ini')


class TestDataReader:
    __test__ = False

    def __init__(self):
        self.admin_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        self.web_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        self.case = None

    def read_json5(self, json_file, file_side='admin') -> None:
        test_data = []
        key_data = []
        if file_side == 'web':
            data_path = os.path.join(self.web_file_path, json_file)
        else:
            data_path = os.path.join(self.admin_file_path, json_file)

        with open(data_path, mode='r', encoding='utf8') as f:
            json_data = json5.load(f)
            for line in json_data:
                value1 = []
                key1 = []
                for k1, v1 in line.items():
                    if k1 != "test_item":
                        value1.append(v1)
                        key1.append(k1)
                    else:
                        for l1 in v1:
                            value2 = []
                            key2 = []
                            for k2, v2 in l1.items():
                                value2.append(v2)
                                key2.append(k2)
                            test_data.append(tuple(value1 + value2))
                            key_data.append(tuple(key1 + key2))  # 之後可能會用到
            test_case = []
            for i in range(len(key_data)):
                test_case.append(dict(zip(key_data[i], test_data[i])))
            self.case = test_case

    def get_case(self, target):
        if self.case is not None:
            testdata = []
            for i in self.case:
                if target == i["test_case"]:
                    testdata.append(i)
            return testdata
        else:
            raise ValueError("尚未載入Json檔案")

    @staticmethod
    def get_test_case(data, target):
        testdata = []
        for i in data:
            if target == i["test_case"]:
                testdata.append(i)
        return testdata

    @staticmethod
    def replace_json(json, target):
        json_copy = copy.deepcopy(json)  # 避免淺層複製導致case讀取有誤
        for key in list(target.keys()):

            value = target.get(key, "不存在")
            try:
                json_copy[key] = value
            except Exception:
                for item in json_copy:
                    item[key] = value
        return json_copy


class EnvReader:
    def __init__(self):
        self.__load_host()
        self.__load_API_headers()

    def __load_host(self):
        self.ADMIN_HOST = config['host']['admin_host']
        self.WEB_HOST = config["host"]['web_host']

    def __load_API_headers(self):
        self.ADMIN_HEADER = config['API_headers']['admin']
        self.WEB_HEADER = config['API_headers']['web']


# class ResponseVerification:
#     @staticmethod
#     def basic_assert(response, test_data):
#         assert response.status_code == test_data['code_status'], response.text
#         assert test_data['keyword'] in response.text
#         if response.status_code == 200:
#             assert validate_json(response.json(), test_data['schema'])
