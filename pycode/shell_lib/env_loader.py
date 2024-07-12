# -*- coding: utf-8 -*-
# ------------------------------
import sys
import os
sys.path.append('Y:/tool/ND_Tools/python')
sys.path.append('Y:/users/env/maya/scripts/Python/site-packages')
import ND_appEnv.lib.util.env_io as util_env

# ------------------------------
ND_TOOL_PATH_default = "Y:/tool/ND_Tools/python"

env_key = "ND_TOOL_PATH_PYTHON"
ND_TOOL_PATH = os.environ.get(env_key, ND_TOOL_PATH_default)
for path in ND_TOOL_PATH.split(';'):
    path = path.replace('\\', '/')
    if path in sys.path: continue
    sys.path.append(path)
# ------------------------------
import ND_appEnv.env as env_param
import ND_lib.shotgun.sg_scriptkey as sg_scriptkey
import yaml


# -----------------------------------
# -----------------------------------
def run(args, **kwargs):
    fork = kwargs.get('fork', True)
    # ------------------------------------
    env_key = 'ND_TOOL_PATH_PYTHON'
    ND_TOOL_PATH = os.environ.get(env_key,'Y:/tool/ND_Tools/python')
    for path in ND_TOOL_PATH.split(';'):
        path = path.replace('\\','/')
        if path in sys.path: continue
        sys.path.append(path)
    # ------------------------------------

    toolkit_path = "Y:\\tool\\ND_Tools\\shotgun"
    app_launcher_path = "config\\env\\includes\\app_launchers.yml"
    dcc_tools = ["maya", "nuke", "nukex"]

    # プロジェクト名からShotgunの設定を取得する
    project_app_launcher = "%s\\ND_sgtoolkit_%s\\%s" % (toolkit_path, args.lower(), app_launcher_path)

    if not os.path.exists(project_app_launcher.replace('/', '\\')):
        project_app_launcher = "Y:\\tool\\ND_Tools\\shotgun\\ND_sgtoolkit_{}\\config\\env\\includes\\app_launchers.yml".format(args.lower())
        if not os.path.exists(project_app_launcher):
            return None
        # project_app_launcher = "%s\\ND_sgtoolkit_%s\\%s" % (toolkit_path, args.lower(), app_launcher_path)

    f = open(project_app_launcher, "r")
    data = yaml.safe_load(f)

    f.close()

    for dcc in dcc_tools:
        for version in data["launch_%s" % dcc]["versions"]:
            args = data["launch_%s" % dcc]["windows_args"]
            if dcc == 'maya':
                renderinfo = version.replace('(','').split(')')

    renderer = renderinfo[1].replace('_','').upper()
    rendver = renderinfo[2]
    ryear = renderinfo[0]
    oe = "_TMP_" + renderer + "_VER"
    os.environ[oe] = rendver

    argslist = args.split(' ')
    args = argslist[0].lower()

    values_ana = [args+'/maya/'+ryear+'/amd64/win']
    app_mode = values_ana.pop(0)
    # -----------------------------------
    filePath = '/'.join([env_param.data_path, "dummy.json"])
    # -----------------------------------
    keys = ["name", "appName", "version", "osType", "osName"]
    values = ["ndesign_base", ".", ".", ".", "."]
    options = app_mode.split('/')
    values[:len(options)] = options
    options = dict(zip(keys, values))

    # -----------------------------------
    envDict = util_env.loadConf(filePath, **options)
    # env = util_env.getEnvDict(envDict, env=os.environ, expand=True)

# -----------------------------------
def load_sg_info(project_name):
    # shotgun_api3
    sg = sg_scriptkey.scriptKey()
    project = sg.find_one("Project", [["name", "is", project_name.upper()]], ["id"])  # プロジェクト指定
    sg_data_list = sg.find(
        "Software",
        [["projects", "in", project]],
        ["sg_status", "code", "windows_args"],
    )
    maya_ver = 2020
    arnold_ver = 0
    for sg_data in sg_data_list:
        if "Maya" in sg_data["code"]:
            if sg_data["windows_args"] is None or len(sg_data["windows_args"].split(" ")) < 3:
                continue
            if maya_ver < int(sg_data["windows_args"].split(" ")[1]):
                maya_ver = int(sg_data["windows_args"].split(" ")[1])
            if "MtoA" in sg_data["code"]:
                if arnold_ver < int(sg_data["windows_args"].split(" ")[2]):
                    arnold_ver = int(sg_data["windows_args"].split(" ")[2])
    return maya_ver, arnold_ver


def set_arnold_env(project_name):
    maya_ver, arnold_ver = load_sg_info(project_name)
    if arnold_ver == 0:
        return maya_ver
    # arnold
    sys.path.append('Y:/users/env/arnold/mtoa/{}_MtoA_{}/scripts'.format(maya_ver, arnold_ver))
    sys.path.append('Y:/users/env/maya/Python3/scripts/Python/site-packages')
    # scripts
    scripts_path = 'Y:/users/env/arnold/mtoa/{}_MtoA_{}/scripts'.format(maya_ver, arnold_ver)
    if os.environ.get("PYTHONPATH"):
        os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ";" + scripts_path
    else:
        os.environ["PYTHONPATH"] = (
            scripts_path
            + ";C:/Program Files/Autodesk/Maya{}/Python/lib/site-packages".format(maya_ver)
        )

    os.environ['MAYA_SCRIPT_PATH'] = scripts_path
    # plug-in
    plugin_path = 'Y:/users/env/arnold/mtoa/{}_MtoA_{}/plug-ins'.format(maya_ver, arnold_ver)
    # os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH'].rstrip(';') + ';' + plugin_path
    os.environ['MAYA_PLUG_IN_PATH'] = plugin_path
    # mod
    mod_path = "Y:/users/env/maya/2023/mod;Y:/users/env/arnold/mtoa/2023_MtoA_5133"
    # os.environ['MAYA_MODULE_PATH']  = os.environ['MAYA_MODULE_PATH'].rstrip(';') + ';' + mod_path
    os.environ['MAYA_MODULE_PATH'] = mod_path
    # path
    os.environ['PATH'] = os.environ['PATH'].rstrip(';') + ';' + 'Y:/users/env/arnold/mtoa/{}_MtoA_{}/bin'.format(maya_ver, arnold_ver)
    os.environ["_MAYA_PYTHON_VER"] ="2_7_x"
    return maya_ver
