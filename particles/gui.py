# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/NewExperimentWindow.ui'
#
# Created: Sun Jan 17 22:00:02 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewExperimentWindow(object):
    def setupUi(self, NewExperimentWindow):
        NewExperimentWindow.setObjectName("NewExperimentWindow")
        NewExperimentWindow.resize(443, 448)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewExperimentWindow.sizePolicy().hasHeightForWidth())
        NewExperimentWindow.setSizePolicy(sizePolicy)
        self.group_particle_settings = QtGui.QGroupBox(NewExperimentWindow)
        self.group_particle_settings.setGeometry(QtCore.QRect(10, 0, 201, 201))
        self.group_particle_settings.setObjectName("group_particle_settings")
        self.formLayoutWidget = QtGui.QWidget(self.group_particle_settings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 20, 201, 174))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.form_particle_settings = QtGui.QFormLayout(self.formLayoutWidget)
        self.form_particle_settings.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.form_particle_settings.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.form_particle_settings.setContentsMargins(5, 5, 5, 5)
        self.form_particle_settings.setVerticalSpacing(6)
        self.form_particle_settings.setObjectName("form_particle_settings")
        self.label_n_right = QtGui.QLabel(self.formLayoutWidget)
        self.label_n_right.setMinimumSize(QtCore.QSize(115, 0))
        self.label_n_right.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_n_right.setObjectName("label_n_right")
        self.form_particle_settings.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_n_right)
        self.label_particle_r = QtGui.QLabel(self.formLayoutWidget)
        self.label_particle_r.setMinimumSize(QtCore.QSize(115, 0))
        self.label_particle_r.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_particle_r.setObjectName("label_particle_r")
        self.form_particle_settings.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_particle_r)
        self.label_n_left = QtGui.QLabel(self.formLayoutWidget)
        self.label_n_left.setMinimumSize(QtCore.QSize(115, 0))
        self.label_n_left.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_n_left.setObjectName("label_n_left")
        self.form_particle_settings.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_n_left)
        self.label_v_init = QtGui.QLabel(self.formLayoutWidget)
        self.label_v_init.setMinimumSize(QtCore.QSize(115, 0))
        self.label_v_init.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_v_init.setObjectName("label_v_init")
        self.form_particle_settings.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_v_init)
        self.label_v_loss = QtGui.QLabel(self.formLayoutWidget)
        self.label_v_loss.setMinimumSize(QtCore.QSize(115, 0))
        self.label_v_loss.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_v_loss.setObjectName("label_v_loss")
        self.form_particle_settings.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_v_loss)
        self.n_left = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.n_left.setDecimals(0)
        self.n_left.setMinimum(0.0)
        self.n_left.setMaximum(500.0)
        self.n_left.setProperty("value", 100.0)
        self.n_left.setObjectName("n_left")
        self.form_particle_settings.setWidget(0, QtGui.QFormLayout.FieldRole, self.n_left)
        self.n_right = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.n_right.setDecimals(0)
        self.n_right.setProperty("value", 100.0)
        self.n_right.setObjectName("n_right")
        self.form_particle_settings.setWidget(1, QtGui.QFormLayout.FieldRole, self.n_right)
        self.particle_r = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.particle_r.setMinimum(0.01)
        self.particle_r.setSingleStep(0.01)
        self.particle_r.setProperty("value", 0.05)
        self.particle_r.setObjectName("particle_r")
        self.form_particle_settings.setWidget(2, QtGui.QFormLayout.FieldRole, self.particle_r)
        self.v_init = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.v_init.setSingleStep(0.01)
        self.v_init.setObjectName("v_init")
        self.form_particle_settings.setWidget(3, QtGui.QFormLayout.FieldRole, self.v_init)
        self.v_loss = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.v_loss.setMaximum(1.0)
        self.v_loss.setSingleStep(0.01)
        self.v_loss.setObjectName("v_loss")
        self.form_particle_settings.setWidget(4, QtGui.QFormLayout.FieldRole, self.v_loss)
        self.group_geometry = QtGui.QGroupBox(NewExperimentWindow)
        self.group_geometry.setGeometry(QtCore.QRect(10, 200, 201, 231))
        self.group_geometry.setObjectName("group_geometry")
        self.formLayoutWidget_3 = QtGui.QWidget(self.group_geometry)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(0, 20, 200, 209))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.form_box_geometry = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.form_box_geometry.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.form_box_geometry.setContentsMargins(5, 5, 5, 6)
        self.form_box_geometry.setObjectName("form_box_geometry")
        self.label_box_width = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_box_width.setMinimumSize(QtCore.QSize(115, 0))
        self.label_box_width.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_box_width.setObjectName("label_box_width")
        self.form_box_geometry.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_box_width)
        self.label_box_height = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_box_height.setMinimumSize(QtCore.QSize(115, 0))
        self.label_box_height.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_box_height.setObjectName("label_box_height")
        self.form_box_geometry.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_box_height)
        self.label_barrier_x = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_barrier_x.setMinimumSize(QtCore.QSize(115, 0))
        self.label_barrier_x.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_barrier_x.setObjectName("label_barrier_x")
        self.form_box_geometry.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_barrier_x)
        self.label_barrier_width = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_barrier_width.setMinimumSize(QtCore.QSize(115, 0))
        self.label_barrier_width.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_barrier_width.setObjectName("label_barrier_width")
        self.form_box_geometry.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_barrier_width)
        self.label_hole_y = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_hole_y.setMinimumSize(QtCore.QSize(115, 0))
        self.label_hole_y.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_hole_y.setObjectName("label_hole_y")
        self.form_box_geometry.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_hole_y)
        self.label_hole_height = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_hole_height.setMinimumSize(QtCore.QSize(115, 0))
        self.label_hole_height.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_hole_height.setObjectName("label_hole_height")
        self.form_box_geometry.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_hole_height)
        self.box_width = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.box_width.setSingleStep(0.01)
        self.box_width.setProperty("value", 10.0)
        self.box_width.setObjectName("box_width")
        self.form_box_geometry.setWidget(0, QtGui.QFormLayout.FieldRole, self.box_width)
        self.box_height = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.box_height.setSingleStep(0.01)
        self.box_height.setProperty("value", 10.0)
        self.box_height.setObjectName("box_height")
        self.form_box_geometry.setWidget(1, QtGui.QFormLayout.FieldRole, self.box_height)
        self.barrier_x = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.barrier_x.setSingleStep(0.01)
        self.barrier_x.setProperty("value", 5.0)
        self.barrier_x.setObjectName("barrier_x")
        self.form_box_geometry.setWidget(2, QtGui.QFormLayout.FieldRole, self.barrier_x)
        self.barrier_width = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.barrier_width.setSingleStep(0.01)
        self.barrier_width.setProperty("value", 1.0)
        self.barrier_width.setObjectName("barrier_width")
        self.form_box_geometry.setWidget(3, QtGui.QFormLayout.FieldRole, self.barrier_width)
        self.hole_y = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.hole_y.setSingleStep(0.01)
        self.hole_y.setProperty("value", 5.0)
        self.hole_y.setObjectName("hole_y")
        self.form_box_geometry.setWidget(4, QtGui.QFormLayout.FieldRole, self.hole_y)
        self.hole_height = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.hole_height.setSingleStep(0.01)
        self.hole_height.setProperty("value", 1.0)
        self.hole_height.setObjectName("hole_height")
        self.form_box_geometry.setWidget(5, QtGui.QFormLayout.FieldRole, self.hole_height)
        self.group_collision_settings = QtGui.QGroupBox(NewExperimentWindow)
        self.group_collision_settings.setGeometry(QtCore.QRect(220, 0, 211, 131))
        self.group_collision_settings.setObjectName("group_collision_settings")
        self.formLayoutWidget_2 = QtGui.QWidget(self.group_collision_settings)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 211, 106))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.form_collision_settings = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.form_collision_settings.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.form_collision_settings.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.form_collision_settings.setContentsMargins(5, 5, 5, 5)
        self.form_collision_settings.setVerticalSpacing(6)
        self.form_collision_settings.setObjectName("form_collision_settings")
        self.label_delta_v_top = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_delta_v_top.setMinimumSize(QtCore.QSize(115, 0))
        self.label_delta_v_top.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_delta_v_top.setObjectName("label_delta_v_top")
        self.form_collision_settings.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_delta_v_top)
        self.label_delta_v_bottom = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_delta_v_bottom.setMinimumSize(QtCore.QSize(115, 0))
        self.label_delta_v_bottom.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_delta_v_bottom.setObjectName("label_delta_v_bottom")
        self.form_collision_settings.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_delta_v_bottom)
        self.label_delta_v_side = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_delta_v_side.setMinimumSize(QtCore.QSize(115, 0))
        self.label_delta_v_side.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_delta_v_side.setObjectName("label_delta_v_side")
        self.form_collision_settings.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_delta_v_side)
        self.delta_v_top = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.delta_v_top.setSingleStep(0.01)
        self.delta_v_top.setObjectName("delta_v_top")
        self.form_collision_settings.setWidget(0, QtGui.QFormLayout.FieldRole, self.delta_v_top)
        self.delta_v_bottom = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.delta_v_bottom.setSingleStep(0.01)
        self.delta_v_bottom.setObjectName("delta_v_bottom")
        self.form_collision_settings.setWidget(1, QtGui.QFormLayout.FieldRole, self.delta_v_bottom)
        self.delta_v_side = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.delta_v_side.setSingleStep(0.01)
        self.delta_v_side.setObjectName("delta_v_side")
        self.form_collision_settings.setWidget(2, QtGui.QFormLayout.FieldRole, self.delta_v_side)
        self.button_run = QtGui.QPushButton(NewExperimentWindow)
        self.button_run.setGeometry(QtCore.QRect(330, 410, 101, 28))
        self.button_run.setObjectName("button_run")
        self.group_misc_settings = QtGui.QGroupBox(NewExperimentWindow)
        self.group_misc_settings.setGeometry(QtCore.QRect(220, 130, 211, 131))
        self.group_misc_settings.setObjectName("group_misc_settings")
        self.formLayoutWidget_4 = QtGui.QWidget(self.group_misc_settings)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(0, 20, 211, 106))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.form_misc_settings = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.form_misc_settings.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.form_misc_settings.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.form_misc_settings.setContentsMargins(5, 5, 5, 5)
        self.form_misc_settings.setVerticalSpacing(6)
        self.form_misc_settings.setObjectName("form_misc_settings")
        self.label_g = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_g.setMinimumSize(QtCore.QSize(115, 0))
        self.label_g.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_g.setObjectName("label_g")
        self.form_misc_settings.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_g)
        self.label_simulation_time = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_simulation_time.setMinimumSize(QtCore.QSize(115, 0))
        self.label_simulation_time.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_simulation_time.setObjectName("label_simulation_time")
        self.form_misc_settings.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_simulation_time)
        self.label_fps = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_fps.setMinimumSize(QtCore.QSize(115, 0))
        self.label_fps.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_fps.setObjectName("label_fps")
        self.form_misc_settings.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_fps)
        self.g = QtGui.QDoubleSpinBox(self.formLayoutWidget_4)
        self.g.setMinimum(0.1)
        self.g.setSingleStep(0.1)
        self.g.setProperty("value", 9.8)
        self.g.setObjectName("g")
        self.form_misc_settings.setWidget(0, QtGui.QFormLayout.FieldRole, self.g)
        self.simulation_time = QtGui.QDoubleSpinBox(self.formLayoutWidget_4)
        self.simulation_time.setDecimals(0)
        self.simulation_time.setMinimum(1.0)
        self.simulation_time.setMaximum(180.0)
        self.simulation_time.setObjectName("simulation_time")
        self.form_misc_settings.setWidget(1, QtGui.QFormLayout.FieldRole, self.simulation_time)
        self.fps = QtGui.QDoubleSpinBox(self.formLayoutWidget_4)
        self.fps.setDecimals(0)
        self.fps.setMinimum(1.0)
        self.fps.setMaximum(60.0)
        self.fps.setProperty("value", 30.0)
        self.fps.setObjectName("fps")
        self.form_misc_settings.setWidget(2, QtGui.QFormLayout.FieldRole, self.fps)
        self.group_output_file = QtGui.QGroupBox(NewExperimentWindow)
        self.group_output_file.setGeometry(QtCore.QRect(220, 260, 211, 51))
        self.group_output_file.setObjectName("group_output_file")
        self.output_file = QtGui.QLineEdit(self.group_output_file)
        self.output_file.setEnabled(True)
        self.output_file.setGeometry(QtCore.QRect(0, 20, 181, 30))
        self.output_file.setObjectName("output_file")
        self.output_file_button = QtGui.QToolButton(self.group_output_file)
        self.output_file_button.setGeometry(QtCore.QRect(176, 20, 30, 30))
        self.output_file_button.setObjectName("output_file_button")

        self.retranslateUi(NewExperimentWindow)
        QtCore.QMetaObject.connectSlotsByName(NewExperimentWindow)

    def retranslateUi(self, NewExperimentWindow):
        NewExperimentWindow.setWindowTitle(QtGui.QApplication.translate("NewExperimentWindow", "Particles in Box", None, QtGui.QApplication.UnicodeUTF8))
        self.group_particle_settings.setTitle(QtGui.QApplication.translate("NewExperimentWindow", "Particle settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_n_right.setText(QtGui.QApplication.translate("NewExperimentWindow", "Count (right side)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_particle_r.setText(QtGui.QApplication.translate("NewExperimentWindow", "Radius", None, QtGui.QApplication.UnicodeUTF8))
        self.label_n_left.setText(QtGui.QApplication.translate("NewExperimentWindow", "Count (left side)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_v_init.setText(QtGui.QApplication.translate("NewExperimentWindow", "Initial speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_v_loss.setText(QtGui.QApplication.translate("NewExperimentWindow", "Speed loss factor", None, QtGui.QApplication.UnicodeUTF8))
        self.group_geometry.setTitle(QtGui.QApplication.translate("NewExperimentWindow", "Box geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_box_width.setText(QtGui.QApplication.translate("NewExperimentWindow", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_box_height.setText(QtGui.QApplication.translate("NewExperimentWindow", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.label_barrier_x.setText(QtGui.QApplication.translate("NewExperimentWindow", "Barrier X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_barrier_width.setText(QtGui.QApplication.translate("NewExperimentWindow", "Barrier width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_hole_y.setText(QtGui.QApplication.translate("NewExperimentWindow", "Hole Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_hole_height.setText(QtGui.QApplication.translate("NewExperimentWindow", "Hole height", None, QtGui.QApplication.UnicodeUTF8))
        self.group_collision_settings.setTitle(QtGui.QApplication.translate("NewExperimentWindow", "Speed change after collision", None, QtGui.QApplication.UnicodeUTF8))
        self.label_delta_v_top.setText(QtGui.QApplication.translate("NewExperimentWindow", "Top", None, QtGui.QApplication.UnicodeUTF8))
        self.label_delta_v_bottom.setText(QtGui.QApplication.translate("NewExperimentWindow", "Bottom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_delta_v_side.setText(QtGui.QApplication.translate("NewExperimentWindow", "Sides", None, QtGui.QApplication.UnicodeUTF8))
        self.button_run.setText(QtGui.QApplication.translate("NewExperimentWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.group_misc_settings.setTitle(QtGui.QApplication.translate("NewExperimentWindow", "Misc settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_g.setText(QtGui.QApplication.translate("NewExperimentWindow", "g", None, QtGui.QApplication.UnicodeUTF8))
        self.label_simulation_time.setText(QtGui.QApplication.translate("NewExperimentWindow", "Min. to simulate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fps.setText(QtGui.QApplication.translate("NewExperimentWindow", "Frames/second", None, QtGui.QApplication.UnicodeUTF8))
        self.group_output_file.setTitle(QtGui.QApplication.translate("NewExperimentWindow", "Output file", None, QtGui.QApplication.UnicodeUTF8))
        self.output_file_button.setText(QtGui.QApplication.translate("NewExperimentWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
