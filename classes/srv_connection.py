import requests
from PyQt5.QtCore import QSettings


class Srv:
    settings = QSettings("settings/preferences.ini", QSettings.IniFormat)
    protocol = settings.value("server_connection/protocol", defaultValue="http")
    address = settings.value("server_connection/address", defaultValue="192.168.0.14")
    port = settings.value("server_connection/port", defaultValue="5003")
    postfix_get = settings.value("server_connection/postfix_get", defaultValue="getbyid?card=")
    postfix_edit = settings.value("server_connection/postfix_post", defaultValue="edit")

    def load_preferences(self):
        settings = QSettings("settings/preferences.ini", QSettings.IniFormat)
        self.protocol = settings.value("server_connection/protocol", defaultValue="http")
        self.address = settings.value("server_connection/address", defaultValue="192.168.0.14")
        self.port = settings.value("server_connection/port", defaultValue="5003")
        self.postfix_get = settings.value("server_connection/postfix_get", defaultValue="getbyid?card=")
        self.postfix_edit = settings.value("server_connection/postfix_post", defaultValue="edit")

    def srv_address(self, postfix):
        self.load_preferences()
        return self.protocol + '://' + self.address + ':' + self.port + '/' + postfix

    def check_connection(self, url):
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            print("Connection established")
            return True
        except requests.ConnectionError:
            print("Couldn't establish network connection")
        except requests.exceptions.InvalidSchema:
            print("Invalid URL: {}".format(url))
        return False

    def request_for_data(self, url, arg):
        timeout = 5
        if self.check_connection(url):
            response = requests.get(url + str(arg), timeout=timeout)
            return response.json()
        else:
            print("Couldn't establish network connection")
        return -1

    def request_send_data(self, json_obj):
        url = self.srv_address(Srv.postfix_edit)
        response = requests.post(url, data=json_obj, headers={'Content-Type': 'application/json'})
        if response.status_code == requests.codes.ok:
            return "Request successfully posted. Code: {}".format(response.status_code)
        else:
            return "Request failed with state: {}".format(response.status_code)
