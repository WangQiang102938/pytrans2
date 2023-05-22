from enum import Enum
from typing import Any, List
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
from PyQt6.QtWidgets import QWidget
from controller.pipeline.pipeline_hub import PipeMemo, PipeUpdateMode, PipelineHub, PipelineNode
from model.capture.capture_node import CaptureNode
import my_utils.qt_utils as qt_utils
import my_utils
import os,sys,shutil

class PortEnum(Enum):
    IN_ORIGIN='origin_in:[[str]]'
    IN_TRANS='translated_in:[[str]]'
    IN_IMAGE='image_in:Image'

class ImageExt(Enum):
    JPEG='jpeg'
    PNG='png'

class Memo(PipeMemo):
    def __init__(self, pipe_ins: PipelineNode) -> None:
        super().__init__(pipe_ins)
        self.id_img_dict:dict[str,Image]=None
        self.html_txts:list[str]=None
        self.html:str=None
        self.img_ext:str=None
        self.title:str=None

class HtmlGenWidget(QFrame):
    def bind(self,pipe_node:'HtmlGenV1'):
        self.pipe_node=pipe_node
        main_layout=self.main_layout=QVBoxLayout()
        self.setLayout(main_layout)

        self.save_btn,save_con=qt_utils.FormItem(self).setup(
            "File",main_layout
        ).add_content_chain(QPushButton("Save"))
        self.open_after_save_check=save_con.add_content(QCheckBox("Open after saved"))

        self.image_ext_combo=qt_utils.FormItem(self).setup(
            "Image Type",main_layout
        ).add_content(QComboBox())
        for item in ImageExt:
            self.image_ext_combo.addItem(item.name,item.value)

        self.print_check=qt_utils.FormItem(self).setup(
            "",main_layout
        ).add_content(QCheckBox("Print html"))

        self.main_layout.addItem(qt_utils.gen_vert_spacer())
        return self

class HtmlGenV1(PipelineNode):
    name="HTML Gen V1"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)
        self.option_widget=HtmlGenWidget().bind(self)
        self.option_widget.save_btn.clicked.connect(self.save)

    def get_port_keys(self, input_port=True) -> List[str]:
        return [
            PortEnum.IN_IMAGE.value,
            PortEnum.IN_TRANS.value,
            PortEnum.IN_ORIGIN.value,
        ] if input_port else []

    def option_ui_setup(self, container: QWidget):
        container_layout = QHBoxLayout(container) if container.layout()==None else container.layout()
        container_layout.setContentsMargins(2, 2, 2, 2)
        container_layout.addWidget(self.option_widget)

    def process_start(self):
        return super().process_start()

    def process_capnode(self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input):
        memo=self.find_memo(node,Memo,True)
        memo.id_img_dict=dict()
        memo.html_txts=list()
        for child in node.children:
            child_memo=self.find_memo(child,Memo)
            if child_memo==None:
                continue
            if child_memo.html_txts!=None:
                memo.html_txts+=child_memo.html_txts
            if child_memo.id_img_dict!=None:
                for key,val in child_memo.id_img_dict.items():
                    memo.id_img_dict[key]=val
        if(node.get_node_type()==node.Type.ROOT):
            if self.option_widget.print_check.isChecked():
                for node in memo.html_txts:
                    print(node)

        image=my_utils.safe_get_dict_val(input,PortEnum.IN_IMAGE,Image)
        origin_txt:list[list[str]]=my_utils.safe_get_dict_val(input,PortEnum.IN_ORIGIN,list)
        trans_txt:list[list[str]]=my_utils.safe_get_dict_val(input,PortEnum.IN_TRANS,list)

        if(image==None):
            return
        aligned_txt= self.align_txt(origin_txt, trans_txt)
        if aligned_txt==None:
            return

        html_row = self.gen_html(image, aligned_txt)

        memo.id_img_dict[str(id(image))]=image
        memo.html_txts+=[html_row.to_html()]


    def gen_html(self, image, aligned_txt):
        html_row = SimpleHTMLTag('tr', args='class="capture-row"').chain_content(
            SimpleHTMLTag('td', args='class="capture-image-td"').chain_content(
                SimpleHTMLTag('div', args='class="capture-clip-div"').chain_content(
                    SimpleHTMLTag("img", args=f"src=\"./images/{id(image)}.{self.option_widget.image_ext_combo.currentData()}\"", surround=False)
                )
            )
        )
        text_td = SimpleHTMLTag('td', args='class="capture-text-td"').add_me_to(html_row)
        text_con = SimpleHTMLTag('div', args='class="capture-tex-con"').add_me_to(text_td)

        for sec_pair in aligned_txt:
            con = SimpleHTMLTag('div', args='class="capture-text-block-con"').add_me_to(text_con)
            for sent_pair in sec_pair:
                con.add_content(SimpleHTMLTag('div', args='class="paired-translate-con"').chain_content(
                    SimpleHTMLTag('p', args='class="origin-text"').chain_content(SimpleHTMLTag(sent_pair[0], text_flag=True))
                ).chain_content(
                    SimpleHTMLTag('br', surround=False)
                ).chain_content(
                    SimpleHTMLTag('p', args='class="trans-text"').chain_content(SimpleHTMLTag(sent_pair[1], text_flag=True))
                ))

        return html_row

    def align_txt(self, origin_txt, trans_txt):
        sec_list=list[list[tuple[str,str]]]()
        try:
            if len(origin_txt)==len(trans_txt): # section aligned
                for origin_sec,trans_sec in zip(origin_txt,trans_txt):
                    sent_list=list[tuple[str,str]]()
                    if len(origin_sec)==len(trans_sec): # sents aligned
                        for origin_sent,trans_sent in zip(origin_sec,trans_sec):
                            sent_list.append((origin_sent,trans_sent))
                    else: # sents aligned
                        sent_list.append((
                            "\n\n".join(origin_sec),
                            "\n\n".join(trans_sec)
                        ))
                    sec_list.append(sent_list)
            else:
                sec_list.append([[(
                    "\n\n\n".join(["\n\n".join(x) for x in origin_txt]),
                    "\n\n\n".join(["\n\n".join(x) for x in trans_txt])
                )]])
            return sec_list
        except Exception as e:
            return None

    def process_end(self):
        working_doc=self.pipe_hub.ctrl_hub.main.model_hub.working_doc
        memo=self.find_memo(working_doc.root_node,Memo)
        if memo==None:
            return
        title=memo.title=os.path.splitext(os.path.split(working_doc.path)[1])[0]
        memo.html=html_template.format(title=title,trs="\n".join(memo.html_txts))
        memo.img_ext=self.option_widget.image_ext_combo.currentData()

    def save(self):
        working_doc=self.pipe_hub.ctrl_hub.main.model_hub.working_doc
        memo=self.find_memo(working_doc.root_node,Memo)
        title=memo.title
        paths=qt_utils.qt_file_io(title="Save To ...",side_paths=[os.getcwd()])
        for path in paths:
            if os.path.isfile(path):
                continue
            # TODO: customize path
            saving_path=f"{path}/{title}"
            if os.path.exists(saving_path) and os.path.isdir(saving_path):
                overwrite_confirm=QMessageBox.question(
                    None,"Overwrite confirm","This directory already exist, Overwrite?"
                )
                if overwrite_confirm==QMessageBox.DialogCode.Rejected:
                    continue
            else:
                os.mkdir(saving_path)
            shutil.copy2(working_doc.path,f"{saving_path}/")
            shutil.copy2(f"{os.path.split(__file__)[0]}/styles.css",f"{saving_path}/")
            with open(f"{saving_path}/{title}.html","w") as f:
                f.write(memo.html)
            img_path=f"{saving_path}/images"
            if not os.path.isdir(img_path):
                os.mkdir(img_path)
            for key,image in memo.id_img_dict.items():
                image.save(f"{img_path}/{key}.{memo.img_ext}")
            if self.option_widget.open_after_save_check.isChecked():
                import subprocess
                subprocess.call(['open', saving_path])
                break




class SimpleHTMLTag:
    def __init__(self, tag: str, surround: bool = True, args: str = "", tabsize=4, text_flag=False) -> None:
        self.tag = tag
        self.contents = list[SimpleHTMLTag]()
        self.surround = surround
        self.args = args
        self.tabsize = 4
        self.textflag = text_flag

    def to_html(self) -> str:
        if(self.textflag):
            return self.tag
        contents_html = "\n"+"\n".join([x.to_html() for x in self.contents])
        contents_html=f"\n{self.tabsize*' '}".join(contents_html.split('\n'))
        if self.surround:
            return "<{tag} {arg}>{content}\n</{tag}>".format(tag=self.tag, arg=self.args, content=contents_html)
        else:
            return "<{tag} {arg}/>".format(tag=self.tag, arg=self.args)

    def chain_content(self, content: 'SimpleHTMLTag'):
        self.contents.append(content)
        return self

    def add_content(self, content: 'SimpleHTMLTag'):
        self.contents.append(content)
        return content

    def add_me_to(self, parent: 'SimpleHTMLTag'):
        parent.add_content(self)
        return self

html_template="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="styles.css" rel="stylesheet" type="text/css">
    <title>{title}</title>
</head>
<body>
    <table>
        <tr>
            <th>Capture</th>
            <th>Trans</th>
        </tr>
        {trs}
    </table>
</body>
</html>
"""
