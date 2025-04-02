#coding:utf-8
import maya.cmds as cmds

def manual_bake_remover_main():
    # sceneTimewarpはOn
    cmds.setAttr('time1.enableTimewarp', 1)
    # select All
    top_nodes = cmds.ls(assemblies=True)
    tg_nodes = cmds.ls('*:*_ctrl')
    camera_nodes = ['allRoot01', 'allRoot02', 'cam_GG', 'cameraGEMINI4K:cameraGEMINI4K_allOffset_GP', 'cameraGEMINI4K:cameraGEMINI4K_trans', 'cameraGEMINI4K:cameraGEMINI4K_rot', 'cameraGEMINI4K:cameraGEMINI4K_rendcam']
    tg_nodes = tg_nodes + camera_nodes
    _layer = cmds.animLayer("AnimLayer1")
    cmds.select(tg_nodes)
    cmds.animLayer(_layer, e=True, aso=True)
    # return
    start = cmds.playbackOptions(q=1,min=1)
    end = cmds.playbackOptions(q=1,max=1)
    cmds.animLayer(_layer, e=True, sel=True)
    cmds.animLayer(fur=True)
    # cmds.select(tg_nodes)
    # cmds.bakeResults(_layer, hi=True, t=(start, end), removeBakedAnimFromLayer=True, sm=True)
    # return
    cmds.bakeResults(tg_nodes, hi=True, t=(start, end), preserveOutsideKeys=True, disableImplicitControl=True, removeBakedAnimFromLayer=True, sm=True, shape=True, oversamplingRate=1.0)
    # return
    cmds.setAttr('time1.enableTimewarp', 0)
    cmds.delete('AnimLayer1')
    cmds.delete('timewarp')


if __name__ == '__main__':
    manual_bake_remover_main()