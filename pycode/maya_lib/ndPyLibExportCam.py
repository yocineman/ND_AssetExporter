# -*- coding: utf-8 -*-
try:
    from importlib import reload
except:
    pass

import os
import maya.cmds as cmds
import maya.mel as mel
import re

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
    cam_shapes = cmds.ls(ca=True)
    try:
        cam_shapes.remove('frontShape')
        cam_shapes.remove('perspShape')
        cam_shapes.remove('sideShape')
        cam_shapes.remove('topShape')
        cam_shapes.remove('leftShape')
        cam_shapes.remove('backShape')
        cam_shapes.remove('bottomShape')
        cam_shapes.remove('front1Shape')
        cam_shapes.remove('persp1Shape')
        cam_shapes.remove('side1Shape')
        cam_shapes.remove('top1Shape')
        cam_shapes.remove('persp2Shape')
        cam_shapes.remove('deformation_camShape')
    except ValueError:
        pass
    for camShape in cam_shapes[:]:
        if cmds.getAttr("{}.orthographic".format(camShape)):
            cam_shapes.remove(camShape)

    cams = cmds.listRelatives(cam_shapes, p=True, f=True)
    tg_cam_list = []
    if cams is None:
        return
    for i in range(len(cams)):
        tg_cam_list.append(cams[i])

    return tg_cam_list


def bake_cam(sframe, eframe, cam_scale, scene_time_warp):
    cams = search_cam()
    if cams is None:
        return
    shapeAttrs = ['fl','hfa','vfa','lsr','fs','fd','sa','coi','ncp','fcp', 'locatorScale', 'centerOfInterest']
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
            for t in range(int(sframe),int(eframe+1)):
                cmds.currentTime(t)
                warp_time = cmds.getAttr("time1.outTime", time=t)
                time_set_list.append([t, warp_time])

            cmds.setAttr("time1.enableTimewarp", 1)
            for time_set in time_set_list:
                t = time_set[0]
                warp_time = time_set[1]
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
        # try:
        #     mb_path = ma_path.replace('.ma', '.mb')
        #     cmds.file(mb_path, force=True, options='v=0', typ='mayaBinary', pr=True, es=True, f=True)
        # except:
        #     pass


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

    cams = bake_cam(sframe, eframe, kwargs['cam_scale'], kwargs['scene_timewarp'])
    if cams is None:
        return

    if cmds.objExists('cam_grp'):
        cmds.delete('cam_grp')
    cmds.group(em=True, n='cam_grp')
    bake_cams = []
    for i in range(len(cams)):
        from_cam = cams[i][1]
        to_cam = cams[i][0]
        cmds.parent(to_cam,'cam_grp')
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
        if kwargs['remain_cam'] == True:
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