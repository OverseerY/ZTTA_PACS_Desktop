from PyQt5.QtCore import QThread, pyqtSignal
from classes.pass_card import Card


class GetThread(QThread):
    normalsignal = pyqtSignal(dict)
    emptysignal = pyqtSignal(str)
    errorsignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        emp = Card.get_employee(Card())
        if emp == -1:
            self.errorsignal.emit(1)
        elif emp == -2:
            self.errorsignal.emit(2)
        else:
            if type(emp) != str:
                self.normalsignal.emit(emp)
            else:
                self.emptysignal.emit(emp)


class SaveThread(QThread):
    save_signal = pyqtSignal(str)

    def __init__(self, value, parent=None):
        QThread.__init__(self, parent)
        self.value = value

    def run(self):
        result = Card.save_employee(Card(), self.value[0], self.value[1], self.value[2])
        self.save_signal.emit(str(result))
        self.exec_()
