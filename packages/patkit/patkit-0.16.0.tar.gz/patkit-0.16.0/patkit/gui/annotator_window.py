#
# Copyright (c) 2019-2025
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
This is the main window of the PATKIT annotator.
"""

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1087, 795)
        MainWindow.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mplwindow = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplwindow.setObjectName("mplwindow")
        self.mplWindowVerticalLayout = QtWidgets.QVBoxLayout(self.mplwindow)
        self.mplWindowVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mplWindowVerticalLayout.setObjectName("mplWindowVerticalLayout")
        self.horizontalLayout.addWidget(self.mplwindow)
        self.button_organiser = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_organiser.sizePolicy().hasHeightForWidth()
        )
        self.button_organiser.setSizePolicy(sizePolicy)
        self.button_organiser.setMinimumSize(QtCore.QSize(300, 0))
        self.button_organiser.setMaximumSize(QtCore.QSize(200, 16777215))
        self.button_organiser.setObjectName("button_organiser")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.button_organiser)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.button_organiser)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.goLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.goLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.goLineEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.goLineEdit.setObjectName("goLineEdit")
        self.horizontalLayout_3.addWidget(self.goLineEdit)
        self.goButton = QtWidgets.QPushButton(self.groupBox)
        self.goButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.goButton.setObjectName("goButton")
        self.horizontalLayout_3.addWidget(self.goButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(self.button_organiser)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(300, 50))
        self.frame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtWidgets.QPushButton(self.frame)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 1, 1, 1)
        self.nextButton = QtWidgets.QPushButton(self.frame)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout.addWidget(self.nextButton, 1, 0, 1, 1)
        self.prevButton = QtWidgets.QPushButton(self.frame)
        self.prevButton.setObjectName("prevButton")
        self.gridLayout.addWidget(self.prevButton, 0, 0, 1, 1)
        self.exportButton = QtWidgets.QPushButton(self.frame)
        self.exportButton.setObjectName("exportButton")
        self.gridLayout.addWidget(self.exportButton, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.frame)
        self.databaseView = QtWidgets.QListView(self.button_organiser)
        self.databaseView.setObjectName("databaseView")
        self.verticalLayout_3.addWidget(self.databaseView)
        self.ultrasoundFrame = QtWidgets.QWidget(self.button_organiser)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ultrasoundFrame.sizePolicy().hasHeightForWidth()
        )
        self.ultrasoundFrame.setSizePolicy(sizePolicy)
        self.ultrasoundFrame.setMinimumSize(QtCore.QSize(300, 300))
        self.ultrasoundFrame.setObjectName("ultrasoundFrame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.ultrasoundFrame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3.addWidget(self.ultrasoundFrame)
        self.positionRB = QtWidgets.QGroupBox(self.button_organiser)
        self.positionRB.setObjectName("positionRB")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.positionRB)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.positionRB_1 = QtWidgets.QRadioButton(self.positionRB)
        self.positionRB_1.setAutoFillBackground(False)
        self.positionRB_1.setObjectName("positionRB_1")
        self.tonguePositionRBs = QtWidgets.QButtonGroup(MainWindow)
        self.tonguePositionRBs.setObjectName("tonguePositionRBs")
        self.tonguePositionRBs.addButton(self.positionRB_1)
        self.verticalLayout_5.addWidget(self.positionRB_1)
        self.positionRB_2 = QtWidgets.QRadioButton(self.positionRB)
        self.positionRB_2.setAutoFillBackground(False)
        self.positionRB_2.setObjectName("positionRB_2")
        self.tonguePositionRBs.addButton(self.positionRB_2)
        self.verticalLayout_5.addWidget(self.positionRB_2)
        self.positionRB_3 = QtWidgets.QRadioButton(self.positionRB)
        self.positionRB_3.setAutoFillBackground(False)
        self.positionRB_3.setObjectName("positionRB_3")
        self.tonguePositionRBs.addButton(self.positionRB_3)
        self.verticalLayout_5.addWidget(self.positionRB_3)
        self.verticalLayout_3.addWidget(self.positionRB)
        self.horizontalLayout.addWidget(self.button_organiser)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1087, 22))
        self.menubar.setObjectName("menubar")

        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_image = QtWidgets.QMenu(self.menubar)

        self.menu_image.setObjectName("menu_image")
        self.menu_script = QtWidgets.QMenu(self.menubar)
        self.menu_script.setEnabled(False)
        self.menu_script.setObjectName("menu_script")
        self.menu_navigation = QtWidgets.QMenu(self.menubar)
        self.menu_navigation.setObjectName("menu_navigation")
        self.menu_export = QtWidgets.QMenu(self.menubar)
        self.menu_export.setObjectName("menu_export")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.action_open = QtGui.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save_all = QtGui.QAction(MainWindow)
        self.action_save_all.setObjectName("action_save_all")
        self.actionSave_as = QtGui.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.action_save_all_textgrids = QtGui.QAction(MainWindow)
        self.action_save_all_textgrids.setObjectName(
            "action_save_all_textgrids")
        self.action_save_current_textgrid = QtGui.QAction(MainWindow)
        self.action_save_current_textgrid.setObjectName(
            "action_save_current_textgrid")
        self.action_quit = QtGui.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")

        self.actionShow_interpreter = QtGui.QAction(MainWindow)
        self.actionShow_interpreter.setObjectName("actionShow_interpreter")
        self.actionRun_file = QtGui.QAction(MainWindow)
        self.actionRun_file.setObjectName("actionRun_file")

        self.actionNext = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionPrevious = QtGui.QAction(MainWindow)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionNext_Frame = QtGui.QAction(MainWindow)
        self.actionNext_Frame.setObjectName("actionNext_Frame")
        self.actionPrevious_Frame = QtGui.QAction(MainWindow)
        self.actionPrevious_Frame.setObjectName("actionPrevious_Frame")

        self.action_export_analysis = QtGui.QAction(MainWindow)
        self.action_export_analysis.setEnabled(False)
        self.action_export_analysis.setObjectName("action_export_analysis")
        self.action_export_main_figure = QtGui.QAction(MainWindow)
        self.action_export_main_figure.setObjectName(
            "action_export_main_figure")
        self.action_export_ultrasound_frame = QtGui.QAction(
            MainWindow)
        self.action_export_ultrasound_frame.setObjectName(
            "action_export_ultrasound_frame"
        )
        self.action_export_annotations_and_metadata = QtGui.QAction(
            MainWindow)
        self.action_export_annotations_and_metadata.setObjectName(
            "action_export_annotations_and_metadata"
        )
        self.action_export_aggregate_images = QtGui.QAction(
            MainWindow)
        self.action_export_aggregate_images.setObjectName(
            "action_export_aggregate_images"
        )
        self.action_export_distance_matrices = QtGui.QAction(
            MainWindow)
        self.action_export_distance_matrices.setObjectName(
            "action_export_distance_matrices"
        )

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save_current_textgrid)
        self.menu_file.addAction(self.action_save_all_textgrids)
        self.menu_file.addAction(self.action_save_all)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)

        # self.menu_script.addAction(self.actionShow_interpreter)
        # self.menu_script.addAction(self.actionRun_file)

        self.menu_navigation.addAction(self.actionNext)
        self.menu_navigation.addAction(self.actionPrevious)
        self.menu_navigation.addSeparator()
        self.menu_navigation.addAction(self.actionNext_Frame)
        self.menu_navigation.addAction(self.actionPrevious_Frame)

        self.menu_export.addAction(self.action_export_aggregate_images)
        self.menu_export.addAction(self.action_export_annotations_and_metadata)
        self.menu_export.addAction(self.action_export_distance_matrices)
        self.menu_export.addAction(self.action_export_main_figure)
        self.menu_export.addAction(self.action_export_ultrasound_frame)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_export.menuAction())
        self.menubar.addAction(self.menu_image.menuAction())
        self.menubar.addAction(self.menu_script.menuAction())
        self.menubar.addAction(self.menu_navigation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PATKIT Annotator"))
        self.groupBox.setTitle(_translate("MainWindow", "Go to Recording"))
        self.goButton.setText(_translate("MainWindow", "Go"))
        self.saveButton.setText(_translate("MainWindow", "Save..."))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.prevButton.setText(_translate("MainWindow", "Previous"))
        self.exportButton.setText(_translate("MainWindow", "Save Annotations..."))
        self.positionRB.setTitle(
            _translate("MainWindow", "Customised Metadata: TonguePosition")
        )
        self.positionRB_1.setText(_translate("MainWindow", "High"))
        self.positionRB_2.setText(_translate("MainWindow", "Low"))
        self.positionRB_3.setText(_translate("MainWindow", "Other / Not visible"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_image.setTitle(_translate("MainWindow", "Image"))
        self.menu_script.setTitle(_translate("MainWindow", "Script"))
        self.menu_navigation.setTitle(_translate("MainWindow", "Navigation"))
        self.menu_export.setTitle(_translate("MainWindow", "Export"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.action_open.setText(_translate("MainWindow", "Open..."))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_save_all.setText(_translate("MainWindow", "Save all"))
        self.action_save_all.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionShow_interpreter.setText(
            _translate("MainWindow", "Show interpreter")
        )
        self.actionRun_file.setText(_translate("MainWindow", "Run file..."))
        self.actionNext.setText(_translate("MainWindow", "Next Recording"))
        self.actionNext.setShortcut(_translate("MainWindow", "Down"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous Recording"))
        self.actionPrevious.setShortcut(_translate("MainWindow", "Up"))
        self.action_export_analysis.setText(
            _translate("MainWindow", "Export analysis...")
        )
        self.actionNext_Frame.setText(_translate("MainWindow", "Next Frame"))
        self.actionNext_Frame.setShortcut(_translate("MainWindow", "Right"))
        self.actionPrevious_Frame.setText(_translate("MainWindow", "Previous Frame"))
        self.actionPrevious_Frame.setShortcut(_translate("MainWindow", "Left"))
        self.action_export_main_figure.setText(
            _translate("MainWindow", "Export main figure...")
        )
        self.action_export_main_figure.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_export_ultrasound_frame.setText(
            _translate("MainWindow", "Export ultrasound figure...")
        )
        self.action_export_annotations_and_metadata.setText(
            _translate("MainWindow", "Export annotations and metadata...")
        )
        self.action_export_aggregate_images.setText(
            _translate("MainWindow", "Export aggregate images...")
        )
        self.action_save_all_textgrids.setText(
            _translate("MainWindow", "Save all TextGrids")
        )
        self.action_save_current_textgrid.setText(
            _translate("MainWindow", "Save current TextGrid")
        )
        self.action_quit.setText(_translate("MainWindow", "Quit"))
        self.action_quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_export_distance_matrices.setText(
            _translate("MainWindow", "Export distance matrices...")
        )
