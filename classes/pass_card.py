import nfc
from nfc.clf import RemoteTarget
from classes.srv_connection import Srv
from classes.utilities import Util


class Card:
    def get_device(self):
        try:
            clf = nfc.ContactlessFrontend('usb')
            device = clf.device
            clf.close()
            return str(device)
        except OSError:
            return -1

    def get_uid(self):
        try:
            clf = nfc.ContactlessFrontend('usb')
            # print("Waiting for NFC-tag...")
            tag = clf.connect(rdwr={'on-connect': lambda tag: False})
            target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
            tag_id = Util.parse_tag(Util(), target)
            clf.close()
            return tag_id
        except OSError:
            return -1

    def get_employee(self):
        uid = self.get_uid()
        if uid != -1:
            dec_uid = Util.convert_hex_to_decimal(Util(), uid)
            url = Srv.srv_address(Srv(), Srv.postfix_get)
            result = Srv.request_for_data(Srv(), url, dec_uid)
            if result != -1:
                employee = Util.parse_json(Util(), result)
                if employee != -1:
                    return employee
                else:
                    return str(dec_uid)
            else:
                return -2
        else:
            return -1

    def save_employee(self, *args):
        if len(args) == 3:
            emp = Util.create_json_card(Util(), args[0], args[1], args[2])
            return Srv.request_send_data(Srv(), emp)
        else:
            return "Wrong number of arguments"
