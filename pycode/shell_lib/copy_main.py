#coding:utf-8
import os
# import shutil
import distutils.dir_util
import subprocess

def getFiles (path):
    fileDirs = os.listdir(path)
    files = [os.path.join(path,fileDir).replace("\\", "/") for fileDir in fileDirs if os.path.isfile(os.path.join(path, fileDir).replace('\\', '/'))]
    return files


def getDirs (path):
    fileDirs = os.listdir(path)
    dirs = [fileDir for fileDir in fileDirs if os.path.isdir(os.path.join(path, fileDir).replace('\\', '/'))]
    return dirs


def getCharList(charsetpath):
    charsetpath = charsetpath.replace("\\", "/")
    if not os.path.exists(charsetpath):
        raise ValueError('char is not exported')
    charlist = getDirs(charsetpath)
    return charlist


def getCurrentFilesList(charsetpath, mode="ma"):
    charsetpath = charsetpath.replace("\\", "/")
    charList = getCharList(charsetpath)
    current_files = []
    if mode=="ma":
        for char in charList:
            if "non_connection_" in char:
                continue
            current_file = getFiles(os.path.join(charsetpath, char, "current"))
            current_files.extend(current_file)
        camFile = os.path.join(charsetpath.replace('char','Cam'), "current", "cam")
        current_files.append(camFile)
    elif mode=="anim":
        for char in charList:
            current_file = getFiles(os.path.join(charsetpath, char, "current", "anim"))
            current_files.extend(current_file)
    return current_files


def getCurrentDirsList(charsetpath):
    charsetpath = charsetpath.replace("\\", "/")
    charList = getCharList(charsetpath)
    currentDirs = []
    for char in charList:
        currentDirs.append(os.path.join(charsetpath, char))
    return currentDirs


def getCamFilesList(camsetpath):
    camsetpath = os.path.join(camsetpath.replace("\\", "/"), "current", "cam")
    if not os.path.exists(camsetpath):
        raise ValueError('camera is not exported')
    camFiles = [os.path.join(camsetpath,file_name) for file_name in os.listdir(camsetpath) if str(file_name).split(".")[-1] in ["ma", "mb"]]
    return camFiles


def open_folder(path):
    subprocess.call("explorer {}".format(path.replace("/", "\\")))


def check_newest_ver(char_dir):
    next_ver = 0
    while(1):
        next_ver = next_ver+1
        next_ver_str = str(next_ver).zfill(3)
        next_dir = char_dir + "/v" + next_ver_str
        if not os.path.exists(next_dir):
            next_ver = next_ver-1
            if next_ver == 0:
                next_ver = None
            return next_ver


def copy_main(dir_path):
    char_dirs = getCurrentDirsList(dir_path)
    for char_dir in char_dirs:
        newest_ver = check_newest_ver(char_dir)
        char_name = char_dir.split("\\")[-1]
        if newest_ver is None:
            print("{}: is not exported.".format(char_name))
        else:
            newest_dir = os.path.join(char_dir, "v{}".format(str(newest_ver).zfill(3)))
            current_dir = os.path.join(char_dir, "current")
            _result = distutils.dir_util.copy_tree(newest_dir, current_dir)
            print(_result)
            print("{}: -> ver:{}".format(char_name, str(newest_ver)))
    print("=== copy finished. ==")
