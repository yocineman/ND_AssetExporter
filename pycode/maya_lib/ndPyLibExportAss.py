#coding:utf-8
import maya.cmds as cmds
import re
import os
import sys

def export_ass_main(**kwargs):
    regex_list = kwargs['namespace']
    frame_range = kwargs['frame_range']
    top_node = kwargs['top_node']
    print("###exp_ass_above#")

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

    # シーンのオープン
    cmds.file(kwargs['input_path'], o=True, f=True)

    # フレームレンジの設定
    if frame_range != False:
        sframe = frame_range[0]
        eframe = frame_range[1]
    else:
        sframe = cmds.playbackOptions(q=True, min=True)
        eframe = cmds.playbackOptions(q=True, max=True)
    sframe -= float(kwargs['frame_handle'])
    eframe += float(kwargs['frame_handle'])

    # ターゲットとなるネームスペースの検索
    tg_ns_list = []

    namespaces = cmds.namespaceInfo(lon=True, r=True)
    for scene_ns in namespaces:
        for input_ns in regex_list:
            match = re.match(input_ns, scene_ns)
            print(input_ns, scene_ns, match)
            if match != None:
                tg_ns_list.append(scene_ns)

    for tg_ns in tg_ns_list:
        ns_top_node =  tg_ns + ":" + top_node
        if not cmds.objExists(ns_top_node):
            continue
        ass_file_name = tg_ns+'.ass'
        ass_file_path = kwargs['publish_ver_ass_path']+'/'+ass_file_name
        cmds.select(ns_top_node)
        cmds.arnoldExportAss(ns_top_node, f=ass_file_path, mask=6393, lightLinks=True, s=True, boundingBox=True, sf=sframe, ef=eframe)

def ndPyLibExportAss_caller(args):
    export_ass_main(**args)
