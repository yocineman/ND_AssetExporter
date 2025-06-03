# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import yaml
import time


onpath = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")


def set_env():
    # arnold
    sys.path.append("Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts")
    # scripts
    scripts_path = "Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts"
    if os.environ.get("PYTHONPATH") is None:
        os.environ["PYTHONPATH"] = scripts_path
    else:
        os.environ["PYTHONPATH"] = (
            scripts_path + ";" + os.environ["PYTHONPATH"].rstrip(";")
        )
    if os.environ.get("PYTHONPATH") is None:
        os.environ["PYTHONPATH"] = scripts_path
    else:
        os.environ["PYTHONPATH"] = (
            scripts_path + ";" + os.environ["PYTHONPATH"].rstrip(";")
        )
    # plug-in
    if os.environ.get("MAYA_PLUG_IN_PATH") is None:
        os.environ["MAYA_PLUG_IN_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/plug-ins"
        )
    else:
        os.environ["MAYA_PLUG_IN_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/plug-ins;"
            + os.environ["MAYA_PLUG_IN_PATH"].rstrip(";")
        )
    # mod
    mod_path = "Y:/users/env/maya/2023/mod"
    if os.environ.get("MAYA_MODULE_PATH") is None:
        os.environ["MAYA_MODULE_PATH"] = mod_path
    else:
        os.environ["MAYA_MODULE_PATH"] = (
            mod_path + ";" + os.environ["MAYA_MODULE_PATH"].rstrip(";")
        )
    # path
    if os.environ.get("PATH") is None:
        os.environ["PATH"] = "Y:/users/env/arnold/mtoa/2023_MtoA_531/bin"
    else:
        os.environ["PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/bin;"
            + os.environ["PATH"].rstrip(";")
        )
    if os.environ.get("ARNOLD_PATH") is None:
        os.environ["ARNOLD_PATH"] = "Y:/users/env/arnold/mtoa/2023_MtoA_531"
    else:
        os.environ["ARNOLD_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531;"
            + os.environ["ARNOLD_PATH"].rstrip(";")
        )
    if os.environ.get("ARNOLD_PLUGIN_PATH") is None:
        os.environ["ARNOLD_PLUGIN_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/procedurals;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/shaders;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/shaders;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/procedurals"
        )
    else:
        os.environ["ARNOLD_PLUGIN_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/procedurals;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/shaders;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/shaders;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/procedurals;"
            + os.environ["ARNOLD_PLUGIN_PATH"].rstrip(";")
        )
    os.environ["MTOA_EXTENSIONS_PATH"] = (
        "Y:/users/env/arnold/mtoa/2023_MtoA_531/extensions"
    )
    os.environ["MTOA_PATH"] = "Y:/users/env/arnold/mtoa/2023_MtoA_531/"
    if os.environ.get("MTOA_SCRIPT_PATH") is None:
        os.environ["MTOA_SCRIPT_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts/mtoa/mel"
        )
    else:
        os.environ["MTOA_SCRIPT_PATH"] = (
            "Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts;"
            + "Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts/mtoa/mel"
        )
    
    os.environ["MAYA_PLUG_IN_RESOURCE_PATH"] = ("Y:/users/env/arnold/mtoa/2023_MtoA_531/resources;"
        "C:/Program Files/Autodesk/Maya2023/plug-ins/ATF/resources")


def run_subprocess(cmd, kwargs):
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            env=os.environ,
            cwd=os.path.dirname(kwargs["input_path"]),
            capture_output=True,  # stdoutとstderrを捕捉
            text=True,  # テキストモードで捕捉
            check=False,  # return codeが非ゼロでも例外を発生させない
        )

        # 捕捉した stdout をすぐに表示
        print("--- Captured STDOUT ---")
        print(proc.stdout)
        print("--- End STDOUT ---")

        # 捕捉した stderr をすぐに表示
        print("--- Captured STDERR ---")
        print(proc.stderr)
        print("--- End STDERR ---")

        # 追加デバッグ情報: return code
        print(f"--- Process returned code: {proc.returncode} ---")

        # 捕捉した出力をデバッグ用のログファイルにも書き出す
        # ログファイルのパスは、Deadline Workerから書き込み可能な場所を指定
        # 例: ジョブIDやタイムスタンプを使ってユニークなファイル名にする
        log_dir = "Y:/users/deadlineuser/DCC_log/ND_AssetExporter"  # ログ出力パス
        os.makedirs(log_dir, exist_ok=True)
        username= os.environ.get("USERNAME", "unknown_user")
        log_file_path = os.path.join(log_dir, f"maya_batch_debug_log_{username}{os.getpid()}.txt")

        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(
                f"Command executed: {' '.join(cmd) if isinstance(cmd, list) else cmd}\n\n"
            )
            f.write("--- STDOUT ---\n")
            f.write(proc.stdout)
            f.write("\n--- STDERR ---\n")
            f.write(proc.stderr)
            f.write(f"\n--- Return Code: {proc.returncode} ---\n")

    except Exception as e:
        # subprocess.run 自体が失敗した場合の例外処理
        print(f"ERROR during subprocess execution: {e}")
    print("return code: {}".format(proc.returncode))
    print("captured stdout: {}".format(proc.stdout))
    print("captured stderr: {}".format(proc.stderr))


def maya_cmd_maker(unique_order, mayafile=None, is_exe=False):
    maya_cmd = (
        "import sys;"
        + "sys.path.append('{}/maya_lib');".format(onpath)
        + "sys.path.append('{}');".format(onpath)
        + "sys.path.append('Y:/users/env/arnold/mtoa/2023_MtoA_531/scripts');"
        + "sys.path.append('C:/Program Files/Autodesk/Maya2023/Python/Lib/site-packages/maya/mel');"
        + "sys.path.append('Y:/users/env/maya/2023/mod');")
    
    if is_exe is True:
        mayaBatch = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\maya.exe"
    else:
        mayaBatch = "C:\\Program Files\\Autodesk\\Maya2023\\bin\\mayabatch.exe"
    cmd = [mayaBatch]
    
    maya_cmd = maya_cmd + unique_order
    if mayafile is not None:
        cmd.append("-file")
        cmd.append(mayafile.replace("\\", "/"))

    cmd.append("-command")
    cmd.append('python("{}")'.format(maya_cmd.replace(";", "\;").replace("'", "'")))
    return cmd


# ------------------------------------
#  Anim
# ------------------------------------
def animExport(**kwargs):
    print("###setn_env###")
    set_env()
    unique_order = (
        "import maya.cmds as cmds;cmds.loadPlugin('mtoa');cmds.file('{}', f=True,o=True);"
        "from maya_lib.ndPyLibExportAnim import export_anim_main;"
        "export_anim_main(**{})".format(kwargs["input_path"], kwargs)
    )
    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    print(cmd)
    run_subprocess(cmd, kwargs)


def animAttach(**kwargs):
    file_namespace = kwargs["file_namespace"]
    ma_ver_path = kwargs["ma_ver_path"]
    anim_ver_path = kwargs["anim_ver_path"]
    asset_path = kwargs["asset_path"]
    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "import maya.cmds as cmds;"
        "saveAs('{}');".format(ma_ver_path)
        + "loadAsset('{}', '{}');".format(asset_path, file_namespace)
        + "loadAsset('{}', '{}_anim');".format(anim_ver_path, file_namespace)
        + "saveAs('{}')".format(ma_ver_path)
    )
    cmd = maya_cmd_maker(unique_order,  is_exe=kwargs["is_exe"])
    print(cmd)
    run_subprocess(cmd, kwargs)


def animReplace(**kwargs):
    ma_current_path = kwargs["ma_current_path"]
    publish_current_anim_path = kwargs["anim_current_path"]
    file_namespace = kwargs["file_namespace"]
    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "replaceAsset('{}', '{}_anim');".format(
            publish_current_anim_path, file_namespace
        )
        + "save();"
    )
    cmd = maya_cmd_maker(
        unique_order,
        mayafile=ma_current_path,
        is_exe=kwargs["is_exe"],
    )
    run_subprocess(cmd, kwargs)


def abcExport(**kwargs):
    unique_order = (
        "import maya.cmds as cmds;cmds.file('{}', f=True,o=True);"
        "from ndPyLibExportAbc import ndPyLibExportAbc_caller;"
        "ndPyLibExportAbc_caller({})".format(kwargs["input_path"], kwargs)
    )
    cmd = maya_cmd_maker(unique_order,  is_exe=kwargs["is_exe"])
    run_subprocess(cmd, kwargs)


def abcAttach(**kwargs):
    asset_path = kwargs["asset_path"]
    namespace = kwargs["file_namespace"]
    top_node = namespace + ":" + kwargs["top_node"]
    ma_ver_path = kwargs["ma_ver_path"]
    abc_ver_path = kwargs["abc_ver_path"]

    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "import maya.cmds as cmds;"
        "saveAs('{}');".format(ma_ver_path)
        + "loadAsset('{}', '{}');".format(asset_path, namespace)
        + "selHierarchy=cmds.ls('{}', dag=True);".format(top_node)
        + "attachABC('{}', '{}', selHierarchy);".format(abc_ver_path, namespace)
        + "saveAs('{}')".format(ma_ver_path)
    )
    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    print("####abcAttach####")
    print(cmd)
    run_subprocess(cmd, kwargs)


def abcReplace(**kwargs):
    ma_current_path = kwargs["ma_current_path"]
    abc_current_path = kwargs["abc_current_path"]
    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "replaceABCPath('{}');".format(abc_current_path) + "save();"
    )
    cmd = maya_cmd_maker(
        unique_order,
        mayafile=ma_current_path,
        is_exe=kwargs["is_exe"],
    )
    print("####abcReplace####")
    print(cmd)    
    run_subprocess(cmd, kwargs)

# ------------------------------------
#  Abc&Anim
# ------------------------------------
def abcAnimAttach(**kwargs):
    asset_path = kwargs["asset_path"]
    namespace = kwargs["file_namespace"]
    top_node = namespace + ":" + kwargs["top_node"]
    ma_ver_path = kwargs["ma_ver_path"]
    abc_ver_path = kwargs["abc_ver_path"]
    anim_ver_path = kwargs["anim_ver_path"]

    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "import maya.cmds as cmds;"
        "saveAs('{}');".format(ma_ver_path)
        + "loadAsset('{}', '{}');".format(asset_path, namespace)
        + "selHierarchy=cmds.ls('{}', dag=True);".format(top_node)
        + "attachABC('{}', '{}', selHierarchy);".format(abc_ver_path, namespace)
        + "loadAsset('{}', '{}_anim');".format(anim_ver_path, namespace)
        + "saveAs('{}');".format(ma_ver_path)
    )

    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    run_subprocess(cmd, kwargs)


def abcAnimReplace(**kwargs):
    namespace = kwargs["file_namespace"]
    ma_current_path = kwargs["ma_current_path"]
    abc_current_path = kwargs["abc_current_path"]
    anim_current_path = kwargs["anim_current_path"]
    unique_order = (
        "from maya_lib.mayaBasic import *;"
        "replaceABCPath('{}');".format(abc_current_path)
        + "replaceAsset('{}', '{}_anim');".format(anim_current_path, namespace)
        + "save();"
    )
    cmd = maya_cmd_maker(
        unique_order,
        mayafile=ma_current_path,
        is_exe=kwargs["is_exe"],
    )
    run_subprocess(cmd, kwargs)


# ------------------------------------
#  Cam
# ------------------------------------
def camExport(**kwargs):
    unique_order = (
        "from ndPyLibExportCam import ndPylibExportCam_caller;"
        "ndPylibExportCam_caller(**{})".format(kwargs)
    )
    cmd = maya_cmd_maker(
        unique_order, mayafile=kwargs["input_path"], is_exe=kwargs["is_exe"]
    )
    run_subprocess(cmd, kwargs)


# ------------------------------------
#  Ass
# ------------------------------------
def assExport(**kwargs):
    unique_order = (
        "from maya_lib.ndPyLibExportAss import export_ass_main;"
        "export_ass_main(**{})".format(kwargs)
    )
    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    run_subprocess(cmd, kwargs)

def assAttach(**kwargs):
    unique_order = (
        "from maya_lib.ndPyLibAttachAss import attach_ass_main;"
        "attach_ass_main(**{})".format(kwargs)
    )
    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    print(cmd)
    run_subprocess(cmd, kwargs)


def assReplace(**kwargs):
    unique_order = (
        "from maya_lib.ndPyLibReplaceAss import replace_ass_main;"
        "replace_ass_main(**{})".format(kwargs)
    )
    cmd = maya_cmd_maker(unique_order, is_exe=kwargs["is_exe"])
    print(cmd)
    run_subprocess(cmd, kwargs)
