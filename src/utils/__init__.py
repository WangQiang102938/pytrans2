import utils.pipeline_utils
import utils.preview_utils
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


