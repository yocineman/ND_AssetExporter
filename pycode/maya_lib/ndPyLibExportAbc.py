# -*- coding: utf-8 -*-

import os
import re

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

def getNamespace():
    namespaces = cmds.namespaceInfo(lon=True, r=True)
    namespaces.remove('UI')
    namespaces.remove('shared')
    return namespaces


def Euler_filter(obj_list):
    xyz = ['.rotateX', '.rotateY', '.rotateZ']
    for obj in obj_list:
        anim_cv = map(lambda x: cmds.connectionInfo(obj+x, sfd=True), xyz)
        anim_cv = map(lambda x: x.rstrip('.output'), anim_cv)
        try:
            anim_cv = filter(lambda x: cmds.nodeType(x) in ['animCurveTL', 'animCurveTU', 'animCurveTA', 'animCurveTT'], anim_cv)
            if len(list(anim_cv)) == 0:
                continue
            cmds.filterCurve(anim_cv, f='euler')
            print('# Euler Filter Success: '+obj+' #')
        except:
            continue


def getAllNodes(namespace, _regexArgs):
    if len(_regexArgs) == 0:
        regexArgs = ['*']

    nodes = []
    regexArgs = _regexArgs.split(',')

    for regex in regexArgs:
        objs = []
        objSets = []
        regexN = ''
        if namespace != '':
            regexN += namespace + ':'
        regexN = regexN + regex
        try:
            objs = cmds.ls(regexN, type='transform')
            # 後ろ５文字がShapeならば除外
            objs = [obj for obj in objs if not obj.endswith('Shape')]
            objSets = cmds.sets(regexN, q=True)
        except:
            continue
        if objs != None:
            if len(objs) != 0:
                nodes += objs
        if objSets != None:
            if len(objSets) != 0:
                nodes += objSets

    return nodes


def export_abc_main(**kwargs):
    print("ndPylibExportABC Start")
    print('##export_anim_main args#############')
    print('scene timewarp        : ', kwargs['manual_bake'])
    print('publish_ver_abc_path : ', kwargs['publish_ver_abc_path'])
    print('export_item           : ', kwargs['export_item'])
    print('namespace             : ', kwargs['namespace'])
    print('abc_item: ', kwargs['abc_item'])
    print('####################################')
    input_ns_list = kwargs['namespace']
    frame_range = kwargs['frame_range']
    if frame_range != False:
        sframe = frame_range[0]
        eframe = frame_range[1]
    else:
        sframe = cmds.playbackOptions(q=True, min=True)
        eframe = cmds.playbackOptions(q=True, max=True)

    sframe -= float(kwargs['frame_handle'])
    eframe += float(kwargs['frame_handle'])

    tg_ns_list = []
    scene_ns_list = getNamespace()
    for scene_ns in scene_ns_list:
        for input_ns in input_ns_list:
            match = re.match(input_ns, scene_ns)
            print(input_ns, scene_ns, match)
            if match != None:
                tg_ns_list.append(scene_ns)

    print("scene_ns_list ###")
    print(scene_ns_list)
    print("--")
    print("input_ns_list ###") 
    print(input_ns_list)
    print("--")
    print("### tg_ns_list ###")
    if len(tg_ns_list) == 0:
        print("tg_ns_list is empty. Please check the namespace input.")
    else:
        print(tg_ns_list)

    tg_nodes_dic = {}
    if 'add_attr' in kwargs.keys():
        dictAttributes = {}
        context = "/mat/"
        for eachSG in pm.ls(type="shadingEngine"):
            if eachSG.split(':')[0] not in scene_ns_list:
                continue
            members = pm.sets(eachSG,q=True,nodesOnly=False)
            if len(members)==0:
                continue
            shader = (pm.listConnections(eachSG+".aiSurfaceShader",p=False,c=False,s=True,d=False) or [""])[0]
            if shader == "":
                shader = (pm.listConnections(eachSG+".surfaceShader",p=False,c=False,s=True,d=False) or [""])[0]
            if shader == "":
                continue
            shaderName = shader.name()
            for eachMember in members:
                #SGがオブジェクトに紐付けられている場合の処理
                if type(eachMember) == pm.nodetypes.Mesh:
                    dictAttributes[eachMember]={"shader":[],"rest":[]}
                    dictAttributes[eachMember]["shader"] = [context+eachSG]*eachMember.numFaces()
                    for vtxIndex in range(eachMember.numVertices()):
                        position = pm.pointPosition(eachMember+".vtx["+str(vtxIndex)+"]",world=True).get()
                        dictAttributes[eachMember]["rest"].append( [position[0],position[1],position[2]] )
                #SGがフェースに紐付けられている場合の処理
                elif eachMember._ComponentLabel__ == "f":
                    # listComponents = pm.ls(eachMember,flatten=True)
                    shape = eachMember._node
                    if shape not in dictAttributes:
                        dictAttributes[shape]={"shader":[],"rest":[]}
                        dictAttributes[shape]["shader"]= [""]*eachMember.totalSize()
                        for vtxIndex in range(shape.numVertices()):
                            dictAttributes[shape]["rest"].append( pm.pointPosition(shape+".vtx["+str(vtxIndex)+"]",world=True) )
                    #該当するリストのインデックスにシェーダ名を書き込む
                    for index in eachMember.indices():
                        dictAttributes[shape]["shader"][index] = context+eachSG#shaderName
        restAttributeName = "rest"
        shaderAttributeName = "shop_materialpath"
        for eachShape in dictAttributes:
            #Rest Positionアトリビュートを追加
            if not pm.attributeQuery(restAttributeName+"_AbcGeomScope",node=eachShape,exists=True):
                pm.addAttr(eachShape, dataType="string", longName=restAttributeName+"_AbcGeomScope")
            pm.setAttr(eachShape+"."+restAttributeName+"_AbcGeomScope", "var")
            if not pm.attributeQuery(restAttributeName,node=eachShape,exists=True):
                pm.addAttr(eachShape,dataType="vectorArray",longName=restAttributeName)
            pm.setAttr(eachShape+"."+restAttributeName,dictAttributes[eachShape]["rest"])
            #shop_materialpathアトリビュートを追加
            if not pm.attributeQuery(shaderAttributeName+"_AbcGeomScope",node=eachShape,exists=True):
                pm.addAttr(eachShape, dataType="string", longName=shaderAttributeName+"_AbcGeomScope")
            pm.setAttr(eachShape+"."+shaderAttributeName+"_AbcGeomScope", "uni")
            if not pm.attributeQuery(shaderAttributeName,node=eachShape,exists=True):
                pm.addAttr(eachShape,dataType="stringArray",longName=shaderAttributeName)
            pm.setAttr(eachShape+"."+shaderAttributeName,dictAttributes[eachShape]["shader"])

    # euler filter

    for tg_ns in tg_ns_list:
        print(tg_ns, kwargs['abc_item'])
        print(getAllNodes(tg_ns, kwargs['abc_item']))
        all_nodes = getAllNodes(tg_ns, kwargs['abc_item'])
        Euler_filter(all_nodes)
        tg_nodes_dic[tg_ns] = all_nodes
        yeti_set = cmds.ls(tg_ns+':yetiSet')
        if len(yeti_set) != 0:
            yeti_objs = cmds.sets(tg_ns+':yetiSet', q=True)
        else:
            yeti_objs = []
        yeti_list = []
        for yeti_obj in yeti_objs:
            inyeticasch = cmds.getAttr(yeti_obj+".cacheFileName")
            outyeticasch = cmds.getAttr(yeti_obj+".outputCacheFileName")
            yeti_path = os.path.join(kwargs['publish_char_path'],'yetimem.txt')
            yeti_list.append(yeti_obj)
            yeti_list.append(inyeticasch)
            yeti_list.append(outyeticasch)
        if len(yeti_list) != 0:
            yeti_path = os.path.join(kwargs['publish_char_path'],'yetimem.txt')
            try:
                with open(yeti_path, 'w') as fp:
                    for line in yeti_list:
                        fp.write(line)
                        fp.write('\n')
            except Exception as e:
                print(e)

    if not cmds.pluginInfo('AbcExport', q=True, l=True):
        plugin_path = "C:/Program Files/Autodesk/Maya2023/bin/plug-ins"
        # os.environ["_TMP_VER"] = os.environ["_TMP_VER"]+";"+plugin_path
        cmds.loadPlugin('AbcExport')

    cache_nodes = cmds.ls(type='cacheFile')
    cmds.hide(cache_nodes)

    for tg_ns, tg_nodes in tg_nodes_dic.items():
        if len(tg_nodes) == 0:
            continue
        top_node =  tg_ns + ":" + kwargs['top_node']
        abc_file_name = tg_ns+'.abc'
        abc_file_path = kwargs['publish_ver_abc_path']+'/'+abc_file_name

        strAbc = ''
        strAbc = strAbc + '-frameRange '
        strAbc = strAbc + str(sframe) + ' '
        strAbc = strAbc + str(eframe) + ' '
        strAbc = strAbc + '-uvWrite '
        # strAbc = strAbc + '-worldSpace '
        strAbc = strAbc + '-writeVisibility '
        strAbc = strAbc + '-eulerFilter '
        strAbc = strAbc + '-dataFormat ogawa '
        strAbc = strAbc + '-step '
        strAbc = strAbc + str(kwargs['step_value']) + ' '
        strAbc = strAbc + '-root '
        # strAbc = strAbc + top_node + ' '
        for tg_node in tg_nodes:
            strAbc = strAbc  + tg_node + ' '
        strAbc = strAbc + '-file '
        strAbc = strAbc + abc_file_path
        if 'add_attr' in kwargs.keys():
            strAbc = strAbc + ' -attr ' + kwargs['add_attr']

        print('AbcExport -j {}'.format(strAbc))
        mel.eval('AbcExport -verbose -j \"{}\"'.format(strAbc))
    return


def ndPyLibExportAbc_caller(args):
    export_abc_main(**args)


if __name__ == '__main__':
    args = {
        'manual_bake': False,
        'publish_ver_abc_path': 'P:/Project/mem2/shots/roll05/s141G/c004/publish/test_charSet/001_LXMAR/v002/abc',
        'export_item': {'anim': None, 'abc': 'ABCset'},
        'namespace': ['[_A-Za-z]*LXMAR[0-9]*_RigRH'],
        'abc_item': 'ABCset',
        'input_path': 'P:/Project/mem2/shots/roll05/s141G/c004/work/test/s141Gc004_anm_v001.ma',
        'frame_range': False,
        'frame_handle': False,
        'top_node': 'root',
        'step_value': False,
        'publish_char_path': r'P:\Project\mem2\shots\roll05\s141G\c004\publish\test_charSet\001_LXMAR'
        }
    ndPyLibExportAbc_caller(args)
    