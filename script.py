import requests
import hashlib
import base64

from typing import Any, Dict


class Modem:
    def __init__(self, host: str):
        self.session = requests.Session()
        self.host = host

    def login(self, pwd: str):
        encoded = base64.encodebytes(pwd.encode('utf-8')).strip()
        data = {'isTest': False,
                'goformId': 'LOGIN',
                'password': encoded.decode('ascii'),
                }
        headers = {'Referer': f'http://{self.host}/index.html'}
        url = f'http://{self.host}/goform/goform_set_cmd_process'
        r = self.session.post(url, headers=headers, data=data)
        r.raise_for_status()
        self._get_fields()

    def _get(self, args) -> Dict[str, Any]:
        headers = {'Referer': f'http://{self.host}/index.html'}
        url = f'http://{self.host}/goform/goform_get_cmd_process'
        params = {'isTest': False, **args}
        r = self.session.get(url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        return data

    def _get_fields(self):
        params = {'multi_data': 1, 'cmd': 'Language,cr_version,wa_inner_version,RD'}
        data = self._get(params)
        rd = data['RD']
        cr_version = data['cr_version']
        wa_inner_version = data['wa_inner_version']
        prefix_hash = hashlib.md5((cr_version + wa_inner_version).encode('utf-8')).hexdigest()
        self.ad = hashlib.md5((prefix_hash + rd).encode('utf-8')).hexdigest()

    def is_wan_up(self) -> bool:
        params = {'multi_data': 1,
                  'sms_received_flag_flag': 0,
                  'sts_received_flag_flag': 0,
                  'sms_db_change_flag': 0,
                  'cmd': 'modem_main_state,wan_connect_status'}
        data = self._get(params)
        modem_state = data.get("modem_main_state")
        wan_state = data.get("wan_connect_status")
        return modem_state == "modem_init_complete" and wan_state == "pdp_connected"

    def set_wan_up(self):
        headers = {'Referer': f'http://{self.host}/index.html'}
        url = f'http://{self.host}/goform/goform_set_cmd_process'
        data = {'isTest': False,
                'notCallback': True,
                'goformId': 'CONNECT_NETWORK',
                'AD': self.ad}
        r = self.session.post(url, headers=headers, data=data)
        r.raise_for_status()
        data = r.json()
        assert data["result"] != "failure", data
