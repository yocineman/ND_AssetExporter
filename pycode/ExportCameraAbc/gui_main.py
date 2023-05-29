# coding: utf-8
# ------------------------------
_version_ = "0.0.1"
_author_ = "Kei Ueda"
# ------------------------------
import os
import sys
import subprocess
try:
    from importlib import reload
except:
    pass
import maya.cmds as cmds

from . import export_camera_abc_main
reload(export_camera_abc_main)

from maya import OpenMayaUI as omUI
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
import PySide2.QtWidgets as QtWidgets
import shiboken2

onpath = os.path.dirname(os.path.abspath(__file__))
TOOLNAME = 'Export Camera as alembic'


def undoable(func):
    def _undoable(*args):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args)
        finally:
            cmds.undoInfo(closeChunk=True)
    return _undoable


class GUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.close_exists_window()
        ui_file = 'gui.ui'
        ui_path = os.path.join(onpath, ui_file)
        self.ui = QUiLoader().load(ui_path)
        self.setCentralWidget(self.ui)
        self.set_window_pos()
        self.setWindowTitle('{} {}'.format(TOOLNAME, _version_))

        self.ui.export_btn.clicked.connect(self.export_btn_clciked)
        self.ui.open_exp_folder_btn.clicked.connect(self.open_exp_folder_btn_clicked)
        self.instance_export_camera_abc()
        self.ui.show()

    def export_btn_clciked(self):
        remain_cam = self.ui.ramain_cam_chk.isChecked()
        self.get_ext_type()
        self.InstanceExportCameraAbc.export(remain_cam)

    def get_ext_type(self):
        self.ext_type = self.ui.ext_group.checkedButton().text().split('_exp')[0]

    def open_exp_folder_btn_clicked(self):
        # open folder
        self.get_ext_type()
        dir_path = self.InstanceExportCameraAbc.get_ext_dir(self.ext_type)
        if os.path.exists(dir_path):
            subprocess.Popen(["start", "", dir_path], shell=True)
        else:
            dir_path = self.InstanceExportCameraAbc.output_base
            subprocess.Popen(["start", "", dir_path], shell=True)

    def instance_export_camera_abc(self):
        self.InstanceExportCameraAbc = export_camera_abc_main.ExportCameraAbc()


    def close_exists_window(self):
        ptr = omUI.MQtUtil.mainWindow()
        if ptr is not None:
            child_list = shiboken2.wrapInstance(
                int(ptr), QtWidgets.QMainWindow).children()
            for c in child_list[:]:
                if self.__class__.__name__ == c.__class__.__name__:
                    try:
                        c.close()
                    except Exception as e:
                        print(e)

    def set_window_pos(self):
        try:
            desktop = QtWidgets.qApp.desktop()
            activeScreen = desktop.screenNumber(desktop.cursor().pos())
            desktopCenter = desktop.screenGeometry(activeScreen).center()
            w_w = desktopCenter.x()
            w_h = desktopCenter.y()
            framesize = self.ui.frameSize()
            self.move(w_w-framesize.width()/2, w_h-framesize.height()/2)
        except:
            pass

def runs():
    # app = QtWidgets.QApplication.instance()
    # if app is None:
    #     app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    return True
