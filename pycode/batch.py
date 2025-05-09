# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import yaml

onpath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

def maya_cmd_maker(unique_order, mayafile=None, mayaBatch=None, is_exe=False):
    maya_cmd = (
        "import sys;"+
        "sys.path.append(\'{}/maya_lib\');".format(onpath)+
        "sys.path.append(\'{}\');".format(onpath)
    )
    maya_cmd = maya_cmd + unique_order
    cmd = [mayaBatch]
    if mayafile is not None:
        cmd.append('-file')
        cmd.append(mayafile.replace('\\', '/'))
    if is_exe is not True:
        cmd.append('-batch')
    cmd.append('-command')
    cmd.append('python(\"{}\")'.format(maya_cmd.replace(';', '\;').replace('\'', '\'')))
    cmd.append
    return cmd


def env_load(project):
    ND_TOOL_PATH_default = "Y:/tool/ND_Tools/python"
    env_key = "ND_TOOL_PATH_PYTHON"
    ND_TOOL_PATH = os.environ.get(env_key, ND_TOOL_PATH_default)
    for path in ND_TOOL_PATH.split(';'):
        path = path.replace('\\', '/')
        if path in sys.path: continue
        sys.path.append(path)
    import shell_lib.env_loader
    # shell_lib.env_loader.run(project, fork=True)
    maya_ver = shell_lib.env_loader.set_arnold_env(project)

    # python3も2で実行されるように
    # os.environ['MAYA_PYTHON_VERSION']='2'
    # os.environ["_MAYA_PYTHON_VER"] ="2_7_x"
    return maya_ver


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
    project_app_launcher = "%s\\ND_sgtoolkit_%s\\%s" % (toolkit_path, project.lower(), app_launcher_path)
    # project_app_launcher = "Y:\\tool\\ND_Tools\\python\\ND_appEnv\\projects\\{}.json".format(project)
    # ------------------------------------
    if not os.path.exists(project_app_launcher):
        print("Error: %s does not exist" % project_app_launcher)
        maya_exe = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\maya.exe"
        # maya_exe = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\mayabatch.exe"
        return maya_exe
    f = open(project_app_launcher, "r")
    data = yaml.safe_load(f)
    f.close()
    # ------------------------------------
    ryear = 2022
    for dcc in dcc_tools:
        for version in data["launch_%s" % dcc]["versions"]:
            if dcc == 'maya':
                ryear = version.replace('(','').split(')')[0]
    if ver_override == 'False' or ver_override == False:
        # maya_exe = 'C:\\Program Files\\Autodesk\\Maya{}\\bin\\mayabatch.exe'.format(str(ryear))
        maya_exe = 'C:\\Program Files\\Autodesk\\Maya2023\\bin\\maya.exe'
    else:
        maya_exe = 'C:\\Program Files\\Autodesk\\Maya{}\\bin\\maya.exe'.format(str(ver_override))
    return  maya_exe


# ------------------------------------
#  Anim
# ------------------------------------
def animExport(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    unique_order = (
        'from maya_lib.ndPyLibExportAnim import export_anim_main;'
        'export_anim_main(**{})'.format(kwargs)
    )
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch)
    print(cmd)
    # subprocess.call(cmd, shell=True, env=os.environ)
    subprocess.call(cmd, shell=True, env=os.environ, cwd=os.path.dirname(kwargs['input_path']), stdout=subprocess.PIPE, stderr=subprocess.PIPE, is_exe=kwargs['is_exe'])


def animAttach(**kwargs):
    maya_ver = env_load(kwargs['project'])
    # mayaBatch = maya_version(kwargs['project'], maya_ver)
    mayaBatch = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\maya.exe"
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
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    print(cmd)
    subprocess.call(cmd, shell=False, env=os.environ)


def animReplace(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    ma_current_path = kwargs['ma_current_path']
    publish_current_anim_path = kwargs['anim_current_path']
    file_namespace = kwargs['file_namespace']
    unique_order = (
        'from maya_lib.mayaBasic import *;'
        'replaceAsset(\'{}\', \'{}_anim\');'.format(publish_current_anim_path, file_namespace) +
        'save();'
    )
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    subprocess.call(cmd, shell=True, env=os.environ)

# ------------------------------------
#  Abc
# ------------------------------------
def abcExport(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    unique_order = (
            'from ndPyLibExportAbc import ndPyLibExportAbc_caller;'
            'ndPyLibExportAbc_caller({})'.format(kwargs))
    cmd = maya_cmd_maker(unique_order, mayafile=kwargs['input_path'], mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    subprocess.call(cmd, shell=True)


def abcAttach(**kwargs):
    maya_ver = env_load(kwargs['project'])
    # mayaBatch = maya_version(kwargs['project'], maya_ver)
    mayaBatch = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\maya.exe"
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
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    print("####abcAttach####")
    print(cmd)
    subprocess.call(cmd, shell=True)


def abcReplace(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    ma_current_path = kwargs['ma_current_path']
    abc_current_path = kwargs['abc_current_path']
    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'replaceABCPath(\'{}\');'.format(abc_current_path) +
            'save();')
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    print("####abcReplace####")
    print(cmd)
    subprocess.call(cmd, shell=True)

# ------------------------------------
#  Abc&Anim
# ------------------------------------
def abcAnimAttach(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
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

    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    subprocess.call(cmd, shell=True)


def abcAnimReplace(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    namespace = kwargs['file_namespace']
    ma_current_path = kwargs['ma_current_path']
    abc_current_path = kwargs['abc_current_path']
    anim_current_path = kwargs['anim_current_path']
    unique_order = (
            'from maya_lib.mayaBasic import *;'
            'replaceABCPath(\'{}\');'.format(abc_current_path) +
            'replaceAsset(\'{}\', \'{}_anim\');'.format(anim_current_path, namespace) +
            'save();')
    cmd = maya_cmd_maker(unique_order, mayafile=ma_current_path, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    subprocess.call(cmd, shell=True)


# ------------------------------------
#  Cam
# ------------------------------------
def camExport(**kwargs):
    maya_ver = env_load(kwargs['project'])
    mayaBatch = maya_version(kwargs['project'], maya_ver)
    unique_order = (
        'from ndPyLibExportCam import ndPylibExportCam_caller;'
        'ndPylibExportCam_caller(**{})'.format(kwargs))
    cmd = maya_cmd_maker(unique_order, mayafile=kwargs['input_path'],mayaBatch=mayaBatch)
    subprocess.call(cmd, shell=True, env=os.environ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ------------------------------------
#  Ass
# ------------------------------------
def assExport(**kwargs):
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\maya.exe'
    unique_order = (
            'from maya_lib.ndPyLibExportAss import export_ass_main;'
            'export_ass_main(**{})'.format(kwargs))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    subprocess.call(cmd,  shell=True)


def assAttach(**kwargs):
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\maya.exe'
    unique_order = (
            'from maya_lib.ndPyLibAttachAss import attach_ass_main;'
            'attach_ass_main(**{})'.format(kwargs))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    print(cmd)
    subprocess.call(cmd,  shell=True)


def assReplace(**kwargs):
    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2022\\bin\\maya.exe'
    unique_order = (
            'from maya_lib.ndPyLibReplaceAss import replace_ass_main;'
            'replace_ass_main(**{})'.format(kwargs))
    cmd = maya_cmd_maker(unique_order, mayaBatch=mayaBatch, is_exe=kwargs['is_exe'])
    print(cmd)
    subprocess.call(cmd,shell=True)
