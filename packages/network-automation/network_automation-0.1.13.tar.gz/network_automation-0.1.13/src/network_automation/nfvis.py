import json
import requests
from network_automation import environment

header = {
    "content-type": "application/vnd.yang.collection+json",
    "Accept": "application/vnd.yang.data+json",
}


class NFVISServer(object):
    """
    This represents a Cisco NFVIS server
    """
    def __init__(self, hostname, username=None, password=None, verify=True):
        if not hostname:
            raise ValueError("Hostname is missing")

        self.hostname = hostname
        self.url = 'https://' + hostname
        self.username = username or environment.get_cisco_username()
        self.password = password or environment.get_cisco_password()

        if not self.username or not self.password:
            raise ValueError("username/password is missing and could not be retrieved from environment variables")

        self.session = requests.Session()
        if not verify:
            self.session.verify = False

        self.session.auth = (self.username, self.password)

        self.platform = None
        self.get_platform_details()

    def get_platform_details(self):
        if self.platform:
            return self.platform

        uri = self.url + '/api/operational/platform-detail'
        try:
            resp = self.session.get(uri, headers=header)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not connect to {self.hostname}")

        self.platform = json.loads(resp.text)["platform_info:platform-detail"]

    def get_serial(self):
        try:
            return self.platform["hardware_info"]["SN"]
        except KeyError:
            return ""

    def get_pid(self):
        try:
            return self.platform["hardware_info"]["PID"]
        except KeyError:
            return ""

    def get_version(self):
        try:
            return self.platform["hardware_info"]["Version"]
        except KeyError:
            return ""

    def get_interfaces(self, detailed=False):
        if detailed:
            uri = self.url + '/api/operational/pnics?deep'
        else:
            uri = self.url + '/api/operational/pnics'

        try:
            resp = self.session.get(uri, headers=header)
        except requests.exceptions.ConnectionError:
            print("Could not get interface information")
            return None

        return json.loads(resp.text)["pnic:pnics"]["pnic"]

    def get_switch_interfaces(self, detailed=False):
        if detailed:
            uri = self.url + '/api/operational/switch/interface/status?deep'
        else:
            uri = self.url + '/api/operational/switch/interface/status'

        try:
            resp = self.session.get(uri, headers=header)
        except requests.exceptions.ConnectionError:
            print("Could not get switch interface information")
            return None

        if resp.status_code == 200:
            return json.loads(resp.text)["switch:status"]

        return []

    def get_switchport_status(self, detailed=False):
        if detailed:
            uri = self.url + '/api/operational/switch/interface/switchPort?deep'
        else:
            uri = self.url + '/api/operational/switch/interface/switchPort'

        try:
            resp = self.session.get(uri, headers=header)
        except requests.exceptions.ConnectionError:
            print("Could not get switchport information")
            return None

        if resp.status_code == 200:
            return json.loads(resp.text)["switch:switchPort"]

        return []
