# -*- coding: utf-8 -*-
"""
abcの書き出しを行うモジュール

maya.batchで実行することを前提としている。
-------------------------------------------------
ndPyLibExportAbc_Caller
-> export_abc_mainの順で実行される
-------------------------------------------------
yetiのキャッシュファイルのパスを取得し、publish_char_pathに保存する

"""
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


def mergeAnimLayers():
    mel.eval(
        'source "C:/Program Files/Autodesk/Maya2020/scripts/others/performAnimLayerMerge.mel"'.format(
            pm.about(version=True)
        )
    )
    animLayers = cmds.ls(type="animLayer")
    if animLayers:
        try:
            mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))
        except Exception as e:
            print("Error merging animation layers: {}".format(e))
            cmds.warning("Failed to merge animation layers. Please check the output for details.")
    return



def Euler_Filter(attr_list):
    for attr in attr_list:
        try:
            if attr.rstrip('.output') == '':
                continue
            anim_cv = map(lambda x: x.rstrip('.output'), attr)
            anim_cv = filter(lambda x: cmds.nodeType(x) in [
                             'animCurveTL', 'animCurveTU', 'animCurveTA', 'animCurveTT'], anim_cv)
            anim_cv = list(anim_cv)
            if len(list(anim_cv))== 0:
                continue
            cmds.filterCurve(anim_cv, f='euler')
            print("EulerFilter Success: {}".format(attr))
        except Exception as e:
            pass

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
    """
    abcの書き出しを行うメイン関数

    Args:
    publish_ver_abc_path (str): 書き出し先のパス
    export_item (dict): 書き出し対象のアイテム
    namespace (list): 書き出し対象の名前空間リスト
    abc_item (str): 書き出し対象のabcアイテム名
    input_path (str): 入力ファイルのパス
    frame_range (tuple): フレーム範囲 (start, end)
    frame_handle (int): フレームハンドルの値
    top_node (str): トップノードの名前
    step_value (int): ステップ値
    publish_char_path (str): キャラクターのパス
    add_attr (bool): 属性を追加するかどうか
    Returns:
    None
    ------------------------------------------------
    処理は
    1. 名前空間の取得
    2. 名前空間のフィルタリング
    3. 対象ノードの取得
    4. ユーティリティ関数の実行
    5. abcの書き出し
    ------------------------------------------------
    """
    print("ndPylibExportABC Start")
    print('##export_anim_main args#############')
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

    # sframe -= float(kwargs['frame_handle'])
    # eframe += float(kwargs['frame_handle'])
    eframe = float(eframe) + float(kwargs['frame_handle'])
    sframe = float(sframe) - float(kwargs['frame_handle'])

    mergeAnimLayers()

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
        for eachSG in cmds.ls(type="shadingEngine"):
            if eachSG.split(':')[0] not in scene_ns_list:
                continue
            members = cmds.sets(eachSG,q=True,nodesOnly=False)
            if len(members)==0:
                continue
            shader = (cmds.listConnections(eachSG+".aiSurfaceShader",p=False,c=False,s=True,d=False) or [""])[0]
            if shader == "":
                shader = (cmds.listConnections(eachSG+".surfaceShader",p=False,c=False,s=True,d=False) or [""])[0]
            if shader == "":
                continue
            shaderName = shader.name()
            for eachMember in members:
                #SGがオブジェクトに紐付けられている場合の処理
                if type(eachMember) == cmds.nodetypes.Mesh:
                    dictAttributes[eachMember]={"shader":[],"rest":[]}
                    dictAttributes[eachMember]["shader"] = [context+eachSG]*eachMember.numFaces()
                    for vtxIndex in range(eachMember.numVertices()):
                        position = cmds.pointPosition(eachMember+".vtx["+str(vtxIndex)+"]",world=True).get()
                        dictAttributes[eachMember]["rest"].append( [position[0],position[1],position[2]] )
                #SGがフェースに紐付けられている場合の処理
                elif eachMember._ComponentLabel__ == "f":
                    # listComponents = cmds.ls(eachMember,flatten=True)
                    shape = eachMember._node
                    if shape not in dictAttributes:
                        dictAttributes[shape]={"shader":[],"rest":[]}
                        dictAttributes[shape]["shader"]= [""]*eachMember.totalSize()
                        for vtxIndex in range(shape.numVertices()):
                            dictAttributes[shape]["rest"].append( cmds.pointPosition(shape+".vtx["+str(vtxIndex)+"]",world=True) )
                    #該当するリストのインデックスにシェーダ名を書き込む
                    for index in eachMember.indices():
                        dictAttributes[shape]["shader"][index] = context+eachSG#shaderName
        restAttributeName = "rest"
        shaderAttributeName = "shop_materialpath"
        for eachShape in dictAttributes:
            #Rest Positionアトリビュートを追加
            if not cmds.attributeQuery(restAttributeName+"_AbcGeomScope",node=eachShape,exists=True):
                cmds.addAttr(eachShape, dataType="string", longName=restAttributeName+"_AbcGeomScope")
            cmds.setAttr(eachShape+"."+restAttributeName+"_AbcGeomScope", "var")
            if not cmds.attributeQuery(restAttributeName,node=eachShape,exists=True):
                cmds.addAttr(eachShape,dataType="vectorArray",longName=restAttributeName)
            cmds.setAttr(eachShape+"."+restAttributeName,dictAttributes[eachShape]["rest"])
            #shop_materialpathアトリビュートを追加
            if not cmds.attributeQuery(shaderAttributeName+"_AbcGeomScope",node=eachShape,exists=True):
                cmds.addAttr(eachShape, dataType="string", longName=shaderAttributeName+"_AbcGeomScope")
            cmds.setAttr(eachShape+"."+shaderAttributeName+"_AbcGeomScope", "uni")
            if not cmds.attributeQuery(shaderAttributeName,node=eachShape,exists=True):
                cmds.addAttr(eachShape,dataType="stringArray",longName=shaderAttributeName)
            cmds.setAttr(eachShape+"."+shaderAttributeName,dictAttributes[eachShape]["shader"])

    # euler filter

    for tg_ns in tg_ns_list:
        print(tg_ns, kwargs['abc_item'])
        print(getAllNodes(tg_ns, kwargs['abc_item']))
        all_nodes = getAllNodes(tg_ns, kwargs['abc_item'])
        Euler_Filter(all_nodes)
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
        # strAbc = strAbc + '-uvWrite '
        strAbc = strAbc + '-wuvs '
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
    