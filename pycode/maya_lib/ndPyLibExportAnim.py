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
    from .on_maya.project import dw_h_env
    dw_h_env.main()


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
    cmds.file(ma, i=True, ns=ns, force=True, pmt=True)
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
        except Exception as e:
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

    if kwargs['scene_timewarp'] == True or kwargs['scene_timewarp'] == 'True':
        scene_timewarp = True
    else:
        scene_timewarp = False
        
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

    if scene_timewarp:
        cmds.setAttr("time1.enableTimewarp", 0)
    baseAnimationLayer = cmds.animLayer(q=True, r=True)
    
    if baseAnimationLayer != None:
        animLayers = cmds.ls(type='animLayer')
        for al in animLayers:
            cmds.animLayer(al, e=True, sel=False)
        cmds.bakeResults(baseAnimationLayer, t=(sframe, eframe), sb=True, ral=True, sm=True, dic=True)
    if scene_timewarp:
        cmds.setAttr("time1.enableTimewarp", 1)
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
    if scene_timewarp:
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

        cmds.setAttr("time1.enableTimewarp", 1)
        for time_set in time_set_list:
            t = time_set[0]
            warp_time = time_set[1]
            cmds.currentTime(t)
            for attr in attrs:
                try:
                    value = cmds.getAttr(attr)
                    print(t, attr, value)
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
                        # if source.split('.')[-1]!='output':
                        cmds.disconnectAttr(source, attr)
            except Exception as e:
                print(e)

        for time_list in time_value_set_list:
            frame = time_list[0]
            attr = time_list[1]
            value = time_list[2]
            cmds.currentTime(frame)
            print(frame, attr, value)
            try:
                cmds.setAttr(attr, value)
                cmds.setKeyframe(attr, v=value, t=frame)
            except Exception as e:
                print(e)
                # pass
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
    except:
        pass
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
