# -*- coding: utf-8 -*-
#------------------------------
import sys
import os
sys.path.append('Y:/tool/ND_Tools/python')
sys.path.append('Y:/users/env/maya/scripts/Python/site-packages')
import ND_appEnv.lib.util.env_io as util_env

#------------------------------
ND_TOOL_PATH_default = "Y:/tool/ND_Tools/python"

env_key = "ND_TOOL_PATH_PYTHON"
ND_TOOL_PATH = os.environ.get(env_key, ND_TOOL_PATH_default)
for path in ND_TOOL_PATH.split(';'):
    path = path.replace('\\', '/')
    if path in sys.path: continue
    sys.path.append(path)

#------------------------------
import ND_appEnv.env as env_param
import yaml


#-----------------------------------
#-----------------------------------
def run(args, **kwargs):
    fork = kwargs.get('fork', True)
    #------------------------------------
    env_key = 'ND_TOOL_PATH_PYTHON'
    ND_TOOL_PATH = os.environ.get(env_key,'Y:/tool/ND_Tools/python')
    for path in ND_TOOL_PATH.split(';'):
        path = path.replace('\\','/')
        if path in sys.path: continue
        sys.path.append(path)
    #------------------------------------

    toolkit_path = "Y:\\tool\\ND_Tools\\shotgun"
    app_launcher_path = "config\\env\\includes\\app_launchers.yml"
    dcc_tools = ["maya", "nuke", "nukex"]


    #プロジェクト名からShotgunの設定を取得する
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
    #-----------------------------------
    filePath = '/'.join([env_param.data_path, "dummy.json"])
    #-----------------------------------
    keys = ["name", "appName", "version", "osType", "osName"]
    values = ["ndesign_base", ".", ".", ".", "."]
    options = app_mode.split('/')
    values[:len(options)] = options
    options = dict(zip(keys, values))

    #-----------------------------------
    envDict = util_env.loadConf(filePath, **options)
    # env = util_env.getEnvDict(envDict, env=os.environ, expand=True)
