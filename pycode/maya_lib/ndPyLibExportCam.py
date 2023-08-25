# -*- coding: utf-8 -*-
try:
    from importlib import reload
except:
    pass

import os,sys
import maya.cmds as cmds
import maya.mel as mel
import re

def unlock_current_layer():
    try:
        anim_layer_list = cmds.ls(type='animLayer')
        for anim_layer in anim_layer_list:
            cmds.animLayer(anim_layer, e=True, lock=False)
    except:
        pass


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


def Euler_filter(obj_list):
    xyz = ['.rotateX', '.rotateY', '.rotateZ']
    for obj in obj_list:
        anim_cv = map(lambda x: cmds.connectionInfo(obj+x, sfd=True), xyz)
        anim_cv = map(lambda x: x.rstrip('.output'), anim_cv)
        try:
            anim_cv = filter(lambda x: cmds.nodeType(x) in ['animCurveTL', 'animCurveTU', 'animCurveTA', 'animCurveTT'], anim_cv)
            cmds.filterCurve(anim_cv, f='euler')
        except:
            print('# Euler FilterFailed: '+obj+' #')
            continue
        print('# Euler Filter Success: '+obj+' #')


def search_cam():
    tg_cam_list = []
    for cam_shape in cmds.ls(ca=True):
        if cmds.getAttr("{}.orthographic".format(cam_shape)):
            continue
        cam = cmds.listRelatives(cam_shape, p=True)[0]
        if cam == 'persp':
            continue
        tg_cam_list.append(cam)
    return tg_cam_list


def bake_cam(sframe, eframe, cam_scale, scene_time_warp, step_value, tg_cam_list):
    if tg_cam_list is None or tg_cam_list is 'None':
        cams = search_cam()
    else:
        cams = tg_cam_list
    if cams is None:
        return
    shapeAttrs = ['fl','hfa','vfa','lsr','fs','fd','sa','coi','ncp','fcp', 'locatorScale', 'centerOfInterest', 'rotateOrder']
    result_cams = []
    from_cam = []
    to_cam = []
    for i in range(len(cams)):
        to_cam.append(cmds.camera()[0])
        from_cam.append(cams[i])

    if scene_time_warp == True:
        for i in range(len(to_cam)):
            time_set_list = []
            time_value_set_list = []
            shape_value_set_list = []

            cmds.setAttr("time1.enableTimewarp", 1)
            _frame = sframe
            while True:
                cmds.currentTime(_frame)
                warp_time = cmds.getAttr("time1.outTime", time=_frame)
                time_set_list.append([_frame, warp_time])
                _frame += step_value
                if _frame > eframe:
                    break
            cmds.setAttr("time1.enableTimewarp", 1)
            for time_set in time_set_list:
                t = time_set[0]
                warp_time = time_set[1]
                print(t, warp_time)
                cmds.currentTime(t)
                try:
                    attrsTrans = cmds.xform(from_cam[i],q=True,ws=True,t=True)
                    attrsRot = cmds.xform(from_cam[i],q=True,ws=True,ro=True)
                    time_value_set_list.append([t, attrsTrans, attrsRot])
                    for shapeAttr in shapeAttrs:
                        shape_value_set_list.append([t, shapeAttr, cmds.getAttr(from_cam[i]+'.'+shapeAttr)])
                except Exception as e:
                    print(e)
            cmds.setAttr("time1.enableTimewarp", 0)
            for time_list in time_value_set_list:
                frame = time_list[0]
                attrsTrans = time_list[1]
                attrsRot = time_list[2]
                cmds.currentTime(frame)
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsTrans[0], at='tx')
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsTrans[1], at='ty')
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsTrans[2], at='tz')
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsRot[0], at='rx')
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsRot[1], at='ry')
                cmds.setKeyframe(to_cam[i],t=frame, v=attrsRot[2], at='rz')
            for shape_value_set in shape_value_set_list:
                shape_attr = shape_value_set[1]
                shape_value = shape_value_set[2]
                frame = shape_value_set[0]
                cmds.setKeyframe(to_cam[i],t=frame, v=shape_value, at=shape_attr)
    else:
        for t in range(int(sframe),int(eframe+1)):
            for i in range(len(to_cam)):
                cmds.currentTime(t)
                attrsTrans = cmds.xform(from_cam[i],q=True,ws=True,t=True)
                attrsRot = cmds.xform(from_cam[i],q=True,ws=True,ro=True)
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsTrans[0], at='tx')
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsTrans[1], at='ty')
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsTrans[2], at='tz')
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsRot[0], at='rx')
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsRot[1], at='ry')
                cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=attrsRot[2], at='rz')
                cmds.setAttr("{}.filmFit".format(to_cam[i]), cmds.getAttr('{}.filmFit'.format(from_cam[i])))
        for t in range(int(sframe),int(eframe+1)):
            for i in range(len(to_cam)):
                cmds.currentTime(t)
                if int(cam_scale) !=0:
                    cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=float(cam_scale), at='.cs')
                else:
                    camScale = cmds.getAttr(from_cam[i]+'.cameraScale')
                    cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=camScale, at='.cs')

                for thisAttr in shapeAttrs:
                    cmds.setKeyframe(to_cam[i],t=cmds.currentTime(q=True), v=cmds.getAttr(from_cam[i]+'.'+thisAttr), at='.'+thisAttr)


    for i in range(len(to_cam)):
        print('to_cam:', to_cam[i])
        try:
            cmds.setAttr(from_cam[i]+'.'+thisAttr, lock=False)
        except:
            pass

        cmds.setAttr(to_cam[i]+'.renderable', True)
        cmds.setAttr(to_cam[i]+'.renderable', lock=False)
        cmds.setAttr(to_cam[i]+'.rotateAxisX', cmds.getAttr(from_cam[i]+'.rotateAxisX'))
        cmds.setAttr(to_cam[i]+'.rotateAxisY', cmds.getAttr(from_cam[i]+'.rotateAxisY'))
        cmds.setAttr(to_cam[i]+'.rotateAxisZ', cmds.getAttr(from_cam[i]+'.rotateAxisZ'))

        for thisAttr in shapeAttrs:
            cmds.setAttr(to_cam[i]+'.'+thisAttr,lock=True)

        cmds.setAttr(to_cam[i]+'.cs',lock=True)
        cmds.setAttr(to_cam[i]+'.translate',lock=True)
        cmds.setAttr(to_cam[i]+'.rotate',lock=True)
        cmds.setAttr(to_cam[i]+'.scale',lock=True)
        cmds.setAttr(to_cam[i]+'.ro',lock=True)

        result_cams.append([to_cam[i], from_cam[i]])

        mel.eval('setAttr '+to_cam[i]+'.bestFitClippingPlanes true')
    Euler_filter(to_cam)

    return result_cams


def get_unload_ns_dic():
    unLoaded_ref_dic = {}
    refList = cmds.ls(type='reference')
    for ref in refList:
        if ref == 'sharedReferenceNode':
            continue
        try:
            if cmds.referenceQuery(ref, isLoaded=True):
                pass
            else:
                ref_path = cmds.referenceQuery(ref, filename=True)
                ref_ns = cmds.file(ref_path, q=True, ns=True)
                unLoaded_ref_dic[ref_ns] = ref
        except Exception as e:
            print(e)
    return unLoaded_ref_dic


def get_tg_ns_list(scene_ns_list, input_ns_list):
    tg_ns_list = []
    for scene_ns in scene_ns_list:
        for input_ns in input_ns_list:
            match = re.match(input_ns+'$', scene_ns)
            if match != None:
                tg_ns_list.append(scene_ns)
    return tg_ns_list


def export_ma(ma_path):
    if not os.path.exists(os.path.dirname(ma_path)):
        os.makedirs(os.path.dirname(ma_path))
    try:
        cmds.file(ma_path, force=True, options='v=0', typ='mayaAscii', pr=True, es=True, f=True)
    except Exception as e:
        print(e)


def export_fbx(fbx_path):
    if not os.path.exists(os.path.dirname(fbx_path)):
        os.makedirs(os.path.dirname(fbx_path))
    if cmds.pluginInfo('fbxmaya', q=True, l=True) == 0:
        cmds.loadPlugin('fbxmaya')
    cmds.file(fbx_path, force=True, options='v=0', typ='FBX export', pr=True, es=True, f=True)


def export_abc(abc_path, sframe, eframe):
    if not os.path.exists(os.path.dirname(abc_path)):
        os.makedirs(os.path.dirname(abc_path))
    if cmds.pluginInfo('AbcExport', q=True, l=True) == 0:
        cmds.loadPlugin('AbcExport')
    cmds.evaluationManager(mode='off')
    strAbc = ''
    strAbc = strAbc+'-frameRange '+str(sframe)+' '+str(eframe)+' '
    strAbc = strAbc+'-uvWrite '
    strAbc = strAbc+'-worldSpace '
    strAbc = strAbc+'-eulerFilter '
    strAbc = strAbc+'-dataFormat ogawa '
    strAbc = strAbc+ '-root cam_grp '
    strAbc = strAbc+ '-file '+ abc_path
    print ('AbcExport -j ' + strAbc)
    mel.eval('AbcExport -verbose -j ' + '"' + strAbc + '"')
    # cmds.file(kwargs['ma_cam_path'], force=True, options='v=0', typ='mayaAscii', pr=True, es=True)



def export_cam_main(kwargs):
    if kwargs['project'].lower() == 'd_wh':
        set_dw_h_env()
    else:
        set_env()
    # シーンのオープン
    if not cmds.file(q=True, exists=True):
        cmds.file(kwargs['input_path'], o=True, f=True)
    unlock_current_layer()
    top_nodes = cmds.ls(assemblies=True)
    batch_mode = cmds.about(batch=True)
    if 'ext_type' not in kwargs.keys():
        ext_type = 'all'
    else:
        ext_type = kwargs['ext_type']

    if batch_mode:
        cache_nodes = cmds.ls(type='cacheFile')
        hidden_objs = []
        hidden_objs.extend(cmds.hide(top_nodes, rh=True))
        hidden_objs.extend(cmds.hide(cache_nodes, rh=True))
        ignore_attrs = []
        if hidden_objs is not None:
            for obj in hidden_objs:
                ignore_attrs.append('{}.visibility'.format(obj.lstrip('|')))
        unload_ns_dic = get_unload_ns_dic()
        tg_ns_list = get_tg_ns_list(unload_ns_dic.keys(), ['camera[a-zA-Z0-9]*'])
        for tg_ns in tg_ns_list:
            ref = unload_ns_dic[tg_ns]
            cmds.file(lr=ref)
        if hidden_objs is not None:
            for obj in hidden_objs:
                ignore_attrs.append('{}Shape.visibility'.format(obj.lstrip('|')))
                ignore_attrs.append('{}.visibility'.format(obj.lstrip('|')))

    if kwargs['frame_range'] != False and kwargs['frame_range']!=None:
        sframe = float(kwargs['frame_range'].split(',')[0])
        eframe = float(kwargs['frame_range'].split(',')[1])
    else:
        sframe = cmds.playbackOptions(q=True, min=True)
        eframe = cmds.playbackOptions(q=True, max=True)
    sframe -= float(kwargs['frame_handle'])
    eframe += float(kwargs['frame_handle'])

    cams = bake_cam(sframe, eframe, kwargs['cam_scale'], kwargs['scene_timewarp'], kwargs['step_value'], kwargs['tg_cam_list'])
    if cams is None:
        return

    cam_grp = cmds.group(em=True, n='cam_grp')
    bake_cams = []
    for i in range(len(cams)):
        from_cam = cams[i][1]
        to_cam = cams[i][0]
        cmds.parent(to_cam,cam_grp)
        cmds.rename(to_cam, from_cam.split("|")[-1])
        bake_cams.append(to_cam)
    try:
        publish_ver_path = kwargs['publish_ver_path']
        if not os.path.exists(publish_ver_path):
            os.makedirs(publish_ver_path)
        sceneConfpath = os.path.join(publish_ver_path, '..', 'sceneConf.txt')
        with open(sceneConfpath, 'w') as f:
            f.write(str(sframe)+'\n')
            f.write(str(eframe)+'\n')
    except:
        pass
    cmds.select('cam_grp')
    if ext_type == 'ma' or ext_type == 'all':
        ma_cam_path = kwargs['ma_cam_path']
        export_ma(ma_cam_path)
    if ext_type == 'fbx' or ext_type == 'all':
        fbx_cam_path = kwargs['fbx_cam_path']
        export_fbx(fbx_cam_path)
    if ext_type == 'abc' or ext_type == 'all':
        abc_cam_path = kwargs['abc_cam_path']
        export_abc(abc_cam_path, sframe, eframe)

    if 'remain_cam' in kwargs.keys():
        if kwargs['remain_cam'] == False:
            for i in range(len(bake_cams)):
                cmds.delete(bake_cams[i])

    if batch_mode:
        for obj in hidden_objs:
            try:
                dst_obj = '{}.visibility'.format(obj.split('|')[-1])
                src_obj = cmds.listConnections(dst_obj, p=True)[0]
                cmds.disconnectAttr(src_obj, dst_obj)
            except Exception as e:
                print(e)
        cmds.showHidden(hidden_objs)

def ndPylibExportCam_caller(**kwargs):
    export_cam_main(kwargs)