# -*- coding: utf-8 -*-
from typing import Any
from pylib.data_loader import EnvReader
from pylib.api import ApiController

env = EnvReader()
web_host = env.WEB_HOST


class WebApi(ApiController):
    def __init__(self, token=None):
        super().__init__(platform='web')
        if token:
            self.request_session.headers.update({"token": token})

    def login(self,
              country: str = None,
              device_id: str = None,
              grant_type: str = None,
              password: str = None,
              phone: str = None) -> Any:

        if not country:
            country = "CN"
        if not phone:
            phone = "862260000001"
        if not password:
            password = "abc12345"
        if not device_id:
            device_id = "d520c7a8-421b-4563-b955-f5abc56b97ec-0246991"
        if not grant_type:
            grant_type = "password"

        request_body = {
            "method": "post",
            "url": "/api/v1/login",
            "json": {
                "country": country,
                "phone": phone,
                "password": password,
                "device_id": device_id,
                "grant_type": grant_type
            }
        }

        response = self.send_request(**request_body)
        return response
