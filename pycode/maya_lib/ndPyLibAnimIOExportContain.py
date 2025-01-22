# -*- coding: utf-8 -*-

from ndPyLibAnimGetAnimNodeAndAttr import *
import maya.cmds as cmds
import os

def ndPyLibAnimIOExportContain_main(**kwargs):
    isFilterCurve = kwargs['is_filter']
    inDirPath = kwargs['publish_ver_anim_path']
    inFileName = kwargs['anim_file_name']
    pickNodes = kwargs['pick_nodes']
    pickNodesAttr = kwargs['pick_node_and_attrs']
    isCheckAnimCurve = kwargs['is_check_anim_curve']
    isCheckConstraint = kwargs['is_check_constraint']
    tg_nodes = []
    addCmd = []

    NS = ['', '_', ':', '']
    pfxSw = 3
    tmpFile = 'ndExportAnimCurveTmp.ma'

    tg_nodes = ndPyLibAnimGetAnimNodeAndAttr(pickNodes, 0, isCheckAnimCurve, isCheckConstraint)
    if len(pickNodesAttr)!=0:
        tg_nodes += ndPyLibAnimGetAnimNodeAndAttr(pickNodesAttr, 0, isCheckAnimCurve, isCheckConstraint)

    if len(tg_nodes) <= 0:
        return
    print('##PickNodes##')
    print(pickNodes)
    print('##tg_nodes##')
    print(tg_nodes)
    print("check, ", isFilterCurve)
    cmds.select(cl=True)
    for i in range(int(len(tg_nodes)/2)):
        if cmds.objExists(tg_nodes[i*2+1]):
            buf = tg_nodes[i*2+1].split(':')
            if len(buf) == 2:
                try: #retnodeをリネームしている
                    rn = cmds.rename(tg_nodes[i*2+1], buf[1])
                except:
                    rn = tg_nodes[i*2+1]
                tg_nodes[i*2+1] = rn
            cmds.select(tg_nodes[i*2+1], add=True)
    print("state1")
    if isFilterCurve:
        cmds.filterCurve()
    else:
        # print '[nd] Not use filterCurve\n'
        pass

    fileName = inFileName.split(":")[-1]
    filePathName = inDirPath + '/' + fileName
    filePathNamex = os.path.dirname(filePathName)

    if not os.path.exists(filePathNamex):
        print('##Create Dir##')
        os.makedirs(filePathNamex)

    info = {}
    for i in range(int(len(tg_nodes)/2)):
        if cmds.objExists(tg_nodes[i*2+1])==1:
            s = tg_nodes[i*2+1]
            sn = tg_nodes[i*2].split(':')[0]
            info['asset'] = sn
            info['date'] = cmds.date()
            info['tool'] = 'ND_AssetExporter'
            addInfoAttr(s, info)
    print('##Anim Export Start##')
    unknown = cmds.ls(type='unknown')
    if unknown:
        cmds.delete(unknown) 
    try:
        cmds.file(filePathName, f=True, es=True, typ='mayaAscii', ch=0, chn=0, exp=0, con=0, sh=0, )
    except Exception as e:
        print("###############Error: ", e)
        print(e)
    # cmds.file(filePathName, f=True, es=True, typ='mayaAscii', ch=0, chn=0, exp=0, con=0, sh=0, force=1)
    print('##Anim Export End##')

    for i in range(int(len(tg_nodes)/2)):
        from_node = tg_nodes[i*2+1]
        to_node = cmds.ls(tg_nodes[i*2], long=True)[0]
        ns = to_node.split(':')[-2].split('|')[-1]
        _node = ''
        for _part in to_node.split('|'):
            if ns in _part:
                _node += '|:' + _part
        cmd = 'connectAttr -f \"' + tg_nodes[i*2+1] + '.output\" \"' + _node + '\";\n'
        addCmd.append(cmd)

    try:
        readFileID = open(inDirPath+'/'+fileName, 'r')
        writeFileID = open(inDirPath+'/'+tmpFile, 'w')
        line = readFileID.readline()

        while line:
            if line == '// End of ' + fileName + '\n':
                for c in addCmd:
                    writeFileID.write(c)
                writeFileID.write('// End of '+fileName+'\n')
            else:
                writeFileID.write(line)
            line = readFileID.readline()
    except Exception as e:
        print("###############Error: ", e)
        print(e)
    finally:
        readFileID.close()
        writeFileID.close()
    org = inDirPath + '/' + fileName
    tmp = inDirPath + '/' + tmpFile

    os.remove(org)
    os.rename(tmp, org)


def addInfoAttr(node, info):
    for key in info.keys():
        try:
            cmds.getAttr(node+'.'+key)
        except:
            cmds.addAttr(node, ln=key, dt='string')
            cmds.setAttr(node+'.'+key, info[key], type='string')
