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
    def __init__(self):
        current_scene_name = cmds.file(q=True, sn=True)
        scene_name = os.path.basename(current_scene_name).split('.')[0]
        if 'work' in current_scene_name:
            self.outputdir = os.path.join(current_scene_name.split('work')[0], 'publish', 'cache', 'alembic', scene_name)
        elif 'publish' in current_scene_name:
            self.outputdir = os.path.join(current_scene_name.split('publish')[0], 'publish', 'cache', 'alembic', scene_name)
        else:
            cmds.inViewMessage(amg='scene path is not valid.', pos='botLeft', fade=True, fot=2000)
            raise ValueError('scene path is not valid.')
        # outputdir = r'C:\Users\k_ueda\Desktop\work\test'
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
        self.cam_scale = 0
        self.frame_hundle = 5
        self.frame_range = False


    def export(self, remain_cam=False):
        try:
            if cmds.getAttr('time1.enableTimewarp') and cmds.listConnections('time1.timewarpIn_Raw') == True:
                scene_timewarp = True
            else:
                scene_timewarp = False
        except:
            scene_timewarp = True

        info_dic = {
            'outputdir': self.outputdir.replace('\\', '/'),
            'file_name': 'cam',
            'cam_scale': self.cam_scale,
            'frame_handle': self.frame_hundle,
            'frame_range': self.frame_range,
            'scene_timewarp': scene_timewarp,
            'mode': 'all',
            'remain_cam':  remain_cam,
        }
        ndPyLibExportCam.export_manual(info_dic)

        return True