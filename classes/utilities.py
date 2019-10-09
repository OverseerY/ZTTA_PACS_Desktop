import json
from PyQt5.QtWidgets import QMessageBox


class Util:
    def get_root_key(self, obj):
        keys = []
        for k in obj.keys():
            keys.append(k)
        return keys[0]

    def parse_tag(self, value):
        arr = str(value).split(' ')
        for item in arr:
            if item.find("sdd_res=") != -1:
                return item.replace('sdd_res=', '')
        return -1

    def convert_hex_to_decimal(self, value):
        arr = list(value)
        new_arr = []
        for i in range(0, len(arr), 2):
            pair = ''
            pair += arr[i]
            pair += arr[i + 1]
            new_arr.insert(i, pair)
        new_arr.reverse()
        separator = ''
        result = int(separator.join(new_arr), 16)
        return result

    def parse_json(self, json_obj):
        employee = json_obj[self.get_root_key(json_obj)]
        if not employee:
            return -1
        else:
            return employee[0]

    def create_json_card(self, uid, name, department):
        obj = {
            "card": uid,
            "name": name,
            "dept": department
        }

        json_obj = json.dumps(obj, ensure_ascii=False).encode('utf8')
        return json_obj

    def custom_message(self, msg, box_type):
        alert = QMessageBox()
        if box_type == 1:
            alert.setIcon(QMessageBox.Question)
        elif box_type == 2:
            alert.setIcon(QMessageBox.Warning)
        elif box_type == 3:
            alert.setIcon(QMessageBox.Critical)
        elif box_type == 4:
            alert.setIcon(QMessageBox.Question)
        else:
            alert.setIcon(QMessageBox.Information)

        # alert.setWindowIcon(QIcon('icon.png'))
        alert.setText(msg)
        alert.exec_()
