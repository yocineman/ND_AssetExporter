#coding:utf-8
import os,sys
try:
    from importlib import reload
except:
    pass

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)
    from ExportCameraAbc import gui_main
    reload(gui_main)
    gui_main.runs()
