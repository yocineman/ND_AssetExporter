# -*- coding: utf-8 -*-
from shell_lib import util_exporter
import threading
import subprocess
import json
import datetime
import os
import sys
import time

import yaml

try:
    from importlib import reload
except:
    pass
# ------------------------------
__version__ = '9.2.0'
__author__ = 'Kei Ueda'
# ------------------------------
EXPORTER_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))).replace('\\', '/')
# ------------------------------


try:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import QUiLoader
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import QUiLoader
# ------------------------------------


try:
    import ND_Submitter.env as util_env
except Exception as e:
    NoDeadlineMode = True
else:
    NoDeadlineMode = False

PYPATH = 'Y:\\tool\\MISC\\Python2710_amd64_vs2010\\python.exe'

# get username
USERNAME = os.environ.get('USERNAME')
if USERNAME is None:
    USERNAME = 'deadlineuser'

LOGDIR = 'Y:\\users\\'+'deadlineuser'+'\\DCC_log\\ND_AssetExporter'

PRIORITY = 50
GROUP = '16gb'

onpath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
os.chdir(onpath)


class GUI(QMainWindow):

    WINDOW = 'ND_AssetExporter'

    def __init__(self, parent=None, qApp=None):
        #  GUI
        super(self.__class__, self).__init__(parent)
        self.debug = False
        self.ui_path = '.\\gui\\exporter_gui.ui'
        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)
        self.setGeometry(500, 200, 1000, 800)
        self.setWindowTitle('%s %s' % (self.WINDOW, __version__))

        self.input_path = ''
        self.log_txt = ''

        # Shotgrid
        self.asset_fields = [
            'code', 'sg_namespace', 'sg_export_type',
            'sg_top_node', 'sg_abc_export_list',
            'sg_anim_export_list', 'sg_asset_path',
            'sequences']
        self.shot_fields = ['code', 'assets']
        self.base_fields = [
            'code', 'assets',
            'sg_namespace', 'sg_export_type',
            'sg_top_node', 'sg_abc_export_list',
            'sg_anim_export_list', 'sg_asset_path',
            'sequences']

        # table
        self.headers_item = [
            'Asset name', 'Name space',
            'Export Type', 'Export Item',
            'Top Node', 'Asset Path']
        self.convert_dic = {
            'Asset name': 'code',
            'Name space': 'sg_namespace',
            'Export Type': 'sg_export_type',
            'Top Node': 'sg_top_node',
            'Asset Path': 'sg_asset_path'}

        self.headers = ['']
        self.headers.extend(self.headers_item)

        # table data
        self.tabledata = []
        self.check_row = []
        self.executed_row = []

        #  Deadline
        self.priority = PRIORITY
        self.group = GROUP

        maya_version_list = ['2023', '2022', '2020', '2019', '2018', '2017', '2016', '2015']
        for maya_version in maya_version_list:
            self.ui.maya_version_comboBox.addItem(maya_version)

        self.selected_item = None

        self.ui.dd_area.installEventFilter(self)

        # Connect UI
        self.ui.main_table.clicked.connect(self.main_table_clicked)
        self.ui.main_table.doubleClicked.connect(self.main_table_doubleClicked)
        self.ui.cam_scale_override_chk.stateChanged.connect(
            self.cam_scale_override_chk_stateChange)
        self.ui.frame_step_override_chk.stateChanged.connect(
            self.frame_step_override_chk_stateChange)
        self.ui.custom_frame_range_chk.clicked.connect(
            self.custom_frame_range_chk)
        self.ui.frame_handle_chk.clicked.connect(self.frame_handle_chk_clicked)
        self.ui.open_log_button.clicked.connect(self.open_log_button_clicked)
        self.ui.current_refresh_button.clicked.connect(
            self.current_refresh_button_clicked)
        self.ui.open_publish_dir_button.clicked.connect(
            self.open_publish_dir_button_clicked)
        self.ui.help_button.clicked.connect(self.help_button_clicked)
        self.ui.restore_last_file_button.clicked.connect(self.load_user_info)
        self.ui.check_selected_btn.clicked.connect(
            self.check_selected_btn_clicked)
        self.ui.uncheck_selected_btn.clicked.connect(
            self.uncheck_selected_btn_clicked)
        self.ui.allcheck_btn.clicked.connect(self.allcheck_btn_clicked)
        self.ui.alluncheck_btn.clicked.connect(self.alluncheck_btn_clicked)
        self.ui.export_local_btn.clicked.connect(self.export_local_btn_clicked)
        self.ui.export_submit_btn.clicked.connect(
            self.export_submit_btn_clicked)
        self.ui.maya_version_chk.stateChanged.connect(
            self.maya_version_check_stateChange)
        self.ui.evaluate_chk.stateChanged.connect(
            self.evaluate_chk_stateChange)
        self.ui.log_list_btn.clicked.connect(self.log_list_btn_clicked)
        self.ui.log_return_btn.clicked.connect(self.log_return_btn_clicked)
        self.ui.help_listup_button.clicked.connect(self.help_listup_button_clicked)

    def camscale_override_chk_stateChange(self):
        state = self.ui.frame_step_override_chk.isChecked()
        self.ui.frame_step_value_line.setEnabled(state)

    def frame_step_override_chk_stateChange(self):
        state = self.ui.frame_step_override_chk.isChecked()
        self.ui.frame_step_value_line.setEnabled(state)

    def check_selected_btn_clicked(self):
        for selected_row in self.ui.main_table.selectedIndexes():
            self.check_row.append(selected_row.row())
        self.check_row = list(set(self.check_row))
        model = util_exporter.ExporterTableModel(
            self.tabledata, self.headers,
            self.check_row, self.executed_row)
        self.ui.main_table.setModel(model)

    def uncheck_selected_btn_clicked(self):
        selected_index = []
        for selected_row in self.ui.main_table.selectedIndexes():
            selected_index.append(selected_row.row())
        selected_index = list(set(selected_index))
        for _index in selected_index:
            try:
                self.check_row.remove(_index)
            except:
                pass
        model = util_exporter.ExporterTableModel(
            self.tabledata, self.headers,
            self.check_row)
        self.ui.main_table.setModel(model)

    def allcheck_btn_clicked(self):
        self.check_row = list(range(len(self.tabledata)))
        model = util_exporter.ExporterTableModel(
            self.tabledata, self.headers,
            self.check_row, self.executed_row)
        self.ui.main_table.setModel(model)

    def alluncheck_btn_clicked(self):
        self.check_row = []
        model = util_exporter.ExporterTableModel(
            self.tabledata, self.headers,
            self.check_row, self.executed_row)
        self.ui.main_table.setModel(model)

    def frame_handle_chk_clicked(self):
        self.ui.frame_handle_value.setEnabled(
            self.ui.frame_handle_chk.isChecked())

    def custom_frame_range_chk(self):
        state = self.ui.custom_frame_range_chk.isChecked()
        self.ui.sFrame.setEnabled(state)
        self.ui.eFrame.setEnabled(state)

    def cam_scale_override_chk_stateChange(self):
        currentState = self.ui.camscale_override_chk.isChecked()
        self.ui.overrideValue_LineEdit.setEnabled(currentState)

    def export_local_btn_clicked(self):
        self.export_main(mode='Local')

    def export_submit_btn_clicked(self):
        self.export_main(mode='Submit')

    def open_log_button_clicked(self):
        sakura = r'C:\Program Files (x86)\sakura\sakura.exe'
        subprocess.Popen([sakura, self.last_log_path])

    def maya_version_check_stateChange(self):
        state = self.ui.maya_version_chk.isChecked()
        self.ui.maya_version_comboBox.setEnabled(state)

    def contextMenu(self, point):
        print(point)

    def eventFilter(self, object, event):
        if event.type() == QEvent.DragEnter:
            event.acceptProposedAction()
        if event.type() == QEvent.Drop:
            mimedata = event.mimeData()
            urldata = mimedata.urls()
            self.drop_func(urldata)
        return True

    def main_table_clicked(self):
        if self.selected_item != None:
            self.ui.main_table.closePersistentEditor(self.selected_item)
            self.selected_item = None

    def main_table_doubleClicked(self):
        clicked_row = self.ui.main_table.selectedIndexes()[0].row()
        check_rows = self.check_row
        if clicked_row in check_rows[:]:
            check_rows.remove(clicked_row)
        else:
            check_rows.append(clicked_row)
        self.check_row = list(set(check_rows))
        model = util_exporter.ExporterTableModel(
            self.tabledata, self.headers, self.check_row, self.executed_row)
        self.ui.main_table.setModel(model)

    def main_table_rclicked(self):
        selected_item = self.ui.main_table.selectedIndexes()
        if selected_item != None:
            _row = self.selected_item.row()
            _column = self.selected_item.column()
            newitem = self.selected_item.data()
        self.ui.main_table.openPersistentEditor(self.selected_item)

    def current_refresh_button_clicked(self):
        from shell_lib import copy_main, util_exporter
        opc = util_exporter.outputPathConf(self.input_path)
        shot_path = opc.shot_path
        if self.ui.test_debug.isChecked():
            current_path = os.path.join(shot_path, 'publish', 'test_charSet')
        else:
            current_path = os.path.join(shot_path, 'publish', 'charSet')
        copy_main.copy_main(current_path)

    def open_publish_dir_button_clicked(self):
        opc = util_exporter.outputPathConf(self.input_path)
        shot_path = opc.shot_path
        publish_path = os.path.join(shot_path, 'publish')
        subprocess.call('explorer {}'.format(publish_path.replace('/', '\\')))

    def help_button_clicked(self):
        import webbrowser
        url = ('https://otakendesigncojp.sharepoint.com/sites/RigDevelopment/_layouts/15/Doc.aspx?sourcedoc={9ec34422-5bff-42ef-8c06-da416db63df4}&action=edit&wd=target%28StandAlone.one%7Cfd7e5d89-f2fb-4f4f-8357-66b56ecea707%2FND_AssetExporter%7Cbe67cba1-eb34-4cfd-a8fc-c795a4f2bfbb%2F%29&wdorigin=703')
        webbrowser.open_new_tab(url)

    def evaluate_chk_stateChange(self):
        _state = self.ui.evaluate_chk.isChecked()
        self.ui.evaluate_combo.setEnabled(_state)

    def log_list_btn_clicked(self):
        self.log_table = []
        self.log_model = util_exporter.LogTableModel(self.log_table, LOGDIR)
        self.ui.log_table.setModel(self.log_model)
        self.ui.stack_area.setCurrentIndex(2)

    def log_return_btn_clicked(self):
        self.ui.stack_area.setCurrentIndex(0)

    def drop_func(self, urldata):
        # table data初期化
        self.check_row = []
        self.executed_row = []
        self.tabledata = []

        if type(urldata) == list:
            self.input_path = urldata[0].toString().replace('file:///', '')
        else:
            self.input_path = urldata

        self.ui.path_line.setText(self.input_path)
        self.ui.stack_area.setCurrentIndex(0)

        #  Shotgrid
        ProjectInfoClass = util_exporter.ProjectInfo(self.input_path)

        #  Shotgrid情報をUIに反映
        self.ui.shot_line.setText(ProjectInfoClass.shot)
        self.ui.cut_line.setText(ProjectInfoClass.sequence)
        self.project = ProjectInfoClass.project_name
        self.ui.pro_line.setText(self.project)

        #  Shotgridからアセット情報を取得
        SGBaseClass = util_exporter.SGProjectClass(
            self.project, self.base_fields, ProjectInfoClass)
        target_asset_list = SGBaseClass.get_target_asset_list()
        all_asset_dics = SGBaseClass.get_all_asset_dic()

        # tabledata作成
        target_asset_dics = []
        for target_asset_name in target_asset_list:
            target_asset_dics.append(
                all_asset_dics[target_asset_name['name']])
        # ショットのアセット情報が存在しない場合sequencesを見に行く
        if len(target_asset_list) == 0:  
            seq_list = SGBaseClass.get_keying_list(
                'Asset', 'sequences', 'sequence')
            for seq in seq_list:
                target_asset_list.append(seq['code'])
        is_cam_rig_export = ProjectInfoClass.get_camera_rig_info()
        self.tabledata = util_exporter.tabledata_builder(
            self.headers_item, self.convert_dic, target_asset_dics)
        self.tabledata = util_exporter.add_camera_row(
            self.headers_item, self.tabledata, is_cam_rig_export)

        model = util_exporter.ExporterTableModel(self.tabledata, self.headers)
        self.ui.main_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.main_table.customContextMenuRequested.connect(self.main_table_rclicked)
        self.ui.main_table.setModel(model)
        self.ui.main_table.setColumnWidth(0, 25)

        self.ui.export_local_btn.setEnabled(True)
        self.ui.export_submit_btn.setEnabled(True)
        self.output_user_info()

        def _setComboBoxList(qtcombobox, itemlist):
            qtcombobox.clear()
            qtcombobox.addItems(itemlist)

        def _setComboBoxValue(qtcombobox, value, subvalue=None):
            combo_index = qtcombobox.findText(value)
            if combo_index == -1:
                combo_index = qtcombobox.findText(value.lower())
                if combo_index == -1:
                    if subvalue != None:
                        combo_index = qtcombobox.findText(subvalue)
            qtcombobox.setCurrentIndex(combo_index)

        if NoDeadlineMode is False:
            groups = util_env.deadline_group
            pools = util_env.deadline_pool
            if type(groups) is str:
                groups = []
            if type(pools) is str:
                pools = []
            groups.sort()
            pools.sort()
            _setComboBoxList(self.ui.grouplist, groups)
            # _setComboBoxValue(self.ui.grouplist, 'mem032')
            # if util_exporter.is_arnold(self.project) is True:
            _setComboBoxValue(self.ui.grouplist, 'mem064')
            _setComboBoxList(self.ui.poollist, pools)
            _setComboBoxValue(self.ui.poollist, self.project, 'normal')
        elif NoDeadlineMode is True:
            self.ui.export_submit_btn.setDisabled(True)
            self.ui.export_submit_btn.setHidden(True)
        return True

    def export_main(self, mode):
        self.ui.stack_area.setCurrentIndex(1)
        self.ui.repaint()

        # Submit用
        file_number = 1
        jobfiles_list = []

        for table_row in range(len(self.tabledata)):
            if table_row in self.executed_row:
                continue
            if table_row not in self.check_row:
                continue

            row_items = self.tabledata[table_row]
            self.asset_name = row_items[1]
            self.namespace = row_items[2]
            self.export_type = row_items[3]
            self.export_item = row_items[4]
            self.top_node = row_items[5]
            self.asset_path = row_items[6].replace('\\', '/')

            argsdic = self.get_argsdic()

            if '{Empty!}' in argsdic.values():
                continue

            #  LocalExport
            if mode == 'Local':
                #  集計ログ用
                log_name = 'log_' + USERNAME + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') +self.asset_name + '.txt'
                log_path = LOGDIR + '\\' + log_name
                current_dir = EXPORTER_PATH + '/pycode'
                if not os.path.exists(LOGDIR):
                    os.makedirs(LOGDIR)
                self.ui.stack_area.setCurrentIndex(1)
                # スレッドで実行
                thread_args = {}
                thread_args['argsdic'] = argsdic
                thread_args['log_path'] = log_path
                thread_args['current_dir'] = current_dir
                argsdic['log_path'] = log_path.replace('\\', '/')
                export_thread = threading.Thread(
                    target=thread_main, kwargs=thread_args)
                export_thread.start()
                count = 0
                timer = 0
                dt_now = datetime.datetime.now()
                print(dt_now)
                self.log_txt = self.log_txt + \
                    '{} ; start time {}\n'.format(self.asset_name, dt_now)
                while True:
                    if len(threading.enumerate()) == 1:
                        break
                    time.sleep(0.1)
                    timer = timer+0.1
                    if timer > 4:
                        count = count+1
                        timer = 0
                        if count == 10:
                            count = 0
                        self.ui.trace_area.setPlainText(
                            '{}now working{}'.format(self.log_txt, '--'*timer+'\n'))
                        self.ui.repaint()
                    qApp.processEvents()
                #  GUI用ログ出力
                self.last_log_path = log_path
                self.ui.open_log_button.setEnabled(True)
            #  Submit
            elif mode == 'Submit':
                DLclass = util_exporter.DeadlineMod(**argsdic)
                jobfiles_list.append(DLclass.make_submit_files(file_number))
                file_number += 1
            # GUIにチェックを付ける
            self.executed_row.append(table_row)

        #  Submitは最後にまとめて実行する
        if mode == 'Submit':
            util_exporter.submit_to_deadlineJobs(jobfiles_list)

        # エクスポート終了後GUIを更新
        self.ui.stack_area.setCurrentIndex(0)
        self.executed_row = list(set(self.executed_row))
        util_exporter.ExporterTableModel(self.tabledata, self.headers, self.check_row, self.executed_row)
        print('===============Export End==================')

    def get_argsdic(self):
        if self.ui.cam_scale_override_chk.isChecked():
            cam_scale = float(self.ui.cam_scale_override_velue_line.text())
        else:
            cam_scale = False

        if self.ui.frame_handle_chk.isChecked():
            frame_handle = float(self.ui.frame_handle_value.text())
        else:
            frame_handle = False

        if self.ui.custom_frame_range_chk.isChecked():
            frame_range = (self.ui.sFrame.text()) + '-' + (self.ui.eFrame.text())
        else:
            frame_range = False

        if self.ui.frame_step_override_chk.isChecked():
            frame_step_override = float(self.ui.frame_step_value_line.text())
        else:
            frame_step_override = 1.0

        if self.ui.maya_version_chk.isChecked():
            maya_version = self.ui.maya_version_comboBox.currentText()
        else:
            maya_version = False

        if self.ui.evaluate_chk.isChecked():
            evaluate = self.ui.evaluate_combo.currentText()
        else:
            evaluate = False
        if self.ui.exe_chk.isChecked():
            is_exe = True
        else:
            is_exe = False

        argsdic = {
            "asset_name": self.asset_name,
            "namespace": [self.namespace],  # 複数可
            "export_item": yaml.safe_load(
                self.export_item.replace("|", "vertical_bar")
            ),
            "top_node": self.top_node,
            "asset_path": self.asset_path,
            "debug": self.ui.debug_chk.isChecked(),
            "step_value": frame_step_override,
            "export_type": self.export_type,
            "project": self.project,
            "frame_range": frame_range,
            "frame_handle": frame_handle,
            "cam_scale": cam_scale,
            "input_path": str(self.input_path),
            "shot": str(self.ui.shot_line.text()),
            "sequence": str(self.ui.cut_line.text()),
            "manual_bake": self.ui.manual_bake_chk.isChecked(),
            "evaluate": str(evaluate),
            "priority": str(self.ui.priority.text()),
            "pool": str(self.ui.poollist.currentText()),
            "group": str(self.ui.grouplist.currentText()),
            "load_pref": self.ui.force_load_preference_chk.isChecked(),
            "maya_version": maya_version,
            "log_shape": self.ui.log_shape_chk.isChecked(),
            "tg_cam_list": None,
            "is_exe": is_exe,
        }
        return argsdic

    def load_user_info(self):
        filename = 'user_info.py'
        output_dir = 'Y:\\users\\'+USERNAME+'\\DCC_log\\ND_AssetExporter'
        output_file = output_dir + '\\' + filename
        if not os.path.exists(output_dir):
            return
        if os.path.exists(output_file):
            sys.path.append(output_dir)
            import user_info
            print(user_info.path)
            self.drop_func(user_info.path)

    def output_user_info(self):
        filename = 'user_info.py'
        output_dir = 'Y:\\users\\'+USERNAME+'\\DCC_log\\ND_AssetExporter'
        output_file = output_dir + '\\' + filename
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_file, mode='w') as f:
            f.write('path =  \'{}\'\n'.format(self.input_path))

    def help_listup_button_clicked(self):
        help_txt = (
                    u"Asset Pageに\n"
                    u" • AssetPath  -  アセットのパス\n"
                    u" • Export Type   -  abc or anim\n"
                    u"  Abc の場合\n"
                    u"    ○ ABC Export List  -  Exportの対象(abc_setなど)\n"
                    u"    ○ TopNode  -  トップノード(rootなど)\n"
                    u"  Animの場合\n"
                    u"    ○ Anim Export List  -  Exportの対象(ctrl_setsなど)\n"
                    u" • Namespace  -  そのアセットを検索する正規表現(Object1、Object2だったらObject[0-9]*$と記述する\n"
                    u"   [0-9]* 0～9の0回以上の繰り返し、すなわちナンバリングに相当\n"
                    u"   $ 終端記号\n"
                    u"   を入力\n"
                    u"Shot pageに当該ShotのAssetを登録\n")
        # popupで表示
        QMessageBox.information(self, u'要点', help_txt)

def thread_main(**kwargs):
    argsdic = json.dumps(kwargs['argsdic'], ensure_ascii=False)
    log_path = kwargs['log_path']
    current_dir = kwargs['current_dir']
    python = PYPATH
    py_path = r'{}\pycode\exporter_bridge.py'.format(EXPORTER_PATH)
    import pprint
    pprint.pprint(kwargs)
    try:
        proc = subprocess.Popen(
            [python, py_path, argsdic], shell=True, cwd=current_dir)
        proc.wait()
    except Exception as e:
        print(e)
    # if kwargs['argsdic']['log_shape'] == True:
    #     from shell_lib import log_shaper
            # log_shaper.main(log_path)
    return


def runs(*argv):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    skin = r'{}/pycode/gui/skin.stylesheet'.format(
        EXPORTER_PATH).replace('/', '\\')
    tx_o = open(skin, 'r')
    tx_r = tx_o.read()
    tx_o.close()
    app.setStyleSheet(tx_r)
    ui = GUI(None, app)
    ui.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    runs(sys.argv[1:])
