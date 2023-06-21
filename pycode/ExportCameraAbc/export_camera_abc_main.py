# -*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds
try:
    from importlib import reload
except:
    pass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maya_lib import ndPyLibExportCam;reload(ndPyLibExportCam)
import maya.cmds as cmds

class ExportCameraAbc(object):
    def __init__(self, cam_list=None):
        current_scene_name = cmds.file(q=True, sn=True)
        self.file_name = os.path.basename(current_scene_name).split('.')[0]
        if 'work' in current_scene_name:
            self.output_base = os.path.join(current_scene_name.split('work')[0], 'publish', 'cache')
        elif 'publish' in current_scene_name:
            self.output_base = os.path.join(current_scene_name.split('publish')[0], 'publish', 'cache')
        else:
            cmds.inViewMessage(amg='scene path is not valid.', pos='botLeft', fade=True, fot=2000)
            raise ValueError('scene path is not valid.')
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

        self.ma_cam_path = os.path.join(self.output_base, 'ma', self.file_name, 'cam.ma').replace('\\', '/')
        self.abc_cam_path = os.path.join(self.output_base, 'abc', self.file_name, 'cam.abc').replace('\\', '/')
        self.fbx_cam_path = os.path.join(self.output_base, 'fbx', self.file_name, 'cam.fbx').replace('\\', '/')


    def get_ext_dir(self, ext_type='all'):
        if ext_type == 'all':
            self.exp_dir = os.path.join(self.output_base)
        elif ext_type == 'abc':
            self.exp_dir = os.path.join(self.output_base, 'abc')
        elif ext_type == 'fbx':
            self.exp_dir = os.path.join(self.output_base, 'fbx')
        elif ext_type == 'ma':
            self.exp_dir = os.path.join(self.output_base, 'ma')
        return self.exp_dir


    def export(self, remain_cam=False, ext_type='all', tg_cam_list=None):
        try:
            if cmds.getAttr('time1.enableTimewarp') and cmds.listConnections('time1.timewarpIn_Raw') == True:
                scene_timewarp = True
            else:
                scene_timewarp = False
        except:
            scene_timewarp = True
        self.get_ext_dir(ext_type)

        info_dic = {
            'outputdir': self.exp_dir.replace('\\', '/'),
            'file_name': 'cam',
            'cam_scale': self.cam_scale,
            'frame_handle': self.frame_hundle,
            'frame_range': self.frame_range,
            'scene_timewarp': scene_timewarp,
            'ext_type': ext_type,
            'remain_cam':  remain_cam,
            'ma_cam_path': self.ma_cam_path,
            'abc_cam_path': self.abc_cam_path,
            'fbx_cam_path': self.fbx_cam_path,
            'project': os.environ['PROJ'],
            'step_value': 1.0,
            'tg_cam_list': tg_cam_list,
        }
        ndPyLibExportCam.export_cam_main(info_dic)

        return True