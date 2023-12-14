#coding:utf-8
import maya.cmds as cmds
import re
import os
import sys

def attach_ass_main(**kwargs):
    #環境変数などの設定
    # arnold
    sys.path.append('Y:/users/env/arnold/mtoa/2022_MtoA_5133/scripts')
    try:
        import arnold
    except:
        pass
    # scripts
    scripts_path = 'Y:/users/env/arnold/mtoa/2022_MtoA_5133/scripts'
    os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'].rstrip(';') + ';' + scripts_path
    os.environ['MAYA_SCRIPT_PATH'] = os.environ['MAYA_SCRIPT_PATH'] + ';' + scripts_path
    # plug-in
    plugin_path = 'Y:/users/env/arnold/mtoa/2022_MtoA_5133/plug-ins'
    os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH'].rstrip(';') + ';' + plugin_path
    # mod
    mod_path = 'Y:/users/env/maya/2022/mod'
    # os.environ['MAYA_MODULE_PATH']  = os.environ['MAYA_MODULE_PATH'].rstrip(';') + ';' + mod_path
    os.environ['MAYA_MODULE_PATH'] = mod_path
    try:
        cmds.loadPlugin('mtoa')
    except:
        pass
    import mtoa

    namespace = kwargs['file_namespace']
    ma_ver_path = kwargs['ma_ver_path']
    ass_ver_path = kwargs['ass_ver_path']
    frame_list = kwargs['frame_range']
    print(frame_list)
    obj = mtoa.core.createStandIn()
    cmds.setAttr("{}.dso".format(obj), ass_ver_path, type='string')
    cmds.setAttr("{}.frameNumber".format(obj), float(frame_list[0]))
    cmds.setAttr("{}.useFrameExtension".format(obj), True)
    cmds.rename(obj.replace("Shape", ""), "{}_standIn".format(namespace))
    cmds.playbackOptions(min=frame_list[0], max=frame_list[1], e=True)
    cmds.file(rename=ma_ver_path)
    cmds.file(save=True, force=True, type='mayaAscii')


def ndPyLibAttachAss_caller(args):
    attach_ass_main(**args)