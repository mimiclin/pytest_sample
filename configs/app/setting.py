import yaml
import os, sys
import uuid

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)
# import common.utils.globalvar as gl


class Setting:
    def get_yaml_conf(self):
        path = os.path.join(root_path, "configs/app/configs.yml")
        with open(path, 'r', encoding='utf-8') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg
    
    def get_device_conf(self):
        path = os.path.join(root_path, "configs/app/phone_config.yml")
        with open(path, 'r', encoding='utf-8') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg

    def get_phone_connect_link(self, phone_name, ip='', connect_type='local'):
        conf = self.get_device_conf()['Phone_conf']
        phone_platform = gl.get_value('PHONE_PLATFORM')
        if connect_type == 'remote':
            if phone_platform == 'Android':
                connection = f'Android://127.0.0.1:5037/{ip}'
            elif phone_platform == 'iOS':
                connection = f'ios:///http://{ip}:{conf[phone_name]["port"]}'
        else:
            if phone_platform == 'Android':
                connection = f'Android:///{conf[phone_name]["udid"]}'
            elif phone_platform == 'iOS':
                connection = f'ios:///http://127.0.0.1:{conf[phone_name]["port"]}' # 主機端預設位置
        
        return connection

    def get_package_name(self, brand, env='uat'):
        phone_platform = gl.get_value('PHONE_PLATFORM')
        if phone_platform == 'Android':
            package_type = 'package'
        elif phone_platform == 'iOS':
            package_type = 'bundle_id'
        package_name = self.get_yaml_conf()['channel'][brand][env][package_type]

        return package_name
    
    def get_poco_name(self):
        poco_name = self.get_yaml_conf()['channel']['common']['poco']['package']

        return poco_name

    def correct_phone_name(self, phone_name_fuzzy):
        conf = self.get_device_conf()['Phone_conf']
        phone_name_list = conf.keys()
        phone_name_fuzzy = phone_name_fuzzy.split('_')[-1]
        for name in phone_name_list:
            if phone_name_fuzzy == name.split('_')[-1]:
                correct_phone_name = name

        return correct_phone_name
    
    def get_phone_device_id(self, phone_name='', multiple=False):
        if multiple == True:
            conf = self.get_device_conf()['Phone_conf']
            device_id = conf[phone_name]['udid']
        else:
            device_id = uuid.uuid4()

        return str(device_id)
  