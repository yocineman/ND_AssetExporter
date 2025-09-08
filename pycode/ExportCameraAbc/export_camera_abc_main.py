# -*- coding: utf-8 -*-
"""
Camera Exportを行うためのメインスクリプト
"""
import os, sys
import maya.cmds as cmds

try:
    from importlib import reload
except:
    pass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maya_lib import ndPyLibExportCam

reload(ndPyLibExportCam)
import maya.cmds as cmds


class ExportCameraAbc(object):
    def __init__(self, cam_list=None):
        current_scene_name = cmds.file(q=True, sn=True)
        self.file_name = os.path.basename(current_scene_name).split(".")[0]
        if "work" in current_scene_name:
            self.output_base = os.path.join(
                current_scene_name.split("work")[0], "publish", "cache"
            )
        elif "publish" in current_scene_name:
            self.output_base = os.path.join(
                current_scene_name.split("publish")[0], "publish", "cache"
            )
        else:
            cmds.inViewMessage(
                amg="scene path is not valid.", pos="botLeft", fade=True, fot=2000
            )
            raise ValueError("scene path is not valid.")
        # outputdir = r'C:\Users\k_ueda\Desktop\work\test'
        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base)
        self.cam_scale = 0
        self.frame_hundle = 5
        self.frame_range = False
        self.tg_cam_list = cam_list

        # self.ma_cam_path = os.path.join(self.output_base, 'ma','{}.ma'.format(self.file_name)).replace('\\', '/')
        # self.abc_cam_path = os.path.join(self.output_base, 'abc','{}.abc'.format(self.file_name)).replace('\\', '/')
        # self.fbx_cam_path = os.path.join(self.output_base, 'fbx','{}.fbx'.format(self.file_name)).replace('\\', '/')

        self.ma_cam_path = os.path.join(
            self.output_base, "ma", self.file_name, "cam.ma"
        ).replace("\\", "/")
        self.abc_cam_path = os.path.join(
            self.output_base, "abc", self.file_name, "cam.abc"
        ).replace("\\", "/")
        self.fbx_cam_path = os.path.join(
            self.output_base, "fbx", self.file_name, "cam.fbx"
        ).replace("\\", "/")

    def get_ext_dir(self, ext_type="all"):
        if ext_type == "all":
            self.exp_dir = os.path.join(self.output_base)
        elif ext_type == "abc":
            self.exp_dir = os.path.join(self.output_base, "abc")
        elif ext_type == "fbx":
            self.exp_dir = os.path.join(self.output_base, "fbx")
        elif ext_type == "ma":
            self.exp_dir = os.path.join(self.output_base, "ma")
        print("Export directory:", self.exp_dir)
        return self.exp_dir

    def set_aspect_ratio(self):
        # device aspect ratio -> film aspect ratio
        cam_list = cmds.ls(type="camera")
        # render settingsから取得
        device_aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")
        # horizontal film apertureのコネクション削除
        for cam in cam_list:
            if cmds.objExists(cam + ".horizontalFilmAperture"):
                con_list = cmds.listConnections(cam + ".horizontalFilmAperture", p=True)
                if con_list:
                    for con in con_list:
                        cmds.disconnectAttr(con, cam + ".horizontalFilmAperture")
            if cmds.objExists(cam + ".verticalFilmAperture"):
                con_list = cmds.listConnections(cam + ".verticalFilmAperture", p=True)
                if con_list:
                    for con in con_list:
                        cmds.disconnectAttr(con, cam + ".verticalFilmAperture")
            # film aspect ratioの設定
            # horizontalFilmAperture
            v_aperture = cmds.getAttr(cam + ".verticalFilmAperture")
            h_aperture = v_aperture * device_aspect_ratio
            cmds.setAttr(cam + ".horizontalFilmAperture", h_aperture)
            cmds.setAttr(cam + ".filmFit", 1)

    def export(self, remain_cam=False, ext_type="all", tg_cam_list=None, scenetimewarp_type="auto"):
        try:
            if (
                cmds.getAttr("time1.enableTimewarp")
                and cmds.listConnections("time1.timewarpIn_Raw") == True
            ):
                manual_bake = True
            else:
                manual_bake = False
        except:
            manual_bake = True
        self.get_ext_dir(ext_type)
        self.set_aspect_ratio()

        info_dic = {
            "outputdir": self.exp_dir.replace("\\", "/"),
            "file_name": "cam",
            "cam_scale": self.cam_scale,
            "frame_handle": self.frame_hundle,
            "frame_range": self.frame_range,
            "manual_bake": manual_bake,
            "ext_type": ext_type,
            "remain_cam": remain_cam,
            "ma_cam_path": self.ma_cam_path,
            "abc_cam_path": self.abc_cam_path,
            "fbx_cam_path": self.fbx_cam_path,
            "project": os.environ["PROJ"],
            "step_value": 1.0,
            "tg_cam_list": tg_cam_list,
            "scenetimewarp_type": scenetimewarp_type,
        }
        ndPyLibExportCam.export_cam_main(info_dic)

        return True


if __name__ == "__main__":
    # Example usage
    cam_list = cmds.ls(type="camera")
    # shapeではなく、上のノードを取得
    cam_list = [cmds.listRelatives(cam, parent=True)[0] for cam in cam_list]
    

    exporter = ExportCameraAbc(cam_list=cam_list)
    exporter.export(
        remain_cam=True, ext_type="all", tg_cam_list=cam_list
    )  # Specify the camera list if needed
    cmds.inViewMessage(
        amg="Camera export completed.", pos="botLeft", fade=True, fot=2000
    )
