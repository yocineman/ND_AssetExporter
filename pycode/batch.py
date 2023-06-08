# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import yaml

onpath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

def maya_cmd_maker(unique_order, mayafile=None, mayaBatch=None):
    maya_cmd = (
        "import sys;"+
        "sys.path.append(\'{}/maya_lib\');".format(onpath)+
        "sys.path.append(\'{}\');".format(onpath)
    )
    maya_cmd = maya_cmd + unique_order
    cmd = [mayaBatch]
    if mayafile is not None:
        cmd.append('-file')
        cmd.append(mayafile)
    cmd.append('-command')
    cmd.append('python(\"{}\")'.format(maya_cmd.replace(';', '\;').replace('\'', '\\\'')))
    return cmd


def env_load(project, is_env_load):
    if is_env_load is True:
        ND_TOOL_PATH_default = "Y:/tool/ND_Tools/python"
        env_key = "ND_TOOL_PATH_PYTHON"
        ND_TOOL_PATH = os.environ.get(env_key, ND_TOOL_PATH_default)
        for path in ND_TOOL_PATH.split(';'):
            path = path.replace('\\', '/')
            if path in sys.path: continue
            sys.path.append(path)
        import shell_lib.env_loader
        shell_lib.env_loader.run(project, fork=True)

        #python3も2で実行されるように
        os.environ['MAYA_PYTHON_VERSION']='2'
    # if project == 'd_wh':
    #     set_dw_h_env()


def maya_version(project, ver_override=False):
    # ------------------------------------
    env_key = 'ND_TOOL_PATH_PYTHON'
    ND_TOOL_PATH = os.environ.get(env_key,'Y:/tool/ND_Tools/python')
    for path in ND_TOOL_PATH.split(';'):
        path = path.replace('\\','/')
        if path in sys.path: continue
        sys.path.append(path)
    toolkit_path = "Y:\\tool\\ND_Tools\\shotgun"
    app_launcher_path = "config\\env\\includes\\app_launchers.yml"
    dcc_tools = ["maya", "nuke", "nukex"]
    # if project.lower() == 'd_wh':
    #     project_app_launcher = "%s\\ND_sgtoolkit_%s_old\\%s" % (toolkit_path, project.lower(), app_launcher_path)
    # else:
    project_app_launcher = "%s\\ND_sgtoolkit_%s\\%s" % (toolkit_path, project.lower(), app_launcher_path)
    #------------------------------------
    f = open(project_app_launcher, "r")
    data = yaml.safe_load(f)
    f.close()

    for dcc in dcc_tools:
        for version in data["launch_%s" % dcc]["versions"]:
            args = data["launch_%s" % dcc]["windows_args"]
            if dcc == 'maya':
               renderinfo = version.replace('(','').split(')')

    ryear = renderinfo[0]
    if ver_override == 'False' or ver_override == False:
        maya_exe = 'C:\\Program Files\\Autodesk\\Maya{}\\bin\\mayabatch.exe'.format(str(ryear))
        # maya_exe = 'C:\\Program Files\\Autodesk\\Maya2020\\bin\\maya.exe'
    else:
        maya_exe = 'C:\\Program Files\\Autodesk\\Maya{}\\bin\\mayabatch.exe'.format(
            str(ver_override))
    return  maya_exe

# ------------------------------------
# Anim
# ------------------------------------
def animExport(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    unique_order = (
        # 'from maya_lib.mayaBasic import *;'
        'from maya_lib.ndPyLibExportAnim import export_anim_main;'
        'export_anim_main(**{})'.format(kwargs)
    )
    # cmd = maya_cmd_maker(unique_order, mayafile=kwargs['input_path'], mayaBatch=mayaBatch)
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    print(cmd)
    subprocess.call(cmd, shell=True, env=os.environ)

def animAttach(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    argsdic = kwargs
    file_namespace = kwargs['file_namespace']

    ma_ver_path = kwargs['ma_ver_path']
    anim_ver_path = kwargs['anim_ver_path']

    asset_path = kwargs['asset_path']
    unique_order = (
        'from maya_lib.mayaBasic import *;'
        'import maya.cmds as cmds;'
        'saveAs(\'{}\');'.format(ma_ver_path) +
        'loadAsset(\'{}\', \'{}\');'.format(asset_path, file_namespace) +
        'loadAsset(\'{}\', \'{}_anim\');'.format(anim_ver_path, file_namespace) +
        'saveAs(\'{}\')'.format(ma_ver_path))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True, env=os.environ)


def animReplace(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    argsdic = kwargs
    ma_current_path = argsdic['ma_current_path']
    publish_current_anim_path = argsdic['anim_current_path']
    file_namespace = argsdic['file_namespace']
    unique_order = (
        'from maya_lib.mayaBasic import *;'
        'replaceAsset(\'{}\', \'{}_anim\');'.format(publish_current_anim_path, file_namespace) +
        'save();'
    )
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True, env=os.environ)


# ------------------------------------
# Abc
# ------------------------------------
def abcExport(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    argsdic = kwargs
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    unique_order = (
            'from ndPyLibExportAbc import ndPyLibExportAbc_caller;'
            'ndPyLibExportAbc_caller({})'.format(argsdic))
    cmd = maya_cmd_maker(unique_order, mayafile=kwargs['input_path'], mayaBatch=mayaBatch)
    subprocess.call(cmd,  shell=True)


def abcAttach(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    asset_path = kwargs['asset_path']
    namespace = kwargs['file_namespace']
    top_node = namespace + ':' + kwargs['top_node']
    ma_ver_path = kwargs['ma_ver_path']
    abc_ver_path = kwargs['abc_ver_path']

    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'import maya.cmds as cmds;'
            'saveAs(\'{}\');'.format(ma_ver_path) +
            'loadAsset(\'{}\', \'{}\');'.format(asset_path, namespace) +
            'selHierarchy=cmds.ls(\'{}\', dag=True);'.format(top_node) +
            'attachABC(\'{}\', \'{}\', selHierarchy);'.format(abc_ver_path, namespace) +
            'saveAs(\'{}\')'.format(ma_ver_path))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True)


def abcReplace(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    argsdic = kwargs
    ma_current_path = argsdic['ma_current_path']
    abc_current_path = argsdic['abc_current_path']
    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'replaceABCPath(\'{}\');'.format(abc_current_path) +
            'save();')
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True)

# ------------------------------------
# Abc&Anim
# ------------------------------------
def abcAnimAttach(**kwargs):
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    asset_path = kwargs['asset_path']
    namespace = kwargs['file_namespace']
    top_node = namespace + ':' + kwargs['top_node']
    ma_ver_path = kwargs['ma_ver_path']
    abc_ver_path = kwargs['abc_ver_path']
    anim_ver_path = kwargs['anim_ver_path']

    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'import maya.cmds as cmds;'
            'saveAs(\'{}\');'.format(ma_ver_path) +
            'loadAsset(\'{}\', \'{}\');'.format(asset_path, namespace) +
            'selHierarchy=cmds.ls(\'{}\', dag=True);'.format(top_node) +
            'attachABC(\'{}\', \'{}\', selHierarchy);'.format(abc_ver_path, namespace) +
            'loadAsset(\'{}\', \'{}_anim\');'.format(anim_ver_path, namespace) +
            'saveAs(\'{}\');'.format(ma_ver_path))

    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True)


def abcAnimReplace(**kwargs):
    argsdic = kwargs
    env_load(kwargs['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    namespace = kwargs['file_namespace']
    ma_current_path = argsdic['ma_current_path']
    abc_current_path = argsdic['abc_current_path']
    anim_current_path = argsdic['anim_current_path']
    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'replaceABCPath(\'{}\');'.format(abc_current_path) +
            'replaceAsset(\'{}\', \'{}_anim\');'.format(anim_current_path, namespace) +
            'save();')
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True)


# ------------------------------------
# Cam
# ------------------------------------
def camExport(**kwargs):
    argsdic = kwargs
    env_load(argsdic['project'], kwargs['env_load'])
    mayaBatch = maya_version(kwargs['project'], kwargs['maya_version'])
    unique_order = (
        'from ndPyLibExportCam import ndPylibExportCam_caller;'
        'ndPylibExportCam_caller(**{})'.format(argsdic))
    cmd = maya_cmd_maker(unique_order, kwargs['input_path'], mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True)


# ------------------------------------
# Ass
# ------------------------------------
def assExport(**kwargs):
    argsdic = kwargs
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\mayabatch.exe'
    unique_order = (
            'from maya_lib.ndPyLibExportAss import export_ass_main;'
            'export_ass_main(**{})'.format(argsdic))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    subprocess.call(cmd,  shell=True)


def assAttach(**kwargs):
    argsdic = kwargs
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\mayabatch.exe'
    unique_order = (
            'from maya_lib.ndPyLibAttachAss import attach_ass_main;'
            'attach_ass_main(**{})'.format(argsdic))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    print(cmd)
    subprocess.call(cmd,  shell=True)


def assReplace(**kwargs):
    argsdic = kwargs
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\mayabatch.exe'
    unique_order = (
            'from maya_lib.ndPyLibReplaceAss import replace_ass_main;'
            'replace_ass_main(**{})'.format(argsdic))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    print(cmd)
    subprocess.call(cmd,shell=True)


def set_dw_h_env():
    # scripts_path = 'Y:/users/env/arnold/mtoa/2022_MtoA_5133/scripts'
    # os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'].rstrip(';') + ';' + scripts_path
    # os.environ['MAYA_SCRIPT_PATH'] = os.environ['MAYA_SCRIPT_PATH'] + ';' + scripts_path
    # plugin_path = 'Y:/users/env/arnold/mtoa/2022_MtoA_5133/plug-ins'
    # os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH'].rstrip(';') + ';' + plugin_path
    # mod_path = 'Y:/users/env/maya/2022/mod'
    # os.environ['MAYA_MODULE_PATH'] = mod_path
    print("##set_dw_h_env##")
    import maya_lib.project.set_dw_h as set_dw_h
    set_dw_h.main()