from enum import Enum
from model.capture.capture_node import CaptureNode
import utils.pipeline_utils as pipeline_utils
import utils.preview_utils as preview_utils
import random

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
