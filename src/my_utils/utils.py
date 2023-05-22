from enum import Enum
from model.capture.capture_node import CaptureNode
import random,os,sys,importlib,inspect
from importlib.machinery import SourceFileLoader

import PyQt6.sip as sip
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from typing import *

def qwidget_cleanup(widget:QWidget):
    for child in widget.children():
        if(isinstance(child,QLayout)):
            layout:QLayout=child
            rev_item_i_list=list(range(layout.count())).reverse()
            while True:
                item=layout.takeAt(0)
                if item==None:
                    break
                layout.removeItem(item)
                if item.widget():
                    widget.setParent(None)
            QObjectCleanupHandler().add(layout)
        else:
            child.setParent(None)


def swap_list_item(swap_list:list,a_i:int,b_i:int):
    if a_i>b_i:
        tmp=a_i
        a_i=b_i
        b_i=tmp
        del tmp
    if a_i==b_i or swap_list==None or a_i<0 or b_i>swap_list.__len__()-1:
        return
    b=swap_list.pop(b_i)
    a=swap_list.pop(a_i)
    swap_list.insert(a_i,b)
    swap_list.insert(b_i,a)

def count_node(node:CaptureNode,count=0):
    for child in node.children:
        count=count_node(child,count)
    return count+1

T=TypeVar("T")

def safe_get_dict_val(_dict,key,type:Type[T])->T:
    key = key.value if isinstance(key,Enum) else key
    if isinstance(_dict,dict) and key in _dict:
        val=_dict[key]
        return val if isinstance(val,type) else None
    return None

def qt_file_io(
        file_mode:QFileDialog.FileMode=QFileDialog.FileMode.Directory,
        title:str=None,
        side_paths:list[str]=[]
    ):
    title= file_mode.name if title!=None else title

    file_dialog=QFileDialog()
    file_dialog.setWindowTitle(title)
    file_dialog.setFileMode(file_mode)
    file_dialog.setOption(file_dialog.Option.DontUseNativeDialog)

    file_dialog.setSidebarUrls(
        [QUrl.fromLocalFile(x) for x in side_paths]+[
        QUrl.fromLocalFile(QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DesktopLocation)[0]),
        QUrl.fromLocalFile(QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)[0]),
        QUrl.fromLocalFile(QStandardPaths.standardLocations(QStandardPaths.StandardLocation.HomeLocation)[0]),
    ])

    if(file_dialog.exec()):
        return file_dialog.selectedFiles()
    else:
        return None

def scan_class(path:str,cls:Type[T],exclude_cmp_cls=True)->list[Type[T]]:
    cls_list=[]
    sys.path.append(path) if path not in sys.path else None
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, ext = os.path.splitext(file)
            if (ext != '.py' or __file__ == f"{root}/{file}"):
                continue
            module = SourceFileLoader(filename, f"{root}/{file}").load_module()
            for clsname, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, cls):
                    if(obj==cls and not exclude_cmp_cls):
                        continue
                    cls_list.append(obj)
    return cls_list
