from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QPushButton, QLineEdit, QHBoxLayout, QFormLayout
from PyQt5.QtGui import QRegExpValidator, QIcon
from classes.work_threads import SaveThread, GetThread
from classes.preferences import Preferences


class MyWindow(QWidget):
    name_validator = QRegExpValidator(QRegExp("^[A-Z][a-z]+[ ][A-Z][.][A-Z][.]"))
    department_validator = QRegExpValidator(QRegExp("^[A-Z][A-Za-z]+"))
    device_flag = False

    def closeEvent(self, event):
        msg_title = 'Close application'
        msg_body = 'Do you really want to quit?'
        reply = QMessageBox.question(self, msg_title, msg_body,
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_field_modify(self):
        if self.lineName.isModified() or self.lineDepartment.isModified():
            self.buttonCancel.setDisabled(False)

    def on_cancel_clicked(self):
        self.lineDepartment.clear()
        self.lineName.clear()
        self.statusbar.setText("Ready")
        self.buttonCancel.setDisabled(True)

    def save_changes(self):
        card_values = [self.lineUID.text(), self.lineName.text(), self.lineDepartment.text()]
        self.savethread = SaveThread(card_values)
        self.savethread.save_signal.connect(self.on_save_response, Qt.QueuedConnection)
        self.buttonSave.setDisabled(True)
        self.savethread.start()

    def on_save_clicked(self):
        if self.lineUID.text() == "":
            self.statusbar.setText("Empty UID")
        elif self.lineDepartment.text() == "" and self.lineName.text() == "":
            result = QMessageBox.warning(window, "Delete employee",
                                          "Saving card without name and department "
                                          "will be delete cardholder from database if exists. Are you sure?",
                                          buttons=QMessageBox.Yes | QMessageBox.Cancel,
                                          defaultButton=QMessageBox.Cancel)
            if result == QMessageBox.Yes:
                self.save_changes()
            else:
                self.statusbar.setText("Cancelled")
        elif self.lineDepartment.text() == "" or self.lineName.text() == "":
            self.statusbar.setText("Some fields are empty")
        else:
            self.save_changes()

    def on_save_response(self, resp):
        self.statusbar.setText(resp)
        self.buttonSave.setDisabled(False)

    def on_read_finished(self):
        self.buttonCancel.setDisabled(False)

    def on_clicked(self):
        self.buttonRead.setDisabled(True)
        self.mythread.start()

    def on_started(self):
        self.statusbar.setText("Waiting for NFC-tag...")

    def on_finished(self):
        self.buttonRead.setDisabled(False)
        self.buttonCancel.setDisabled(False)

    def on_change(self, obj):
        self.statusbar.setText("Ready")
        self.lineUID.setText(obj['card'])
        self.lineDepartment.setText(obj['department'])
        self.lineName.setText(obj['employee'])

    def on_empty(self, s):
        self.statusbar.setText('Card not used before')
        self.lineUID.setText(s)
        self.lineDepartment.clear()
        self.lineName.clear()
        self.buttonCancel.setDisabled(True)

    def on_error(self, error_code):
        self.lineUID.clear()
        self.lineDepartment.clear()
        self.lineName.clear()
        if error_code == 1:
            self.statusbar.setText('Compatible device not found')
        elif error_code == 2:
            self.statusbar.setText("Couldn't establish network connection")

    def on_device_connect(self, s):
        if s != -1:
            self.statusbar.setText(s)
            self.device_flag = True
        else:
            self.statusbar.setText('Compatible device not found')
            self.device_flag = False

    def open_preferences(self):
        self.pref.show()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.lineUID = QLineEdit()
        self.lineUID.setReadOnly(True)

        self.lineName = QLineEdit()
        self.lineName.setMaxLength(30)
        self.lineName.setPlaceholderText("Ivanov B.C.")
        self.lineName.setValidator(self.name_validator)
        self.lineName.textChanged.connect(self.on_field_modify)

        self.lineDepartment = QLineEdit()
        self.lineDepartment.setMaxLength(20)
        self.lineDepartment.setPlaceholderText("Sales")
        self.lineDepartment.setValidator(self.department_validator)
        self.lineDepartment.textChanged.connect(self.on_field_modify)

        self.statusbar = QLineEdit()
        self.statusbar.setDisabled(True)
        self.statusbar.setText("Ready")
        self.statusbar.setAlignment(Qt.AlignLeft)

        self.buttonRead = QPushButton("&Read")
        self.buttonRead.setFixedHeight(30)
        self.buttonRead.clicked.connect(self.on_clicked)

        self.buttonSave = QPushButton("&Save")
        self.buttonSave.setFixedHeight(30)
        self.buttonSave.clicked.connect(self.on_save_clicked)

        self.buttonCancel = QPushButton("&Clear")
        self.buttonCancel.setFixedHeight(30)
        self.buttonCancel.clicked.connect(self.on_cancel_clicked)
        self.buttonCancel.setDisabled(True)

        self.buttonPreferences = QPushButton("&Preferences")
        self.buttonPreferences.clicked.connect(self.open_preferences)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.buttonRead)
        self.hbox.addWidget(self.buttonSave)
        self.hbox.addWidget(self.buttonCancel)

        self.form = QFormLayout()
        self.form.addRow("Card &ID:", self.lineUID)
        self.form.addRow("&Employee:", self.lineName)
        self.form.addRow("&Department:", self.lineDepartment)
        self.form.addRow(" ", None)
        self.form.addRow(self.hbox)
        self.form.addRow(" ", None)
        self.form.addRow("Status:", self.statusbar)
        self.form.addRow(" ", None)
        self.form.addRow(self.buttonPreferences)

        self.setLayout(self.form)

        self.mythread = GetThread()
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.normalsignal.connect(self.on_change, Qt.QueuedConnection)
        self.mythread.emptysignal.connect(self.on_empty, Qt.QueuedConnection)
        self.mythread.errorsignal.connect(self.on_error, Qt.QueuedConnection)

        self.pref = Preferences()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("ZTTA PACS")
    window.setWindowIcon(QIcon('assets/icon.png'))
    # app.setWindowIcon(QIcon('icon.png'))
    window.setFixedSize(350, 260)
    desktop = QApplication.desktop()
    x = (desktop.width() - window.width()) / 2
    y = (desktop.height() - window.height()) / 3
    window.move(x, y)
    window.show()
    sys.exit(app.exec_())


































