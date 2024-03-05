#coding:utf-8
import maya.cmds as cmds
import re
import os
import sys

def replace_ass_main(**kwargs):
    # 環境変数の設定
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

    # シーンのオープン
    ma_current_path = (kwargs['ma_current_path'])
    cmds.file(ma_current_path, o=True, f=True)

    # ma_current_path = kwargs['ma_current_path']
    # ass_current_path = kwargs['ass_current_path']
    file_namespace = kwargs['file_namespace']
    obj = '{}_standIn'.format(file_namespace)
    dso_org = cmds.getAttr("{}Shape.dso".format(obj))
    dso_ver = dso_org.split('/')[-3]
    dso_new = dso_org.replace(dso_ver, 'current')
    cmds.setAttr("{}Shape.dso".format(obj), dso_new, type='string')
    # cmds.rename(obj, '{}Shape'.format(obj))
    cmds.file(rename=ma_current_path)
    cmds.file(save=True, force=True, type='mayaAscii')


def ndPyLibReplaceAss_caller(args):
    replace_ass_main(**args)