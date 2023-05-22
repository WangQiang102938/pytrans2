from enum import Enum
from model.capture.capture_node import CaptureNode
import random,os,sys,importlib,inspect
from importlib.machinery import SourceFileLoader

import PyQt6.sip as sip
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from typing import *

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
                    if(obj==cls and exclude_cmp_cls):
                        continue
                    cls_list.append(obj)
    return cls_list

def split_dir_from_file(filepath:str):
    return os.path.split(filepath)[0]
