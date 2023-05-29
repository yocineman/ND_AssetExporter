# coding: utf-8

import os,sys
import yaml
import shell_lib.util_exporter as util_exporter
import batch
import pprint
def back_starter_main(**kwargs):
    argsdic = kwargs
    input_path = argsdic['input_path']
    asset_name = argsdic['asset_name']
    export_type = argsdic['export_type']
    debug = argsdic['debug']

    if export_type in ['anim', 'abc', 'abc_anim']:
        argsdic['anim_item'] = argsdic['export_item']['anim']
        argsdic['abc_item'] = argsdic["export_item"]['abc']

    if 'override_shotpath' in argsdic.keys():
        override = True
    else:
        override = False

    opc = util_exporter.outputPathConf(input_path, export_type=export_type, debug=debug)
    opc.set_char(asset_name)
    opc.ver_inc()
    argsdic['publish_char_path'] = opc.publish_char_path
    if export_type == 'anim':
        argsdic['publish_ver_anim_path'] = opc.publish_ver_anim_path
        batch.animExport(**argsdic)
        if override == True:  # animの出力のみ
            return
        anim_files = os.listdir(opc.publish_ver_anim_path)
        if len(anim_files)==0:
            opc.remove_dir()
            print('outputfile not found')
            return
        output_set_list = []
        for anim_file in anim_files:
            file_namespace = anim_file.replace('anim_', '').replace('.ma', '')
            ma_file = file_namespace + '.ma'
            argsdic['file_namespace'] = file_namespace
            argsdic['anim_ver_path'] =  opc.publish_ver_anim_path + '/' + anim_file
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' + ma_file
            batch.animAttach(**argsdic)
            output_set_list.append([ma_file, anim_file])
        opc.copy_ver2current()
        for output_set in output_set_list:
            ma_file = output_set[0]
            anim_file = output_set[1]
            if anim_file[:5] != 'anim_':continue
            if anim_file[-3:] != '.ma':continue
            file_namespace = anim_file.replace('anim_', '').replace('.ma', '')
            argsdic['file_namespace'] = file_namespace
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' +  ma_file
            argsdic['ma_current_path'] =  opc.publish_current_path + '/' + ma_file
            argsdic['anim_ver_path'] = opc.publish_ver_anim_path + '/' + anim_file
            argsdic['anim_current_path'] = opc.publish_current_anim_path + '/' + anim_file
            batch.animReplace(**argsdic)

    elif export_type == 'abc':
        argsdic['publish_ver_abc_path'] = opc.publish_ver_abc_path
        batch.abcExport(**argsdic)
        abc_files = os.listdir(opc.publish_ver_abc_path)
        if len(abc_files) == 0:
            opc.remove_dir()
            print('outputfile not found')
            return
        output_set_list = []
        for abc_file in abc_files:
            file_namespace = abc_file.replace('.abc', '').replace('abc_', '')
            ma_file = file_namespace + '.ma'
            argsdic['file_namespace'] = file_namespace
            argsdic['ma_ver_path'] = opc.publish_ver_path+"/"+ ma_file
            argsdic['abc_ver_path'] = opc.publish_ver_abc_path+"/"+ abc_file
            batch.abcAttach(**argsdic)
            output_set_list.append([ma_file, abc_file])
        opc.copy_ver2current()
        for output_set in output_set_list:
            ma_file = output_set[0]
            abc_file = output_set[1]
            # if abc_file[:4] != 'abc_':continue
            if abc_file[-4:] != '.abc':continue
            file_namespace = abc_file.replace('abc_', '').replace('.abc', '')
            argsdic['file_namespace'] = file_namespace
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' +  ma_file
            argsdic['ma_current_path'] =  opc.publish_current_path + '/' + ma_file
            argsdic['abc_ver_path'] = opc.publish_ver_abc_path + '/' + abc_file
            argsdic['abc_current_path'] = opc.publish_current_abc_path + '/' + abc_file
            batch.abcReplace(**argsdic)

    elif export_type == 'abc_anim':
        argsdic['publish_ver_anim_path'] = opc.publish_ver_anim_path
        argsdic['publish_ver_abc_path'] = opc.publish_ver_abc_path
        batch.animExport(**argsdic)
        batch.abcExport(**argsdic)
        anim_files = os.listdir(opc.publish_ver_anim_path)
        abc_files = os.listdir(opc.publish_ver_abc_path)
        output_set_list = []
        for anim_file in anim_files:  # animFileに合わせる
            file_namespace = anim_file.replace('anim_', '').replace('.ma', '')
            # abc_file = 'abc_' + file_namespace + '.abc'
            abc_file = file_namespace + '.abc'
            ma_file = file_namespace + '.ma'
            argsdic['anim_ver_path'] = opc.publish_ver_anim_path + '/' + anim_file
            argsdic['abc_ver_path'] = opc.publish_ver_abc_path + '/' + abc_file
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' +  file_namespace + '.ma'
            argsdic['file_namespace'] = file_namespace
            batch.abcAnimAttach(**argsdic)
            output_set_list.append([ma_file, abc_file, anim_file])
        opc.copy_ver2current()

        for output_set in output_set_list:
            ma_file = output_set[0]
            abc_file = output_set[1]
            anim_file = output_set[2]
            file_namespace = ma_file.replace('.ma', '')
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' +  ma_file
            argsdic['ma_current_path'] =  opc.publish_current_path + '/' + ma_file
            argsdic['abc_ver_path'] = opc.publish_ver_abc_path + '/' + abc_file
            argsdic['abc_current_path'] = opc.publish_current_abc_path + '/' + abc_file
            argsdic['anim_ver_path'] = opc.publish_ver_anim_path + '/' + anim_file
            argsdic['anim_current_path'] = opc.publish_current_anim_path + '/' + anim_file
            batch.abcAnimReplace(**argsdic)

    elif export_type == 'camera':
        argsdic['publish_ver_path'] = opc.publish_ver_path
        print(opc.shot)
        try:
            oFilename = opc.pro_name+ '_'+ opc.roll+ '_' + opc.sequence +'_'+  opc.shot + '_cam'
        except:
            oFilename = opc.pro_name+ '_'+ opc.sequence +'_'+  opc.shot + '_cam'
        argsdic['ext_type'] = 'all'
        argsdic['ma_cam_path'] =  '{}/{}.ma'.format(opc.publish_ver_path, oFilename)
        argsdic['abc_cam_path'] = '{}/{}.abc'.format(opc.publish_ver_path, oFilename) #フルパスとファイル名
        argsdic['fbx_cam_path'] = '{}/{}.fbx'.format(opc.publish_ver_path, oFilename) #フルパスとファイル名
        batch.camExport(**argsdic)
        opc.copy_ver2current()

    elif export_type == 'ass':
        #  Export
        argsdic['publish_ver_ass_path'] = opc.publish_ver_ass_path
        batch.assExport(**argsdic)
        ass_files = os.listdir(opc.publish_ver_ass_path)
        if len(ass_files) == 0:
            opc.remove_dir()
            print('outputfile not found')
            return

        # Attach
        ass_frame_dict = {}
        ma_set_list = []
        for ass_file in ass_files:
            ass_name = ass_file.split('.')[0]
            frame_num = ass_file.split('.')[1]
            if ass_name not in ass_frame_dict.keys():
                ass_frame_dict[ass_name] = [frame_num]
            else:
                ass_frame_dict[ass_name].append(frame_num)

        for ass_name, key_list in ass_frame_dict.items():
            key_list.sort()
            s_f = key_list[0]
            e_f = key_list[-1]
            argsdic['frame_range'] =  [s_f, e_f]
            file_namespace = ass_name
            ma_file = file_namespace + '.ma'
            ass_file = file_namespace + '.{}.ass'.format(s_f)
            argsdic['file_namespace'] = file_namespace
            argsdic['ma_ver_path'] = opc.publish_ver_path+"/"+ ma_file
            argsdic['ass_ver_path'] = opc.publish_ver_ass_path+"/"+ ass_file
            batch.assAttach(**argsdic)
            ma_set_list.append([ma_file, ass_file, file_namespace])
        opc.copy_ver2current()

        for ma_set in ma_set_list:
            ma_file = ma_set[0]
            ass_file = ma_set[1]
            file_namespace = ma_set[2]
            # if ass_file[:4] != 'ass_':continue
            if ass_file[-4:] != '.ass':continue
            argsdic['file_namespace'] = file_namespace
            argsdic['ma_ver_path'] = opc.publish_ver_path + '/' +  ma_file
            argsdic['ma_current_path'] =  opc.publish_current_path + '/' + ma_file
            argsdic['ass_ver_path'] = opc.publish_ver_ass_path + '/' + ass_file
            argsdic['ass_current_path'] = opc.publish_current_ass_path + '/' + ass_file
            batch.assReplace(**argsdic)
    try:
        opc.addTimeLog()
    except Exception as e:
        print(e)

    print('Output directry: {}'.format(opc.publish_ver_path.replace('/','\\')))
    print('=================END===================')


if __name__ == '__main__':
    #  subprocessで実行するため必要
    argslist = sys.argv[:]
    argslist.pop(0) # 先頭はpyファイルなので
    # argsdic = yaml.safe_load(argslist[0])
    str_dict = ''.join(argslist)
    import pprint
    pprint.pprint(yaml.load(str_dict))
    back_starter_main(**yaml.load(str_dict))
