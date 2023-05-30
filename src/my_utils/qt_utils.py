from PyQt6.QtCore import *
from PyQt6.QtCore import QObjectCleanupHandler, QStandardPaths, QUrl
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from typing import *

from PyQt6.QtWidgets import QFileDialog, QLayout, QWidget

T = TypeVar("T", bound=QWidget)


class FormItem(QGroupBox):
    def setup(self, title: str, layout: QLayout = None, horizon_flag=False):
        self.setTitle(title)

        self.this_layout = QHBoxLayout() if horizon_flag else QVBoxLayout()
        self.setLayout(self.this_layout)
        self.this_layout.setContentsMargins(2, 2, 2, 2)
        # self.adjustSize()
        # self.setStyleSheet('border:1px solid yellow')
        self.contents = list[QWidget]()

        if isinstance(layout, QLayout):
            layout.addWidget(self)
        return self

    def add_content(self, content: T) -> T:
        self.contents.append(content)
        self.this_layout.addWidget(content)
        return content

    def add_content_chain(self, content: T):
        self.contents.append(content)
        self.this_layout.addWidget(content)
        return content, self


def add_to_layout(layout: QLayout, widget: T) -> T:
    layout.addWidget(widget)
    return widget


def gen_vert_spacer():
    return QSpacerItem(1, 1,
                       QSizePolicy.Policy.Minimum,
                       QSizePolicy.Policy.Expanding,
                       )


def qwidget_cleanup(widget: QWidget):
    for child in widget.children():
        if (isinstance(child, QLayout)):
            layout: QLayout = child
            rev_item_i_list = list(range(layout.count())).reverse()
            while True:
                item = layout.takeAt(0)
                if item == None:
                    break
                layout.removeItem(item)
                if item.widget():
                    widget.setParent(None)
            QObjectCleanupHandler().add(layout)
        else:
            child.setParent(None)


def qt_file_io(
    file_mode: QFileDialog.FileMode = QFileDialog.FileMode.Directory,
    title: str = None,
    side_paths: list[str] = []
):
    title = file_mode.name if title != None else title

    file_dialog = QFileDialog()
    file_dialog.setWindowTitle(title)
    file_dialog.setFileMode(file_mode)
    file_dialog.setOption(file_dialog.Option.DontUseNativeDialog)

    file_dialog.setSidebarUrls(
        [QUrl.fromLocalFile(x) for x in side_paths]+[
            QUrl.fromLocalFile(QStandardPaths.standardLocations(
                QStandardPaths.StandardLocation.DesktopLocation)[0]),
            QUrl.fromLocalFile(QStandardPaths.standardLocations(
                QStandardPaths.StandardLocation.DocumentsLocation)[0]),
            QUrl.fromLocalFile(QStandardPaths.standardLocations(
                QStandardPaths.StandardLocation.HomeLocation)[0]),
        ])

    if (file_dialog.exec()):
        return file_dialog.selectedFiles()
    else:
        return None


class EventQObj(QObject):

    def post_init(self):
        self.callback_dict = dict[
            Type[QEvent], list[Callable[[QEvent], None]]
        ]()
        return self

    def add_callback(self, event_cls: Type[QEvent], callback: Callable[[QEvent], None]):
        if event_cls not in self.callback_dict:
            self.callback_dict[event_cls] = []
        self.callback_dict[event_cls].append(callback)

    def rm_callback(self, callback):
        for key, val in self.callback_dict.items():
            if callback in val:
                val.remove(callback)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a1.__class__ in self.callback_dict:
            for callback in self.callback_dict[a1.__class__]:
                callback(a1)
        return super().eventFilter(a0, a1)
