#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from PySide import QtGui, QtCore
from PySide.QtOpenGL import QGLWidget, QGLFormat, QGL
from particles.gui import Ui_NewExperimentWindow, Ui_DemonstrationWindow
from particles.simulation import Simulator, Playback
from OpenGL.GL import (glShadeModel, glClearColor, glClearDepth, glEnable,
                       glMatrixMode, glDepthFunc, glHint, glOrtho,
                       glViewport, glLoadIdentity, glClear, glColor3ub,
                       glBegin, glVertex2d, glColor3f, glLineWidth, glEnd,
                       GL_SMOOTH, GL_DEPTH_TEST, GL_PROJECTION, GL_LEQUAL,
                       GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST,
                       GL_MODELVIEW, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       GL_TRIANGLE_FAN, GL_LINE_STRIP)
import datetime
import os.path
import struct
import argparse
from math import sin, pi


class ParticleWidget(QGLWidget):
    SIN_45 = sin(pi / 4)

    def __init__(self, playback, parent=None):
        super(ParticleWidget, self).__init__(parent=parent)
        self.playback = playback

        self.initializeGL()

        self.paintGL()

    def initializeGL(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        glOrtho(0.0, self.playback.simulator.box_width,
                0.0, self.playback.simulator.box_height,
                0.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def clearGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def paintGL(self):
        self.clearGL()
        glLoadIdentity()

        simulator = self.playback.simulator

        r_sin_45 = simulator.particle_r * self.SIN_45
        r_cos_45 = r_sin_45  # r_cos_45 is kept for readability purpose
        particle_r = simulator.particle_r

        for particle in simulator.particles:
            if particle.id & 1:
                glColor3ub(255, 0, 0)
            else:
                glColor3ub(0, 255, 0)

            # TODO: use display  lists here for speed
            glBegin(GL_TRIANGLE_FAN)
            glVertex2d(particle.pos_x + 0, particle.pos_y + 0)
            glVertex2d(particle.pos_x + particle_r, particle.pos_y + 0)
            glVertex2d(particle.pos_x + r_cos_45, particle.pos_y + r_sin_45)
            glVertex2d(particle.pos_x + 0, particle.pos_y + particle_r)
            glVertex2d(particle.pos_x - r_cos_45, particle.pos_y + r_sin_45)
            glVertex2d(particle.pos_x - particle_r, particle.pos_y + 0)
            glVertex2d(particle.pos_x - r_cos_45, particle.pos_y - r_sin_45)
            glVertex2d(particle.pos_x + 0, particle.pos_y - particle_r)
            glVertex2d(particle.pos_x + r_cos_45, particle.pos_y - r_sin_45)
            glVertex2d(particle.pos_x + particle_r, particle.pos_y + 0)
            glEnd()

        glColor3f(1, 1, 1)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)  # Paint the top of the barrier
        glVertex2d(simulator.barrier_x_left, simulator.box_height)
        glVertex2d(simulator.barrier_x_left, simulator.hole_y_top)
        glVertex2d(simulator.barrier_x_right, simulator.hole_y_top)
        glVertex2d(simulator.barrier_x_right, simulator.box_height)
        glEnd()
        glBegin(GL_LINE_STRIP)  # Paint the bottom of the barrier
        glVertex2d(simulator.barrier_x_left, 0)
        glVertex2d(simulator.barrier_x_left, simulator.hole_y_bottom)
        glVertex2d(simulator.barrier_x_right, simulator.hole_y_bottom)
        glVertex2d(simulator.barrier_x_right, 0)
        glEnd()

    def on_render_scene(self):
        self.paintGL()
        self.updateGL()


class DemonstrationWindow(QtGui.QMainWindow):
    def __init__(self, file_name, parent=None):
        super(DemonstrationWindow, self).__init__(parent=parent)

        self.playback = Playback(file_name)

        self.ui = Ui_DemonstrationWindow()

        self.ui.setupUi(self)

        self.ui.canvas = ParticleWidget(self.playback, parent=self.ui.frame_player)
        self.ui.canvas.setFixedSize(self.ui.frame_player.size())

        self.ui.current_state.setMaximum(len(self.playback))

        self.ui.button_play.clicked.connect(self.on_button_play_pressed)

        self.stopped = False

        self.timer = QtCore.QTimer(parent=self)
        self.timer.timeout.connect(self.on_timer_executed)

        self.ui.current_state.sliderPressed.connect(self.on_scrollbar_pressed)
        self.ui.current_state.sliderReleased.connect(self.on_scrollbar_released)
        self.ui.current_state.valueChanged.connect(self.on_scrollbar_value_changed)

        self.ui.button_backward.clicked.connect(self.previous_state)
        self.ui.button_forward.clicked.connect(self.next_state)

        self.start_playback()

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

    def previous_state(self):
        try:
            self.ui.current_state.setValue(self.ui.current_state.value() - 1)
        except (IOError, struct.error, ValueError) as err:
            self.stop_playback()

    def next_state(self):
        try:
            self.ui.current_state.setValue(self.ui.current_state.value() + 1)
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
        except (IOError, ValueError):
            pass


class NewExperimentWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NewExperimentWindow, self).__init__(parent=parent)

        # Set up UI
        self.ui = Ui_NewExperimentWindow()
        self.ui.setupUi(self)

        self.ui.output_file.setText(datetime.datetime.now().strftime("particles_in_box_%Y-%m-%d-%H-%M.bin"))

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
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("input", nargs="?", type=argparse.FileType(mode="rb"), default=None)
        args = parser.parse_args()

        app = QtGui.QApplication(argv)

        if args.input:
            main_window = DemonstrationWindow(args.input.name)
        else:
            main_window = NewExperimentWindow()
        main_window.show()
        exit(app.exec_())
    except KeyboardInterrupt:
        exit(1)
