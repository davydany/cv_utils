import sys
from PyQt4 import QtGui
from cvutils.gui.cascade_classifier_trainer import CascadeTrainer

class MainWindow(QtGui.QMainWindow):

    actions = (
        ('file__new__cascade_classifier_training_project', 'Cascade Classifier Training Project', None),
        ('file__quit', '&Quit', 'Ctrl+Q'),
    )

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.statusBar().showMessage("Ready!")
        self.setWindowTitle("CV Utilities")
        self.showMaximized()
        self.show()
        self.raise_()

        # setup menu
        self.init_actions()
        self.init_menu()


    def init_actions(self):

        for action in MainWindow.actions:

            action_value = QtGui.QAction(action[1], self,
                                         triggered=getattr(self, 'run_%s' % action[0]))
            if action[2]: action_value.setShortcut(action[2])
            setattr(self, action[0], action_value)

    def init_menu(self):

        menubar = self.menuBar()

        ## create and populate "File" menu
        # create menu items
        self.file_menu = QtGui.QMenu("&Project", self)
        self.file_new_menu = QtGui.QMenu("&New", self)
        self.file_open_menu = QtGui.QMenu("&Open", self)

        # populate with actions
        self.file_new_menu.addAction(self.file__new__cascade_classifier_training_project)

        # add menu items to main menubar
        self.file_menu.addMenu(self.file_new_menu)
        self.file_menu.addMenu(self.file_open_menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.file__quit)

        menubar.addMenu(self.file_menu)


    def run_file__new__cascade_classifier_training_project(self):

        trainer = CascadeTrainer(self)
        trainer.show()




    def run_file__quit(self):

        sys.exit(0)


def main():

    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()