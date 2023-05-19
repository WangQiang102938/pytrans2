import utils.pipeline_utils as pipeline_utils
import utils.preview_utils as preview_utils
import random

import PyQt6.sip as sip
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

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
