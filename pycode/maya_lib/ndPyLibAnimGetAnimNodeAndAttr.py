# -*- coding: utf-8 -*-


import maya.cmds as cmds

def ndPyLibAnimGetAnimNodeAndAttr (inForNodes, inMode, isCheckAnimCurve, isCheckConstraint):
    retNodes = []
    if inForNodes:
        retNodes = ndPyLibAnimGetAnimNodeAndAttrFunc(inForNodes, inMode, isCheckAnimCurve, isCheckConstraint)
    else:
        cmds.confirmDialog(title='Error...', message='Please select the mode that 0-3 is correct or node is zero.')
        cmds.error('[nd] Please select the mode that 0-3 is correct or node is zero.\n')
    return retNodes

def ndPyLibStrDeletePrefix(inStr):
    if cmds.referenceQuery(inr=inStr)==1:
        pfxRN = cmds.referenceQuery(rfn=inStr)
        pfx = pfxRN.replace('RN', '')
        pfxSize = len(pfx)
        inStrSize = len(inStr)
        ret = inStr[pfxSize+2:inStrSize]
    else:
        ret = inStr

    return ret

def _GetAnimNodeAndAttrFunc (inNode, inMode):
    retNodes = []
    nodes = []
    nodeAttr = []
    animCurve = ['animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU']
    count = flag = 0

    for l in animCurve:
        flag = 1
        nodes = []
        try:
            nodes = cmds.listConnections(inNode, c=True, type=l)
            if nodes is not None:
                if inMode == 0 or inMode == 2:
                    for k in range(0, len(nodes)):
                        if inMode == 0:
                            retNodes.append(nodes[k])
                        else:
                            if len(nodeAttr)>1:
                                nodeAttr = nodes[k].split('.')
                                delPfxNode = ndPyLibStrDeletePrefix(nodeAttr[0])
                                retNodes[count] = delPfxNode + '.' + nodeAttr[1]
                            else:
                                delPfxNode = ndPyLibStrDeletePrefix(nodes[k])
                                retNodes[count] = delPfxNode
                        count+=1
                elif inMode == 1 or inMode == 3:
                    for k in range(len(nodes)):
                        if flag == 1:
                            if inMode == 1:
                                retNodes[count] = nodes[k]
                            else:
                                nodeAttr = nodes[k].split('.')
                                delPfxNode = ndPyLibStrDeletePrefix(nodeAttr[0])
                                retNodes[count] = delPfxNode + '.' + nodeAttr[1]

                            flag = 0
                            count+=1
                        else:
                            flag = 1
        except:
            pass
    return retNodes

def ndPyLibAnimGetAnimNodeAndAttrFunc (inForNodes, inMode, isCheckAnimCurve, isCheckConstraint):
    retNodesAll = []
    retNodes = []

    listNoAnimCurveNode = []
    listNoAnimCurveNodeCnt = 0
    listConstraintConnectNode = []
    listConstraintConnectNodeCnt = 0

    for j in range(len(inForNodes)):
        checkNode = inForNodes[j]
        retNodes = _GetAnimNodeAndAttrFunc(checkNode, inMode)
        print(checkNode, retNodes)
        if isCheckAnimCurve and len(retNodes) <= 0:
            listNoAnimCurveNode.append(checkNode)
            listNoAnimCurveNodeCnt += 1
            try:
                cmds.setKeyframe(checkNode, breakdown=0, hierarchy='none', controlPoints=0, shape=True, f=True)
                retNodes = _GetAnimNodeAndAttrFunc(checkNode, inMode)
            except:
                objs = cmds.ls(checkNode)
                retNodes = []
                for obj in objs:
                    cmds.setKeyframe(obj, breakdown=0, hierarchy='none', controlPoints=0, shape=True, f=True)
                    retNodes.extend(_GetAnimNodeAndAttrFunc(obj, inMode))

        retNodesAll += retNodes

    return retNodesAll
