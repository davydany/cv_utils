from PyQt4 import QtGui


class CascadeTrainer(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CascadeTrainer, self).__init__(parent)

        self.button = QtGui.QPushButton("Hello WOrld!", self)


        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

        self.setLayout(layout)
