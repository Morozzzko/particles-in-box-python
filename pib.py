#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from PySide import QtGui, QtCore
from PySide.QtOpenGL import QGLWidget
from particles.gui import Ui_NewExperimentWindow, Ui_DemonstrationWindow
from particles.simulation import Simulator, Playback
from OpenGL.GL import (glShadeModel, glClearColor, glClearDepth, glEnable,
                       glMatrixMode, glDepthFunc, glHint, glOrtho,
                       glViewport, glLoadIdentity, glClear,
                       glColor3f, glLineWidth,
                       GL_SMOOTH, GL_DEPTH_TEST, GL_PROJECTION, GL_LEQUAL,
                       GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST,
                       GL_MODELVIEW, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       GL_TRIANGLE_FAN, GL_LINE_STRIP, GL_VERTEX_ARRAY,
                       glEnableClientState, GL_DOUBLE, glVertexPointer,
                       glDrawArrays, glColorPointer, GL_UNSIGNED_BYTE,
                       GL_COLOR_ARRAY, glDisableClientState)
import OpenGL.arrays.vbo as glvbo
import datetime
import os.path
import struct
import argparse
import numpy as np
import signal
import subprocess
import threading
import collections
from math import sin, cos, radians, pi

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
EXEC_CMD = os.path.join(BASE_PATH, "pib-generate")


def read_from_pipe(process, append_func):
    for line in iter(process.stdout.readline, ""):
        append_func(line)


def simulate(box_width: float, box_height: float,
             delta_v_top: float, delta_v_bottom: float,
             delta_v_side: float,
             barrier_x: float, barrier_width: float, hole_y: float,
             hole_height: float,
             min_to_simulate: int,
             output_file: str,
             v_loss: float, particle_r: float,
             deque: collections.deque,
             n_left: int = 500, n_right: int = 500,
             v_init: float = 0.0,
             g: float = 9.8,
             fps: int = 30,
             ):
    params = [str(x) for x in (n_left, n_right, particle_r, v_init, v_loss,
                               box_width, box_height, barrier_x, barrier_width,
                               hole_y, hole_height, delta_v_top,
                               delta_v_bottom, delta_v_side, g,
                               min_to_simulate, fps, output_file)]
    process = subprocess.Popen([EXEC_CMD] + params, stdout=subprocess.PIPE,
                               bufsize=1, universal_newlines=True)
    t = threading.Thread(target=read_from_pipe, args=(process, deque.append))
    t.daemon = True
    t.start()
    return process


class ParticleWidget(QGLWidget):
    COLOR_LEFT = (255, 0, 0)
    COLOR_RIGHT = (0, 255, 0)

    def __init__(self, playback, parent=None):
        super(ParticleWidget, self).__init__(parent=parent)
        self.playback = playback
        particle_r = playback.simulator.particle_r

        self.xy_offset = np.vstack((
            np.array([(particle_r * cos(radians(x)),
                       particle_r * sin(radians(x)))
                      for x in range(0, 361, 45)]),
            (0, 0)
        ))

        self.xy_size = self.xy_offset.shape[0]

        self.update_particle_data()

        self.initializeGL()

        self.paintGL()

    def initializeGL(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClearDepth(1.0)

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        self.vbo_xy = glvbo.VBO(self.particle_xy)
        self.vbo_color = glvbo.VBO(self.particle_color)
        simulator = self.playback.simulator
        self.vbo_barrier = glvbo.VBO(np.array([
            simulator.barrier_x_left, simulator.box_height,
            simulator.barrier_x_left, simulator.hole_y_top,
            simulator.barrier_x_right, simulator.hole_y_top,
            simulator.barrier_x_right, simulator.box_height,
            simulator.barrier_x_left, 0,
            simulator.barrier_x_left, simulator.hole_y_bottom,
            simulator.barrier_x_right, simulator.hole_y_bottom,
            simulator.barrier_x_right, 0,
        ]))

    def update_particle_data(self):
        self.particle_xy = np.array([(p.pos_x + x, p.pos_y + y)
                                     for p in
                                     self.playback.simulator.particles
                                     for (x, y) in self.xy_offset])
        self.particle_color = np.array([x
                                        for p in
                                        self.playback.simulator.particles
                                        for i in range(self.xy_size)
                                        for x in
                                        (self.COLOR_RIGHT if p.id & 1
                                         else self.COLOR_LEFT)
                                        ], dtype=np.ubyte)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        glOrtho(0.0, self.playback.simulator.box_width,
                0.0, self.playback.simulator.box_height,
                0.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def clearGL(self):
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def deleteBuffers(self):
        self.vbo_color.unbind()
        self.vbo_barrier.unbind()
        self.vbo_xy.unbind()
        del self.vbo_color
        del self.vbo_barrier
        del self.vbo_xy

    def paintGL(self):
        self.clearGL()
        glLoadIdentity()

        simulator = self.playback.simulator

        self.update_particle_data()

        glEnableClientState(GL_COLOR_ARRAY)

        self.vbo_color.set_array(self.particle_color)
        self.vbo_color.bind()
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.vbo_color)
        self.vbo_color.unbind()

        glEnableClientState(GL_VERTEX_ARRAY)

        self.vbo_xy.set_array(self.particle_xy)
        self.vbo_xy.bind()

        glVertexPointer(2, GL_DOUBLE, 0, self.vbo_xy)

        particle_size = self.xy_size

        for i in range(len(simulator)):
            glDrawArrays(GL_TRIANGLE_FAN, i * particle_size, particle_size)

        glDisableClientState(GL_COLOR_ARRAY)
        self.vbo_xy.unbind()

        glColor3f(1, 1, 1)
        glLineWidth(2)
        self.vbo_barrier.bind()
        glVertexPointer(2, GL_DOUBLE, 0, self.vbo_barrier)
        glDrawArrays(GL_LINE_STRIP, 0, 4)
        glDrawArrays(GL_LINE_STRIP, 4, 4)
        self.vbo_barrier.unbind()

    def on_render_scene(self):
        self.paintGL()
        self.updateGL()


class DemonstrationWindow(QtGui.QMainWindow):
    def __init__(self, file_name, parent=None):
        super(DemonstrationWindow, self).__init__(parent=parent)

        self.playback = Playback(file_name)

        self.ui = Ui_DemonstrationWindow()

        self.ui.setupUi(self)

        self.label_time_original = self.ui.label_time.text()

        self.ui.canvas = ParticleWidget(self.playback,
                                        parent=self.ui.frame_player)
        self.ui.canvas.setFixedSize(self.ui.frame_player.size())

        self.ui.current_state.setMaximum(len(self.playback))

        self.ui.button_play.clicked.connect(self.on_button_play_pressed)

        self.stopped = False

        self.timer = QtCore.QTimer(parent=self)
        self.timer.timeout.connect(self.on_timer_executed)

        self.ui.current_state.sliderPressed.connect(
            self.on_scrollbar_pressed)
        self.ui.current_state.sliderReleased.connect(
            self.on_scrollbar_released)
        self.ui.current_state.valueChanged.connect(
            self.on_scrollbar_value_changed)

        self.ui.button_backward.clicked.connect(self.previous_state)
        self.ui.button_forward.clicked.connect(self.next_state)

        self.ui.plot_maxwell.setTitle("Maxwell distribution")
        self.ui.plot_maxwell.setLabel('bottom', 'Speed', units='m/s')
        self.ui.plot_maxwell.setLabel('left', 'Number of particles',
                                      units='')

        self.ui.plot_boltzmann.setTitle("Boltzmann distribution")
        self.ui.plot_boltzmann.setLabel('bottom', 'height', units='m')
        self.ui.plot_boltzmann.setLabel('left', 'Number of particles',
                                        units='')

        self.start_playback()

    def closeEvent(self, *args, **kwargs):
        self.ui.canvas.deleteBuffers()

    def stop_playback(self):
        self.stopped = True
        self.ui.button_play.setText("▷")
        self.timer.stop()

    def launch_timer(self):
        fps = self.ui.fps.value()
        time_step = int(1000 / fps)
        self.timer.start(time_step)

    def start_playback(self):
        self.stopped = False
        self.launch_timer()
        self.ui.button_play.setText("▯▯")

    def update_boltzmann_plot(self, data):
        self.ui.plot_boltzmann.clear()
        data_sorted = sorted((x.pos_y for x in data), reverse=True)
        y, x = np.histogram(data_sorted, bins=20, density=True)
        self.ui.plot_boltzmann.plot(x, y, stepMode=True, fillLevel=0,
                                    brush=(126, 5, 80, 150))

    def update_maxwell_plot(self, data):
        self.ui.plot_maxwell.clear()
        data_sorted = sorted((x.speed() for x in data), reverse=True)
        y, x = np.histogram(data_sorted, bins=20, density=True)
        self.ui.plot_maxwell.plot(x, y, stepMode=True, fillLevel=0,
                                  brush=(126, 5, 80, 150))

        v_probable = x[np.argmax(y)]
        offset = np.max(np.diff(x)) / 2

        k = 4 / np.sqrt(pi) * ((1 / v_probable) ** 3)

        y_theoretical = np.array(
            [k * (val * val) * np.exp(-(val * val) / (v_probable * v_probable))
             for val in x])

        self.ui.plot_maxwell.plot(np.add(x, offset), y_theoretical,
                                  stepMode=False,
                                  brush=(255, 255, 255, 255))

    def update_plot(self, data):
        """
        Update plots

        This method is used to call other methods that are handling
        plotting of specific data, i.e. Maxwell or Botlzmann distribution
        Data passed to this method is a copy of original particle, so any
        manipulation is safe

        :param data:
        :return:
        """
        self.update_maxwell_plot(data)
        self.update_boltzmann_plot(data)

    def previous_state(self):
        try:
            self.ui.current_state.setValue(
                self.ui.current_state.value() - 1)
        except (IOError, struct.error, ValueError) as err:
            self.stop_playback()

    def next_state(self):
        try:
            self.ui.current_state.setValue(
                self.ui.current_state.value() + 1)
        except (IOError, struct.error, ValueError) as err:
            self.stop_playback()

    def on_timer_executed(self):
        if self.stopped or self.sender() != self.timer:
            return
        self.next_state()
        self.launch_timer()

    def on_button_play_pressed(self):
        if self.stopped:
            self.start_playback()
        else:
            self.stop_playback()

    def on_scrollbar_pressed(self):
        self.timer.stop()

    def on_scrollbar_released(self):
        if not self.stopped:
            self.launch_timer()

    def on_scrollbar_value_changed(self, new_state):
        try:
            self.playback.set_state(new_state)
            self.ui.canvas.on_render_scene()
            self.ui.label_time.setText(
                self.label_time_original.format(
                    time=self.playback.simulator.time_elapsed
                )
            )
            self.update_plot(self.playback.simulator.state())
        except (IOError, ValueError):
            pass


class NewExperimentWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NewExperimentWindow, self).__init__(parent=parent)

        # Set up UI
        self.ui = Ui_NewExperimentWindow()
        self.ui.setupUi(self)

        self.ui.label_clear_file_name.setVisible(False)
        self.label_input_text = self.ui.label_input_file_name.text()
        self.input_file = None

        self.ui.label_input_file_name.mouseReleaseEvent = self.set_input_file_path_on_click
        self.ui.label_clear_file_name.mouseReleaseEvent = self.clear_input_file_path_on_click

        self.ui.output_file.setText(datetime.datetime.now().strftime(
            "particles_in_box_%Y-%m-%d-%H-%M.bin"))

        # Connect slots to signals
        self.ui.button_run.clicked.connect(self.run_simulation)

        # File selection dialog
        self.ui.output_file_button.clicked.connect(
            self.set_output_file_path)

    def set_input_file(self, file_path):
        self.input_file = file_path
        if file_path:
            self.ui.label_clear_file_name.setVisible(True)
            self.ui.label_input_file_name.setText(
                "Opening file: {file_path}".format(
                    file_path=os.path.basename(file_path))
            )
            self.ui.box_width.setEnabled(False)
            self.ui.box_height.setEnabled(False)
            self.ui.delta_v_top.setEnabled(False)
            self.ui.delta_v_bottom.setEnabled(False)
            self.ui.delta_v_side.setEnabled(False)
            self.ui.barrier_x.setEnabled(False)
            self.ui.barrier_width.setEnabled(False)
            self.ui.hole_y.setEnabled(False)
            self.ui.hole_height.setEnabled(False)
            self.ui.v_loss.setEnabled(False)
            self.ui.particle_r.setEnabled(False)
            self.ui.g.setEnabled(False)
            self.ui.n_left.setEnabled(False)
            self.ui.n_right.setEnabled(False)
            self.ui.v_init.setEnabled(False)
            self.ui.fps.setEnabled(False)
            self.ui.simulation_time.setEnabled(False)
            self.ui.output_file.setEnabled(False)
            self.ui.output_file_button.setEnabled(False)
        else:
            self.ui.label_input_file_name.setText(self.label_input_text)
            self.ui.label_clear_file_name.setVisible(False)
            self.ui.box_width.setEnabled(True)
            self.ui.box_height.setEnabled(True)
            self.ui.delta_v_top.setEnabled(True)
            self.ui.delta_v_bottom.setEnabled(True)
            self.ui.delta_v_side.setEnabled(True)
            self.ui.barrier_x.setEnabled(True)
            self.ui.barrier_width.setEnabled(True)
            self.ui.hole_y.setEnabled(True)
            self.ui.hole_height.setEnabled(True)
            self.ui.v_loss.setEnabled(True)
            self.ui.particle_r.setEnabled(True)
            self.ui.g.setEnabled(True)
            self.ui.n_left.setEnabled(True)
            self.ui.n_right.setEnabled(True)
            self.ui.v_init.setEnabled(True)
            self.ui.fps.setEnabled(True)
            self.ui.simulation_time.setEnabled(True)
            self.ui.output_file.setEnabled(True)
            self.ui.output_file_button.setEnabled(True)

    def set_input_file_path_on_click(self, ev):
        file_path, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open:',
                                                         filter="*.bin")
        self.set_input_file(file_path or None)

    def clear_input_file_path_on_click(self, ev):
        self.set_input_file(None)

    def set_output_file_path(self):
        file_path, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save as:',
                                                         filter="*.bin")
        self.ui.output_file.setText(file_path)

    def run_simulation(self):
        if self.input_file:
            demo_window = DemonstrationWindow(self.input_file, parent=self)
            demo_window.show()
            self.hide()
            return

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
        n_left = self.ui.n_left.value()
        n_right = self.ui.n_right.value()
        v_init = self.ui.v_init.value()
        fps = self.ui.fps.value()
        min_to_simulate = self.ui.simulation_time.value()
        output_file = self.ui.output_file.text()

        try:
            self.dialog = QtGui.QProgressDialog(
                "Simulating into " + os.path.basename(output_file),
                "Cancel",
                0,
                min_to_simulate * 60)
            self.dialog.show()
            self.dialog.setValue(0)
            self.progress = collections.deque(maxlen=1)

            self.simulator = simulate(n_left=n_left,
                                      n_right=n_right,
                                      particle_r=particle_r,
                                      v_init=v_init,
                                      v_loss=v_loss,
                                      box_width=box_width,
                                      box_height=box_height,
                                      barrier_x=barrier_x,
                                      barrier_width=barrier_width,
                                      hole_y=hole_y,
                                      hole_height=hole_height,
                                      delta_v_top=delta_v_top,
                                      delta_v_bottom=delta_v_bottom,
                                      delta_v_side=delta_v_side,
                                      g=g,
                                      min_to_simulate=min_to_simulate,
                                      fps=fps,
                                      output_file=output_file,
                                      deque=self.progress)
            self.hide()

            self.timer = QtCore.QTimer(parent=self)
            self.timer.start(100)
            self.timer.timeout.connect(self.update_progress)

        except IOError as e:
            QtGui.QMessageBox.critical(self, "Error!", str(e))

    def update_progress(self):
        try:
            result = self.progress.pop()
            self.dialog.setValue(int(result))
        except IndexError:  # if empty or finished
            if self.simulator.poll() is not None:
                self.timer.stop()
                window = DemonstrationWindow(self.ui.output_file.text(),
                                             parent=self)
                window.show()
                # otherwise, do nothing


def sigint_handler(*args):
    QtGui.QApplication.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?",
                        type=argparse.FileType(mode="rb"),
                        default=None)
    args = parser.parse_args()

    app = QtGui.QApplication(argv)

    if args.input:
        main_window = DemonstrationWindow(args.input.name)
    else:
        main_window = NewExperimentWindow()
    main_window.show()

    # Timer is made in order to let program handle SIGINT

    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    exit(app.exec_())
