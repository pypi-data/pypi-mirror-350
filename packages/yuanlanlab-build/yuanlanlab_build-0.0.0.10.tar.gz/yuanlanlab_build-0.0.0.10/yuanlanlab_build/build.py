import http.client
import time
import yaml
import json

_CONFIG = {}


class Build:
    def __init__(self, main_module):
        self.main_module = main_module
        self.build()

    def init_config(self):
        global _CONFIG
        for item in dir(self.main_module):
            if item.startswith('YL_'):
                _CONFIG[item[3:]] = getattr(self.main_module, item)

        if 'METHOD' not in _CONFIG:
            _CONFIG['METHOD'] = 'HTTPS'

        _CONFIG['HEADERS'] = {}
        _CONFIG['HEADERS']['User-Agent'] = _CONFIG.get('HEADERS_USER_AGENT')
        _CONFIG['HEADERS'].update(**_CONFIG.get('HEADERS_X'))

    def get_url_path(self, resource):
        grade = resource.get('g', '1')
        grade = _CONFIG['URL_BASE'].get(grade, '')
        grade = grade[:-1]

        txt1 = resource['id']
        txt2 = resource['v']
        txt3 = resource['f']

        txts = [grade, txt1, txt2, txt3]
        result = '/'.join(txts)
        return result

    def get_content(self, url_path, attempts=3):
        for _ in range(attempts):
            try:
                body = json.dumps(_CONFIG['PAYLOAD'])
                if _CONFIG['METHOD'] == 'HTTPS':
                    connection = http.client.HTTPSConnection(_CONFIG['HOST'])
                else:
                    connection = http.client.HTTPConnection(_CONFIG['HOST'])
                connection.request('POST', url_path, headers=_CONFIG['HEADERS'], body=body)

                response = connection.getresponse()
                if response.status != 200:
                    raise UserWarning
                else:
                    content = response.read().decode()
                    return content
            except http.client.HTTPException as e:
                print(f'HTTP错误，正在重试: {e}')
                time.sleep(2)
            except Exception as e:
                print(f'发生异常: {e}')
                time.sleep(2)

    def get_code(self):
        url_path = self.get_url_path(_CONFIG['URL_CODE'])
        content = self.get_content(url_path)
        return content

    def get_resources(self):
        resources = []
        for url_file in _CONFIG['URL_FILES']:
            url_path = self.get_url_path(url_file)
            content = self.get_content(url_path)
            requirement_content = yaml.load(content, Loader=yaml.SafeLoader)

            requirement_list = []
            for item in ['builds', 'deps']:
                requirement = requirement_content.get(item, [])
                if requirement:
                    requirement_list.extend(requirement)
            resources.extend(requirement_list)
        return resources

    def build(self):
        self.init_config()

        code = self.get_code()
        _CONFIG['RESOURCES'] = self.get_resources()
        exec(code, {'CONFIG': _CONFIG})
