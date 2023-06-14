# coding:utf-8

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import pprint
import os,sys
import re
try:
    from importlib import reload
except:
    pass

sys.path.append(r"Y:\tool\ND_Tools\DCC\dev\standalone\ND_AssetExporter\pycode\maya_lib")
import ndPyLibAnimIOExportContain; reload(ndPyLibAnimIOExportContain)

def set_dw_h_env():
    # 環境変数の設定
    # arnold
    sys.path.append('Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts')
    try:
        import arnold
    except:
        pass
    # scripts
    scripts_path = 'Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts'
    os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'].rstrip(';') + ';' + scripts_path
    os.environ['MAYA_SCRIPT_PATH'] = os.environ['MAYA_SCRIPT_PATH'] + ';' + scripts_path
    # plug-in
    plugin_path = 'Y:/users/env/arnold/mtoa/2020_MtoA_5211/plug-ins'
    os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH'].rstrip(';') + ';' + plugin_path
    # mod
    mod_path = 'Y:/users/env/maya/2020/mod'
    # os.environ['MAYA_MODULE_PATH']  = os.environ['MAYA_MODULE_PATH'].rstrip(';') + ';' + mod_path
    os.environ['MAYA_MODULE_PATH'] = mod_path
    os.environ["PYTHONPATH"] = "P:/Project/D_WH/Library/Tool/maya/scripts/python;Z:/DeadlineRepository10/api/python/Deadline;Y:/tool/ND_Tools/shotgun/ND_sgtoolkit_d_wh/install/core/python;Y:/tool/ND_Tools/shotgun/ND_sgtoolkit_d_wh/install/app_store/tk-maya/v0.11.3/startup;P:/Project/d_wh/Library/users/k_ueda/maya/scripts;Y:/users/env/maya/share/nStup;Y:/users/env/maya/share/tpro;Y:/users/env/maya/share/nDef;Y:/users/env/maya/share/nDev;Y:/users/env/maya/share/nBB;Y:/users/env/maya/share/nDyn;Y:/users/env/maya/share/nShd;Y:/users/env/maya/share/nSelect;Y:/users/env/maya/share/nUtil;Y:/users/env/maya/share/nRend;Y:/users/env/maya/share/startup;Y:/users/env/maya/share/nMod;Y:/users/env/maya/share/nAnim;Y:/users/k_ueda/maya/guren2;Y:/pub/Tools/numpy-unoptimized-1.7.1.win-amd64-py2.7/Lib/site-packages;Y:/users/env/maya/scripts/Python/site-packages;Y:/users/env/maya/share/nAnim/studiolibrary/src;Y:/users/env/maya/share/nAnim/studiolibrary/src/mutils;Y:/users/env/maya/share/nAnim/studiolibrary/src/studiolibrary;Y:/users/env/maya/share/nAnim/studiolibrary/src/studiolibrarymaya;Y:/users/env/maya/share/nAnim/studiolibrary/src/studioqt;Y:/users/env/maya/share/nAnim/studiolibrary/src/studiovendor;Y:/tool/ND_Tools/DCC/ND_AssetExporter/pycode/maya_lib/OnMayaTool;Y:/users/env/maya/scripts;Y:/users/env/maya/2020/scripts;P:/Project/d_wh/Library/users/k_ueda/maya/2020/scripts;Y:/users/env/maya/2020/scripts/python;Y:/pub/Tools/JCGS_Projects/ndesign_base/lib;Y:/tool/MISC/Python2710_amd64_vs2010/Lib/site-packages-new;C:/Program Files/Autodesk/Maya2020/Python/Lib/site-packages;P:/Project/D_WH/Library/Tool/maya;P:/Project/D_WH/Library/Tool/maya/scripts;Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/scripts;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/scripts;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/scripts;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/scripts;Y:/users/env/maya/2019/tools/nimbleTools/scripts;C:/Program Files/Rokoko Motion Library/Maya/2020/scripts;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/scripts;C:/Program Files/Autodesk/Maya2020/plug-ins/fbx/scripts;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/scripts;C:/Program Files/Autodesk/Maya2020/plug-ins/camd/scripts;Y:/users/env/maya/2020/modules/medic/scripts;Y:/users/env/maya/2017-x64/tools/Yeti-v2.2.10_Maya2017-windows64/scripts;C:/Program Files/Allegorithmic/Substance in Maya/2020/scripts;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/scripts;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/scripts;Y:/users/env/maya/scripts/zync-maya/scripts;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/python/site-packages;Y:/users/env/maya/2020/modules/medic/py"
    os.environ["XBMLANGPATH"] = "Y:/users/env/maya/share/nAnim/maya-keyframe-reduction/icons;P:/Project/d_wh/Library/users/k_ueda/maya/2020/prefs/icons;Y:/users/env/maya/2020/prefs/icons;Y:/users/env/maya/2020/mentalray/icons;Y:/users/env/maya/2020/tools/shaveHaircut/maya2009/presets/attrPresets/shaveHair;Y:/users/env/arnold/mtoa/2020_MtoA_5211/icons;P:/Project/d_wh/Library/users/k_ueda/maya/prefs/icons;C:/Program Files/Autodesk/Maya2020/icons;C:/Program Files/Autodesk/Maya2020/app-defaults;C:/Program Files/Autodesk/Maya2020/icons/paintEffects;C:/Program Files/Autodesk/Maya2020/icons/fluidEffects;C:/Program Files/Autodesk/Maya2020/icons/hair;C:/Program Files/Autodesk/Maya2020/icons/cloth;C:/Program Files/Autodesk/Maya2020/icons/live;C:/Program Files/Autodesk/Maya2020/icons/fur;C:/Program Files/Autodesk/Maya2020/icons/muscle;C:/Program Files/Autodesk/Maya2020/icons/turtle;C:/Program Files/Autodesk/Maya2020/icons/FBX;C:/Program Files/Autodesk/Maya2020/icons/mayaHIK;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/icons;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/icons;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/icons;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/icons;Y:/users/env/maya/2019/tools/nimbleTools/icons;C:/Program Files/Rokoko Motion Library/Maya/2020/icons;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/icons;C:/Program Files/Autodesk/Maya2020/plug-ins/fbx/icons;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/icons;C:/Program Files/Autodesk/Maya2020/plug-ins/camd/icons;Y:/users/env/maya/2020/modules/medic/icons;Y:/users/env/maya/2017-x64/tools/Yeti-v2.2.10_Maya2017-windows64/icons;C:/Program Files/Allegorithmic/Substance in Maya/2020/icons;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/icons;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/icons;Y:/users/env/maya/scripts/zync-maya/icons"
    os.environ["MAYA_PLUG_IN_PATH"] = "P:/Project/d_wh/Library/users/k_ueda/maya/2020/plug-ins;Y:/users/env/maya/2020/plug-ins;P:/Project/D_WH/Library/Tool/maya/plug-ins;Y:/users/env/arnold/mtoa/2020_MtoA_5211/plug-ins;P:/Project/d_wh/Library/users/k_ueda/maya/plug-ins;C:/Program Files/Autodesk/Maya2020/bin/plug-ins;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/plug-ins;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/plug-ins;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/plug-ins;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/plug-ins;Y:/users/env/maya/2019/tools/nimbleTools/plug-ins;C:/Program Files/Rokoko Motion Library/Maya/2020/plug-ins;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/plug-ins;C:/Program Files/Autodesk/Maya2020/plug-ins/fbx/plug-ins;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/plug-ins;C:/Program Files/Autodesk/Maya2020/plug-ins/camd/plug-ins;Y:/users/env/maya/2020/modules/medic/plug-ins;Y:/users/env/maya/2017-x64/tools/Yeti-v2.2.10_Maya2017-windows64/plug-ins;C:/Program Files/Allegorithmic/Substance in Maya/2020/plug-ins;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/plug-ins;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/plug-ins;Y:/users/env/maya/scripts/zync-maya/plug-ins;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/plug-ins/win64-2020"
    os.environ["MAYA_PXR_PLUGINPATH_NAME"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/usd"
    os.environ["ARNOLD_PLUGIN_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/procedurals;Y:/users/env/arnold/mtoa/2020_MtoA_5211/shaders;Y:/users/env/arnold/mtoa/2020_MtoA_5211/shaders;Y:/users/env/arnold/mtoa/2020_MtoA_5211/procedurals"
    os.environ["MAYA_RENDER_DESC_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211"
    os.environ["MTOA_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/"
    os.environ["MAYA_CUSTOM_TEMPLATE_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts/mtoa/ui/templates"
    os.environ["PATH"] = "C:/Program Files/Autodesk/Maya2020/Python/Lib/site-packages/PySide2;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/ATF;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/ATF/alias;C:/Program Files/Autodesk/Maya2020/bin/Cg;C:/Program Files/Autodesk/Maya2020/bin;Y:/tool/MISC/Python2710_amd64_vs2010;C:/Program Files/Shotgun/Python/lib/site-packages/pywin32_system32;C:/Program Files/Shotgun/Python3/lib/site-packages/PySide2;C:/Program Files/Shotgun/Python3/lib/site-packages/pywin32_system32;C:/Program Files (x86)/Intel/iCLS Client/;C:/Program Files/Intel/iCLS Client/;C:/Windows/system32;C:/Windows;C:/Windows/System32/Wbem;C:/Windows/System32/WindowsPowerShell/v1.0/;C:/Windows/System32/OpenSSH/;C:/Program Files (x86)/Intel/Intel(R) Management Engine Components/DAL;C:/Program Files/Intel/Intel(R) Management Engine Components/DAL;C:/Program Files (x86)/Intel/Intel(R) Management Engine Components/IPT;C:/Program Files/Intel/Intel(R) Management Engine Components/IPT;C:/Program Files (x86)/QuickTime/QTSystem/;C:/Program Files/Git/cmd;C:/Users/k_ueda/AppData/Local/Microsoft/WindowsApps;C:/Users/k_ueda/AppData/Local/Programs/Microsoft VS Code/bin;%MAYA_LOCATION%/bin;Y:/users/env/maya/2020/dll;Y:/users/env/arnold/mtoa/2020_MtoA_5211/bin;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/bin;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/bin;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/bin;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/../../../bin;Y:/users/env/maya/2020/modules/medic/bin;C:/Program Files/Allegorithmic/Substance in Maya/2020/lib;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/bin;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/bin"
    os.environ["MTOA_EXTENSIONS_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/extensions;Y:/users/env/arnold/mtoa/2020_MtoA_5211/extensions"
    os.environ["ARNOLD_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211"
    os.environ["MTOA_SCRIPT_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts;Y:/users/env/arnold/mtoa/2020_MtoA_5211/scripts/mtoa/mel"
    os.environ["MAYA_PLUG_IN_RESOURCE_PATH"] = "Y:/users/env/arnold/mtoa/2020_MtoA_5211/resources;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/resources;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/resources;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/resources;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/resources;Y:/users/env/maya/2019/tools/nimbleTools/resources;C:/Program Files/Rokoko Motion Library/Maya/2020/resources;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/resources;C:/Program Files/Autodesk/Maya2020/plug-ins/fbx/resources;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/resources;C:/Program Files/Autodesk/Maya2020/plug-ins/camd/resources;Y:/users/env/maya/2020/modules/medic/resources;Y:/users/env/maya/2017-x64/tools/Yeti-v2.2.10_Maya2017-windows64/resources;C:/Program Files/Allegorithmic/Substance in Maya/2020/resources;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/resources;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/resources;Y:/users/env/maya/scripts/zync-maya/resources;"
    os.environ["MAYA_PRESET_PATH"] = "P:/Project/d_wh/Library/users/k_ueda/maya/2020/presets;Y:/users/env/maya/2020/presets;Y:/users/env/arnold/mtoa/2020_MtoA_5211/presets;C:/Program Files/Autodesk/Maya2020/plug-ins/ATF/presets;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/bifrost/presets;C:/Program Files/Autodesk/Maya2020/plug-ins/MASH/presets;C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2018-2022/Contents/presets;Y:/users/env/maya/2019/tools/nimbleTools/presets;C:/Program Files/Rokoko Motion Library/Maya/2020/presets;C:/ProgramData/Autodesk/ApplicationPlugins/MayaScanner/Contents/presets;C:/Program Files/Autodesk/Maya2020/plug-ins/fbx/presets;C:/Program Files/Side Effects Software/Houdini 19.5.493/engine/maya/maya2020/presets;C:/Program Files/Autodesk/Maya2020/plug-ins/camd/presets;Y:/users/env/maya/2020/modules/medic/presets;Y:/users/env/maya/2017-x64/tools/Yeti-v2.2.10_Maya2017-windows64/presets;C:/Program Files/Allegorithmic/Substance in Maya/2020/presets;C:/Program Files/Autodesk/Bifrost/Maya2020/2.2.0.0/vnn/presets;C:/Program Files/Autodesk/Maya2020/plug-ins/xgen/presets;Y:/users/env/maya/scripts/zync-maya/presets"

    try:
        cmds.loadPlugin('mtoa')
    except:
        pass


def set_env():
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


def export_anim_main(**kwargs):
    pprint.pprint(kwargs.items())
    if kwargs['project'].lower() == 'd_wh':
        set_dw_h_env()
    else:
        set_env()

    # シーンのオープン
    cmds.file(kwargs['input_path'], o=True, f=True)

    #  evaluateの設定
    evaluate = kwargs['evaluate']
    if evaluate != False:
        if evaluate == 'DG':
            cmds.evaluationManager(mode='off')
        else:
            cmds.evaluationManager(mode=evaluate)
    #  cacheをハイド
    top_nodes = cmds.ls(assemblies=True)
    cache_nodes = cmds.ls(type='cacheFile')
    hidden_objs = []
    hidden_objs.extend(cmds.hide(top_nodes, rh=True))
    hidden_objs.extend(cmds.hide(cache_nodes, rh=True))
    ignore_attrs = []
    if hidden_objs is not None:
        for obj in hidden_objs:
            ignore_attrs.append('{}.visibility'.format(obj.lstrip('|')))

    output_files = []
    tg_nodes = []
    node_and_attrs = []

    frame_handle = kwargs['frame_handle']
    publish_ver_anim_path = kwargs['publish_ver_anim_path']

    sframe = cmds.playbackOptions(q=True, min=True) - float(frame_handle)
    eframe = cmds.playbackOptions(q=True, max=True) + float(frame_handle)

    if 'frame_range' in kwargs.keys():
        frame_range = kwargs['frame_range']
    else:
        frame_range = [sframe, eframe]
    if 'on_maya' in kwargs.keys():
        frame_range = [sframe, sframe+1]

    with open(os.path.dirname(os.path.dirname(os.path.dirname(publish_ver_anim_path))) + '/sceneConf.txt', 'w') as f:
        f.write(str(sframe)+'\n')
        f.write(str(eframe)+'\n')
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(publish_ver_anim_path))), "resolutionConf.txt"), "w") as f:
        f.write(str(cmds.getAttr("defaultResolution.width"))+"\n")
        f.write(str(cmds.getAttr("defaultResolution.height"))+"\n")

    input_ns_list = kwargs['namespace'][0].replace(' ', '').rstrip(',').split(',')
    regex_list = [i for i in kwargs['export_item']['anim'].replace(' ', '').replace('vertical_bar', '|').split(',') if not '.' in i]  # 通常のエクスポート対象
    regex_attr_list = [i for i in kwargs['export_item']['anim'].split(',') if '.' in i]  # アトリビュートを直接指定

    if kwargs['load_pref'] == True:
        unload_ns_dic = get_unload_ns_dic()
        tg_ns_list = get_tg_ns_list(unload_ns_dic.keys(), input_ns_list)
        for tg_ns in tg_ns_list:
            ref = unload_ns_dic[tg_ns]
            cmds.file(lr=ref)

    scene_ns_list = get_scene_ns_list()
    tg_ns_list = get_tg_ns_list(scene_ns_list, input_ns_list)
    if len(tg_ns_list) == 0:
        print('Namespaceが見つかりませんでした。')
        return False
    tg_nodes = get_tg_nodes(tg_ns_list, regex_list)
    for regex_attr in regex_attr_list:
        tg_nodes.append(regex_attr.split('.')[0])

    if len(tg_nodes) == 0:
        print('(正規表現とマッチするオブジェクト)が見つかりませんでした。')

    character_set = cmds.ls(type='character')
    if len(character_set) != 0:
        cmds.delete(character_set)

    mergeAnimLayers()

    baseAnimationLayer = cmds.animLayer(q=True, r=True)
    if baseAnimationLayer != None and len(cmds.ls(sl=True)) != 0:
        animLayers = cmds.ls(type='animLayer')
        for al in animLayers:
            cmds.animLayer(al, e=True, sel=False)
        cmds.bakeResults(baseAnimationLayer, t=(sframe, eframe), sb=True, ral=True, sm=True, dic=True)

    for tg_node in tg_nodes[:]:
        if cmds.objExists(tg_node) == False:
            tg_nodes.remove(tg_node)

    attrs = getNoKeyAttributes(tg_nodes)
    if len(node_and_attrs) != 0:
        attrs.extend(getNoKeyAttributes(node_and_attrs))
    for tg_ns in tg_ns_list:
        for regex_obj_and_attr in regex_attr_list:
            obj_and_attr = tg_ns+':' + regex_obj_and_attr
            if cmds.objExists(obj_and_attr):
                attrs.append(obj_and_attr)

    if len(attrs) != 0:
        attrs = list(set(attrs)-set(ignore_attrs))
        cmds.setKeyframe(attrs, t=sframe)

    attrs += getConstraintAttributes(tg_nodes)
    attrs += getMotionPathAttributes(tg_nodes)
    attrs += getAddDoubleLinearAttributes(tg_nodes)
    attrs += getTransformConnectionAttributes(tg_nodes)
    attrs += getExpression(tg_nodes)
    attrs += getKeyAttributes(tg_nodes)
    attrs += getAnimLayerConnectionAttributes(tg_nodes)
    attrs += getPairBlendAttributes(tg_nodes)
    attrs = list(set(attrs)-set(ignore_attrs))
    unlockAttributes(attrs)

    for node in tg_nodes:
        if cmds.listConnections(node, s=True, type="constraint") is not None:
            attrs.extend(
                list(set(cmds.listConnections(node, s=True, type="constraint"))))

    # SceneTimeWarp
    if kwargs['scene_timewarp'] == True or kwargs['scene_timewarp'] == 'True':
        time_set_list = []
        time_value_set_list = []

        cmds.setAttr("time1.enableTimewarp", 1)

        step_value = kwargs['step_value']
        _frame = sframe
        while True:
            cmds.currentTime(_frame)
            warp_time = cmds.getAttr("time1.outTime", time=_frame)
            time_set_list.append([_frame, warp_time])
            _frame += step_value
            if _frame > eframe:
                break

        # for t in range(int(sframe),int(eframe+1)):
        #     cmds.currentTime(t)
        #     warp_time = cmds.getAttr("time1.outTime", time=t)
        #     time_set_list.append([t, warp_time])

        cmds.setAttr("time1.enableTimewarp", 1)
        for time_set in time_set_list:
            t = time_set[0]
            warp_time = time_set[1]
            cmds.currentTime(t)
            for attr in attrs:
                try:
                    value = cmds.getAttr(attr)
                    time_value_set_list.append([t, attr, value])
                except Exception as e:
                    print(e)
        cmds.setAttr("time1.enableTimewarp", 0)
        for attr in attrs:
            cmds.keyTangent(attr, edit=True, itt="linear", ott="linear")

        for time_list in time_value_set_list:
            attr = time_list[1]
            try:
                source_attrs = cmds.listConnections(attr, d=False, s=True, p=True)
                if source_attrs is not None:
                    for source in source_attrs:
                        if source.split('.')[-1]!='output':
                            cmds.disconnectAttr(source, attr)
            except Exception as e:
                print(e)

        for time_list in time_value_set_list:
            frame = time_list[0]
            attr = time_list[1]
            value = time_list[2]
            cmds.currentTime(frame)
            # print(frame, attr, value)
            try:
                cmds.setAttr(attr, value)
                cmds.setKeyframe(attr, v=value, t=frame)
            except Exception as e:
                pass
    # 通常のベイク
    else:
        attrs = list(set(attrs)-set(ignore_attrs))
        for obj_and_attr in attrs:
            if cmds.objExists(obj_and_attr) == True:
                cmds.select(obj_and_attr, add=True)
        # print(sframe, eframe)
        _attrs = []
        for attr in attrs[:]:
            if not '.visiblity' in attr:
                _attrs.append(attr)
        cmds.select(_attrs)
        print(_attrs)
        print(tg_nodes)
        # cmds.bakeResults(tg_nodes, t=(sframe, eframe), dic=True, sm=True)
        cmds.bakeResults(tg_nodes, t=(sframe, eframe), dic=True, sm=True, ral=True)


    for obj in hidden_objs:
        try:
            dst_obj = '{}.visibility'.format(obj.split('|')[-1])
            src_obj = cmds.listConnections(dst_obj, p=True)[0]
            cmds.disconnectAttr(src_obj, dst_obj)
        except Exception as e:
            print(e)
    try:
        cmds.showHidden(hidden_objs)
            # if 'on_maya' in kwargs.keys():
            #     return
    except:
        pass
    print('###scene_ns_list####################')
    pprint.pprint(scene_ns_list)
    print('###tg_ns_list#######################')
    pprint.pprint(tg_ns_list)
    print('###tg_nodes########################')
    pprint.pprint(tg_nodes)
    print('####################################')
    for ns in tg_ns_list:
        pick_nodes = []
        pick_node_and_attrs = []
        for node in tg_nodes:
            if 'Geo.' in node:
                continue
            if 'geo.' in node:
                continue
            if 'GEO.' in node:
                continue
            if ns+':' in node:
                pick_nodes.append(node)
        for node in pick_node_and_attrs:
            if ns + ':' in node:
                pick_node_and_attrs.append(node)

        if len(pick_nodes) != 0 or len(pick_node_and_attrs) != 0:
            argsdic = {}
            argsdic['is_filter'] = True
            argsdic['anim_file_name'] = 'anim_'+ns+'.ma'
            argsdic['publish_ver_anim_path'] = kwargs['publish_ver_anim_path']
            argsdic['pick_nodes'] = pick_nodes
            argsdic['pick_node_and_attrs'] = pick_node_and_attrs
            argsdic['frame_range'] = frame_range
            argsdic['scene_timewarp'] = kwargs['scene_timewarp']
            argsdic['is_check_constraint'] = True
            argsdic['is_check_anim_curve'] = True
            ndPyLibAnimIOExportContain.ndPyLibAnimIOExportContain_main(**argsdic)
    return output_files



def eulerfilter(attr_list):
    for attr in attr_list:
        try:
            anim_cv = map(lambda x: x.rstrip('.output'), attr)
            anim_cv = filter(lambda x: cmds.nodeType(x) in [
                             'animCurveTL', 'animCurveTU', 'animCurveTA', 'animCurveTT'], anim_cv)
            cmds.filterCurve(anim_cv, f='euler')
        except:
            continue


def get_reference_file(obj):
    return cmds.referenceQuery(obj, f=True)


def reference_ma(ma, ns):
    # cmds.file(ma, reference=True, ns=ns, force=False, pmt=True)
    pprint.pprint(cmds.file(ma, i=True, ns=ns, force=True, pmt=True))
    return ma


def get_scene_ns_list():
    namespaces = cmds.namespaceInfo(lon=True)
    _nestedNS = []
    for ns in namespaces:
        try:
            nestedNS = cmds.namespaceInfo(ns, lon=True)
            if nestedNS != None:
                _nestedNS += nestedNS
        except:
            continue
    namespaces += _nestedNS
    try:
        namespaces.remove('UI')
        namespaces.remove('shared')
    except:
        pass
    return namespaces


def get_tg_ns_list(scene_ns_list, input_ns_list):
    tg_ns_list = []
    for scene_ns in scene_ns_list:
        for input_ns in input_ns_list:
            match = re.match(input_ns+'$', scene_ns)
            if match != None and ':' not in scene_ns:
                tg_ns_list.append(scene_ns)
    return tg_ns_list


def get_rec_sets(set):
    set_items = cmds.sets(set, q=True)
    print('####set')
    print(set, set_items)
    result = []
    if set_items == None:
        return None
    for set_item in set_items:
        if cmds.objectType(set_item) == 'objectSet':
            _res = get_rec_sets(set_item)
            if _res != None:
                result.extend(_res)
        else:
            result.append(set_item)
    return result


def get_tg_nodes(ns_list, regex_list):
    all_objs = cmds.ls()
    result_nodes = []
    for ns in ns_list:
        nodes = []
        for regex in regex_list:
            if regex == '':
                continue
            for i in all_objs:
                if re.search('{}:{}'.format(ns, regex), i) != None:
                    nodes.append(i)
        nodes = list(set(nodes))
        for node in nodes[:]:
            if cmds.objExists(node) == False:
                nodes.remove(node)
                continue
            if cmds.objectType(node) == 'objectSet':
                _nodes = get_rec_sets(node)
                if _nodes != None:
                    nodes.extend(_nodes)
        result_nodes.extend(nodes)
    return list(set(result_nodes))


def getConstraintAttributes(nodes):
    attrs = []
    for n in nodes:
        const = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='constraint')
        if const is None:
            continue
        for i in range(0, len(const), 2):
            attrs.append(const[i])
    return attrs


def getPairBlendAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='pairBlend')
        if pairblend is None:
            continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
            const = cmds.listConnections(
                pairblend, s=True, d=False, p=False, c=True, t='constraint')
            if const is None:
                continue
            for i in range(0, len(const), 2):
                attrs.append(const[i])
    return attrs


def getMotionPathAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='motionPath')
        if pairblend is None:
            continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
    return attrs


def getAddDoubleLinearAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='addDoubleLinear')
        if pairblend is None:
            continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
    return attrs


def getTransformConnectionAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='transform')
        if pairblend is None:
            continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
    return attrs


def getAnimLayerConnectionAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='animLayer')
        if pairblend is None:
            continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
    return attrs


def getAnimCurveAttributes(nodes):
    attrs = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='animCurveTL')
        if pairblend is not None:
            for i in range(0, len(pairblend), 2):
                attrs.append(pairblend[i])
                continue
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='animCurveTU')
        if pairblend is not None:
            for i in range(0, len(pairblend), 2):
                attrs.append(pairblend[i])
                continue
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='animCurveTA')
        if pairblend is not None:
            for i in range(0, len(pairblend), 2):
                attrs.append(pairblend[i])
                continue
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='animCurveTT')
        if pairblend is not None:
            for i in range(0, len(pairblend), 2):
                attrs.append(pairblend[i])
                continue
    return attrs


def getNoKeyAttributes(nodes):
    attrs = []
    for n in nodes:
        if '.' in n:
            n = n.split('.')[0]
        gAttrs = cmds.listAttr(n, keyable=True)
        if gAttrs is None:
            continue
        for attr in gAttrs:
            if '.' not in attr:
                if cmds.listConnections(n+'.'+attr, s=True, d=False) is None:
                    attrs.append(n+'.'+attr)
    return attrs


def getKeyAttributes(nodes):
    attrs = []
    for n in nodes:
        if '.' in n:
            n = n.split('.')[0]
        gAttrs = cmds.listAttr(n, keyable=True)
        if gAttrs is None:
            continue
        for attr in gAttrs:
            if '.' not in attr:
                if cmds.listConnections(n+'.'+attr, s=True, d=False) is None:
                    pass
                else:
                    attrs.append(n+'.'+attr)
    return attrs


def getNodehasPairBlends(nodes):
    result_nodes = []
    for n in nodes:
        pairblend = cmds.listConnections(
            n, s=True, d=False, p=False, c=False, t='pairBlend')
        if pairblend is not None:
            result_nodes.append(n)
    return result_nodes


def getPairBlend(node):
    pairblends = cmds.listConnections(
        node, s=True, d=False, p=False, c=False, t='pairBlend')
    if pairblends is not None:
        for pairblend in pairblends:
            if "pairBlend" in pairblend:
                return pairblend
    return pairblend


def getExpression(nodes):
    attrs = []
    for n in nodes:
        expression = cmds.listConnections(
            n, s=True, d=False, p=False, c=True, t='expression')
        if expression is not None:
            for i in range(0, len(expression), 2):
                attrs.append(expression[i])
                continue
        if cmds.objectType(n) == 'expression':
            attrs.append(n)
    return attrs


def replacePairBlendstoLocator(nodes, sframe, eframe):
    for node in nodes:
        if "Constraint" in node:
            continue
        blend_attrs = ["outTranslateX", "outTranslateY",
                       "outTranslateZ", "outRotateX", "outRotateY", "outRotateZ"]
        nml_attrs = ["translateX", "translateY",
                     "translateZ", "rotateX", "rotateY", "rotateZ"]
        blend = getPairBlend(node)
        loc = cmds.spaceLocator(n="tmp")[0]
        for blend_attr, attr in zip(blend_attrs, nml_attrs):
            cmds.connectAttr("{}.{}".format(blend, blend_attr),
                             "{}.{}".format(loc, attr))
        cmds.bakeResults(loc, t=(sframe, eframe))
        cmds.delete(blend)
        connect_nodes = cmds.listConnections(node, p=True, s=True)
        for connect_node in connect_nodes:
            if connect_node.split(".")[-1] == "output":
                try:
                    cmds.delete(connect_node.split(".")[0])
                except:
                    pass
        for attr in nml_attrs:
            cmds.connectAttr("{}.{}".format(loc, attr),
                             "{}.{}".format(node, attr))
        cmds.bakeResults(node, t=(sframe, eframe))
        cmds.delete(loc)


def unlockAttributes(nodes):
    for node in nodes:
        if cmds.getAttr(node, lock=True):
            try:
                cmds.setAttr(node, lock=False)
            except Exception as e:
                pass



def mergeAnimLayers():
    mel.eval('source "C:/Program Files/Autodesk/Maya2020/scripts/others/performAnimLayerMerge.mel"'.format(pm.about(version=True)))
    animLayers = cmds.ls(type='animLayer')
    if animLayers:
        try:
            mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))
        except:
            pass
    return


def get_unload_ns_dic():
    unLoaded_ref_dic = {}
    refList = cmds.ls(type='reference')
    for ref in refList:
        if ref == 'sharedReferenceNode':
            continue
        try:
            if cmds.referenceQuery(ref, isLoaded=True):
                # print(ref)
                pass
            else:
                ref_path = cmds.referenceQuery(ref, filename=True)
                ref_ns = cmds.file(ref_path, q=True, ns=True)
                unLoaded_ref_dic[ref_ns] = ref
        except Exception as e:
            print(e)
            # cmds.file(lr=ref)
    return unLoaded_ref_dic



def ndPyLibExportAnim_caller(args):
    export_anim_main(**args)
    print("ndPylibExportAnim End")


def test_caller():
    kwargs = {}
    kwargs['scene_timewarp'] = False
    kwargs['publish_ver_anim_path'] = 'P:/Project/D_WH/shots/ep0/000000/00000/publish/test_charSet/KatarsNml/v006/anim'
    kwargs['export_item'] = {'anim': 'rig_set,main,mainA,mainB,mainC,eyeAimLeft_cnt,eyeAimRight_cnt,eyeAimAll_cnt', 'abc': None}
    # kwargs['export_item'] = {'anim': 'ctrl_set', 'abc': None}
    kwargs['namespace'] = ['KatarsNml_RigProxy']
    # kwargs['evaluate'] = 'DG'
    kwargs['evaluate'] = 'parallel'
    kwargs['debug'] = False
    kwargs['frame_handle'] = 1
    kwargs['load_pref'] = False
    ndPyLibExportAnim_caller(kwargs)
# test_caller()
