#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from PySide import QtGui
from particles.gui import Ui_NewExperimentWindow
from particles.simulation import Simulator
import datetime
import os.path


class NewExperimentWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NewExperimentWindow, self).__init__(parent=parent)

        # Set up UI
        self.ui = Ui_NewExperimentWindow()
        self.ui.setupUi(self)

        self.ui.output_file.setText(datetime.datetime.now().strftime("Particles_in_box_%Y-%m-%d_%H-%M-%S.bin"))

        # Connect slots to signals
        self.ui.button_run.clicked.connect(self.run_simulation)

        # File selection dialog
        self.ui.output_file_button.clicked.connect(self.set_output_file_path)

    def set_output_file_path(self):
        file_path, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save as:', filter="*.bin")
        self.ui.output_file.setText(file_path)

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
        g = self.ui.g.value()
        n_left = int(self.ui.n_left.value())
        n_right = int(self.ui.n_right.value())
        v_init = self.ui.v_init.value()
        fps = int(self.ui.fps.value())
        simulation_time = int(self.ui.simulation_time.value())
        file = self.ui.output_file.text()

        try:
            simulator = Simulator(box_width=box_width, box_height=box_height, delta_v_top=delta_v_top,
                                  delta_v_bottom=delta_v_bottom, delta_v_side=delta_v_side, barrier_x=barrier_x,
                                  barrier_width=barrier_width, hole_y=hole_y, hole_height=hole_height, v_loss=v_loss,
                                  particle_r=particle_r, n_left=n_left, n_right=n_right, v_init=v_init, g=g)
            num_states = simulation_time * 60 * fps

            dialog = QtGui.QProgressDialog("Simulating into " + os.path.basename(file),
                                           "Cancel",
                                           0,
                                           num_states)
            dialog.show()
            dialog.setValue(0)
            for state_num, _ in enumerate(simulator.simulate_to_file(file_path=file,
                                                        num_seconds=simulation_time * 60,
                                                        num_snapshots=fps,
                                                        write_head=True)):
                dialog.setValue(state_num)

        except IOError as e:
            QtGui.QMessageBox.critical(self, "Error!", str(e))
        except Exception as e:
            QtGui.QMessageBox.critical(self, "Error!", str(e))


if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    main_window = NewExperimentWindow()
    main_window.show()
    exit(app.exec_())
