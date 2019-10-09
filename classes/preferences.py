from PyQt5.QtWidgets import QWidget, QFormLayout, QApplication, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSettings


class Preferences(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.settings = QSettings("settings/preferences.ini", QSettings.IniFormat)
        self.defaults = QSettings("settings/default.ini", QSettings.IniFormat)

        self.setWindowTitle("Preferences")
        self.setFixedSize(300, 230)
        layout = QFormLayout()
        desktop = QApplication.desktop()
        x = (desktop.width() - self.width()) / 2
        y = (desktop.height() - self.height()) / 3
        self.move(x, y)

        self.lineProtocol = QLineEdit()
        self.lineProtocol.textChanged.connect(self.on_field_modify)
        self.lineAddress = QLineEdit()
        self.lineAddress.textChanged.connect(self.on_field_modify)
        self.linePort = QLineEdit()
        self.linePort.textChanged.connect(self.on_field_modify)
        self.linePostfixGet = QLineEdit()
        self.linePostfixGet.textChanged.connect(self.on_field_modify)
        self.linePostfixPost = QLineEdit()
        self.linePostfixPost.textChanged.connect(self.on_field_modify)

        self.buttonDefaults = QPushButton("Default")
        self.buttonDefaults.setFixedHeight(30)
        self.buttonDefaults.clicked.connect(self.on_default)
        self.buttonDefaults.setDisabled(True)
        self.buttonSave = QPushButton("Save")
        self.buttonSave.setFixedHeight(30)
        self.buttonSave.clicked.connect(self.on_save_click)
        self.buttonSave.setDisabled(True)

        self.butbox = QHBoxLayout()
        self.butbox.addWidget(self.buttonDefaults)
        self.butbox.addWidget(self.buttonSave)

        layout.addRow("Protocol:", self.lineProtocol)
        layout.addRow("Address:", self.lineAddress)
        layout.addRow("Port:", self.linePort)
        layout.addRow("Postfix GET:", self.linePostfixGet)
        layout.addRow("Postfix POST:", self.linePostfixPost)
        layout.addRow(" ", None)
        layout.addRow(self.butbox)

        self.setLayout(layout)
        self.on_load()

    def on_load(self):
        self.lineProtocol.setText(self.settings.value("server_connection/protocol"))
        self.lineAddress.setText(self.settings.value("server_connection/address"))
        self.linePort.setText(self.settings.value("server_connection/port"))
        self.linePostfixGet.setText(self.settings.value("server_connection/postfix_get"))
        self.linePostfixPost.setText(self.settings.value("server_connection/postfix_post"))

    def on_default(self):
        self.lineProtocol.setText(self.defaults.value("server_connection/protocol", defaultValue="http"))
        self.lineAddress.setText(self.defaults.value("server_connection/address", defaultValue="192.168.0.14"))
        self.linePort.setText(self.defaults.value("server_connection/port", defaultValue="5003"))
        self.linePostfixGet.setText(self.defaults.value("server_connection/postfix_get", defaultValue="getbyid?card="))
        self.linePostfixPost.setText(self.defaults.value("server_connection/postfix_post", defaultValue="edit"))
        self.buttonDefaults.setDisabled(True)
        if not self.buttonSave.isEnabled():
            self.buttonSave.setDisabled(False)

    def on_save_click(self):
        self.settings.beginGroup("server_connection")
        self.settings.setValue("protocol", self.lineProtocol.text())
        self.settings.setValue("address", self.lineAddress.text())
        self.settings.setValue("port", self.linePort.text())
        self.settings.setValue("postfix_get", self.linePostfixGet.text())
        self.settings.setValue("postfix_post", self.linePostfixPost.text())
        self.settings.endGroup()
        self.buttonSave.setDisabled(True)
        print("Saved")

    def on_field_modify(self):
        if self.lineProtocol.isModified() or self.lineAddress.isModified() or self.linePort.isModified() \
                or self.linePostfixGet.isModified() or self.linePostfixPost.isModified():
            self.buttonSave.setDisabled(False)
            self.buttonDefaults.setDisabled(False)
