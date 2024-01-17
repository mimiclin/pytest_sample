# -*- coding: utf-8 -*-
import requests
import json
import inspect
import datetime
from pylib.data_loader import EnvReader

env = EnvReader()
admin_host = env.ADMIN_HOST
admin_header = env.ADMIN_HEADER
web_host = env.WEB_HOST
web_header = env.WEB_HEADER


class ApiController:
    def __init__(self, platform):
        self.current_timestamp = str(int(datetime.datetime.now().timestamp()))
        self.request_session = requests.Session()
        self.platform = platform
        if self.platform == 'admin':
            self.host = admin_host
            self.request_session.headers = eval(admin_header)
        elif self.platform == 'web':
            self.host = web_host
            self.request_session.headers = eval(web_header)
        else:
            raise ValueError(f'Using wrong platform: {self.platform}\nOnly allow [admin] or [web]')

    @staticmethod
    def print_response(response):
        print('\n\n-------------- HTTPS response  *  begin ------------------')
        print(f'status code: {response.status_code}\n')

        print(f'Headers:')
        for k, v in response.headers.items():
            print(f'[{k}]: {v}')

        print('')
        response_text = json.loads(response.text)
        print(
            json.dumps(response_text,
                       sort_keys=True,
                       indent=4,
                       separators=(',', ': '),
                       ensure_ascii=False))
        print('-------------- HTTPS response  *  end ------------------\n\n')

    @staticmethod
    def print_payload(payload):
        print('\n\n-------------- Request payload ------------------')
        if payload['url']:
            print(f"[url]: {payload['url']}")
        if payload['json']:
            print(f"[json]: {json.dumps(payload['json'], indent=4)}")
        if payload['params']:
            print(f"[params]: {payload['params']}")
        print('--------------      Done       ------------------')

    def send_request(self, method, url, json=None, params=None, token=None, files=None):
        if token:
            self.request_session.headers.update({"Authorization": f"Bearer {str(token)}"})

        request_body = {
            "url": self.host + url,
            "json": json,
            "params": params,
            "files": files
        }

        self.print_payload(request_body)

        if method == 'post':
            response = self.request_session.post(**request_body)
        elif method == 'put':
            response = self.request_session.put(**request_body)
        elif method == 'get':
            response = self.request_session.get(**request_body)
        elif method == 'delete':
            response = self.request_session.delete(**request_body)
        else:
            response = "沒有符合的請求模式"

        self.print_response(response)

        return response


class KeywordArgument:
    @staticmethod
    def body_data(filter: list = None):
        if filter is None:
            filter = ['self', 'plat_token']
        caller = inspect.stack()[1][0]
        args, _, _, values = inspect.getargvalues(caller)
        r = dict()
        for i in args:
            if i not in filter and values[i] is not None:
                r[i] = values[i]
        return r
