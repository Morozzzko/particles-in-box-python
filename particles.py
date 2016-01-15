# -*- coding: utf-8 -*-

from sys import argv
from PySide import QtGui
from particles.gui import Ui_NewExperimentWindow


class NewExperimentWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NewExperimentWindow, self).__init__(parent=parent)

        # Set up UI
        self.ui = Ui_NewExperimentWindow()
        self.ui.setupUi(self)

        # Connect slots to signals
        self.ui.button_run.clicked.connect(self.run_simulation)

    def run_simulation(self):
        # TODO: actually do simulation
        box_width = self.ui.box_width.value()
        box_height = self.ui.box_height.value()
        delta_v_top = self.ui.delta_v_top.value()
        delta_v_bottom = self.ui.delta_v_bottom.value()
        delta_v_side = self.ui.delta_v_side.value()
        barrier_x = self.ui.barrier_x.value()
        barrier_width = self.ui.barrier_width.value()
        hole_y = self.ui.hole_y.value()
        hole_height = self.ui.hole_height.value()
        v_loss = self.ui.v_loss.value()
        particle_r = self.ui.particle_r.value()



if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    main_window = NewExperimentWindow()
    main_window.show()
    exit(app.exec_())
