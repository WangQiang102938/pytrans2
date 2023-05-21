from enum import Enum
from typing import Any, List
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
from PyQt6.QtWidgets import QWidget
from controller.pipeline.pipeline_hub import PipeMemo, PipeUpdateMode, PipelineHub, PipelineNode
from model.capture.capture_node import CaptureNode
import utils.pipeline_utils as pipeline_utils
import utils
from utils.pipeline_utils import FormItem,add_to_layout
import http.client
from urllib.parse import urlencode
import json

class PortEnum(Enum):
    IN_TEXT='in:[[str]]'
    OUT_TEXT='out:[[str]]'

class Memo(PipeMemo):
    def __init__(self, pipe_ins: PipelineNode) -> None:
        super().__init__(pipe_ins)
        self.txt_in:list[list[str]]=None
        self.txt_out:list[list[str]]=None

class GoogleTranslateWidget(QFrame):
    def bind(self):
        self.main_layout=QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

        self.api_key_edit= FormItem(self).setup(
            'Api Key',self.main_layout
        ).add_content(QLineEdit())

        self.char_limit_edit= FormItem(self).setup(
            'Max chars size',self.main_layout
        ).add_content(QSpinBox())
        self.char_limit_edit.setRange(10,100000)
        self.char_limit_edit.setValue(5000)

        self.src_lang_combo= FormItem(self).setup(
            'Source Language',self.main_layout
        ).add_content(QComboBox())

        self.tar_lang_combo= FormItem(self).setup(
            'Target Language',self.main_layout
        ).add_content(QComboBox())


        self.print_output= FormItem(self).setup(
            'Print result to console',self.main_layout
        ).add_content(QCheckBox())

        self.main_layout.addItem(QSpacerItem(0,0,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        ))
        for item in SupportLangEnum:
            self.src_lang_combo.addItem(item.name,item.value)
            self.tar_lang_combo.addItem(item.name,item.value)
        self.src_lang_combo.setCurrentText(            SupportLangEnum.English.name        )
        self.tar_lang_combo.setCurrentText(            SupportLangEnum.Chinese_Simplified.name        )

        return self


class GoogleTranslate(PipelineNode):
    name='Google Translate'

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)
        self.option_widget=GoogleTranslateWidget().bind()
        self.node2text_dict=dict[CaptureNode,list[list[str]]]()
        self.text2trans=dict[str,str]()

    def option_ui_setup(self, container: QWidget):
        container_layout = QHBoxLayout(container) if container.layout()==None else container.layout()
        container_layout.setContentsMargins(2, 2, 2, 2)
        container_layout.addWidget(self.option_widget)
        container.setVisible(True)
        container.show()

    def process_start(self):
        self.node2text_dict.clear()
        self.text2trans.clear()

    def process_capnode(self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input):
        memo=self.find_memo(node,Memo,True)
        text_in=utils.safe_get_dict_val(input,PortEnum.IN_TEXT,list)
        if text_in==None:
            return
        try:
            for section in text_in:
                for sent in section:
                    if not isinstance(sent,str):
                        raise TypeError(sent)
            for section in text_in:
                for sent in section:
                    self.text2trans[sent]=None
            self.node2text_dict[node]=text_in
        except Exception as e:
            print(e)


    def process_end(self):
        translate_queue=list[list[str]]()
        working_queue=list[str]()
        count=0
        # split to max_size
        for sent,val in self.text2trans.items():
            if (working_queue.__len__()-2)*2+count+sent.__len__()>self.option_widget.char_limit_edit.value():
                translate_queue.append(working_queue)
                working_queue=list[str]()
                count=0
            working_queue.append(sent)
            count+=sent.__len__()
        translate_queue.append(working_queue) if working_queue.__len__()>0 else None
        # translate
        progressbar=self.pipe_hub.ui.pipeCapNodeProgress
        progressbar.setRange(0,translate_queue.__len__())
        progressbar.setFormat(f"Api req:%v/{translate_queue.__len__()}")
        progressbar.reset()
        for i,origin_sents in enumerate(translate_queue):
            queue="\n\n".join(origin_sents)
            result=self.google_trans(queue)
            if result!=None:
                translated_sents=result.split("\n\n")
                for origin,trans in zip(origin_sents,translated_sents):
                    self.text2trans[origin]=trans
            progressbar.setValue(i+1)
            self.pipe_hub.ctrl_hub.main.app.processEvents()
        progressbar.resetFormat()
        # put result to node memo
        for capnode,origin_sections in self.node2text_dict.items():
            memo=self.find_memo(capnode,Memo)
            if memo==None:
                continue
            trans_sec_list=list[list[str]]()
            memo.txt_out=list[list[str]]()
            for origin_sents in origin_sections:
                trans_sents=list[str]()
                for origin_sent in origin_sents:
                    trans_sents.append(self.text2trans[origin_sent])
                memo.txt_out.append(trans_sents)
            if self.option_widget.print_output.isChecked():
                print(memo.txt_out)

    def get_output(self, node: CaptureNode, key: str) -> Any:
        memo=self.find_memo(node,Memo)
        if key==PortEnum.OUT_TEXT.value and memo!=None:
            return memo.txt_out
        else:
            return None

    def google_trans(self,queue:str):
        try:
            conn = http.client.HTTPSConnection("translation.googleapis.com")
            params = {
                "q": queue,
                "target": self.option_widget.tar_lang_combo.currentData(),
                "source": self.option_widget.src_lang_combo.currentData(),
                'key': self.option_widget.api_key_edit.text(),
                'format': 'text'
            }
            payload = urlencode(params)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'Accept-Encoding': "application/gzip",
            }

            conn.request("POST", "/language/translate/v2", payload, headers)

            res = conn.getresponse()
            data = res.read()
            data_decode = json.loads(data.decode("utf-8"))
            result:str=data_decode['data']['translations'][0]['translatedText']
        except Exception as e:
            print("GoogleTransApiFailed")
            result=None
        finally:
            return result


    def get_port_keys(self, input_port=True) -> List[str]:
        return [
            PortEnum.IN_TEXT.value
        ]if input_port else[
            PortEnum.OUT_TEXT.value
        ]


class SupportLangEnum(Enum):
    Afrikaans="af"
    Albanian="sq"
    Amharic="am"
    Arabic="ar"
    Armenian="hy"
    Assamese="as"
    Aymara="ay"
    Azerbaijani="az"
    Bambara="bm"
    Basque="eu"
    Belarusian="be"
    Bengali="bn"
    Bhojpuri="bho"
    Bosnian="bs"
    Bulgarian="bg"
    Catalan="ca"
    Cebuano="ceb"
    Chinese_Simplified="zh-CN"
    Chinese_Traditional="zh-TW"
    Corsican="co"
    Croatian="hr"
    Czech="cs"
    Danish="da"
    Dhivehi="dv"
    Dogri="doi"
    Dutch="nl"
    English="en"
    Esperanto="eo"
    Estonian="et"
    Ewe="ee"
    Filipino_Tagalog="fil"
    Finnish="fi"
    French="fr"
    Frisian="fy"
    Galician="gl"
    Georgian="ka"
    German="de"
    Greek="el"
    Guarani="gn"
    Gujarati="gu"
    Haitian_Creole="ht"
    Hausa="ha"
    Hawaiian="haw"
    Hebrew="he or iw"
    Hindi="hi"
    Hmong="hmn"
    Hungarian="hu"
    Icelandic="is"
    Igbo="ig"
    Ilocano="ilo"
    Indonesian="id"
    Irish="ga"
    Italian="it"
    Japanese="ja"
    Javanese="jv or jw"
    Kannada="kn"
    Kazakh="kk"
    Khmer="km"
    Kinyarwanda="rw"
    Konkani="gom"
    Korean="ko"
    Krio="kri"
    Kurdish="ku"
    Kurdish_Sorani="ckb"
    Kyrgyz="ky"
    Lao="lo"
    Latin="la"
    Latvian="lv"
    Lingala="ln"
    Lithuanian="lt"
    Luganda="lg"
    Luxembourgish="lb"
    Macedonian="mk"
    Maithili="mai"
    Malagasy="mg"
    Malay="ms"
    Malayalam="ml"
    Maltese="mt"
    Maori="mi"
    Marathi="mr"
    Meiteilon_Manipuri="mni-Mtei"
    Mizo="lus"
    Mongolian="mn"
    Myanmar_Burmese="my"
    Nepali="ne"
    Norwegian="no"
    Nyanja_Chichewa="ny"
    Odia_Oriya="or"
    Oromo="om"
    Pashto="ps"
    Persian="fa"
    Polish="pl"
    Portuguese_Portugal, Brazil="pt"
    Punjabi="pa"
    Quechua="qu"
    Romanian="ro"
    Russian="ru"
    Samoan="sm"
    Sanskrit="sa"
    Scots_Gaelic="gd"
    Sepedi="nso"
    Serbian="sr"
    Sesotho="st"
    Shona="sn"
    Sindhi="sd"
    Sinhala_Sinhalese="si"
    Slovak="sk"
    Slovenian="sl"
    Somali="so"
    Spanish="es"
    Sundanese="su"
    Swahili="sw"
    Swedish="sv"
    Tagalog_Filipino="tl"
    Tajik="tg"
    Tamil="ta"
    Tatar="tt"
    Telugu="te"
    Thai="th"
    Tigrinya="ti"
    Tsonga="ts"
    Turkish="tr"
    Turkmen="tk"
    Twi_Akan="ak"
    Ukrainian="uk"
    Urdu="ur"
    Uyghur="ug"
    Uzbek="uz"
    Vietnamese="vi"
    Welsh="cy"
    Xhosa="xh"
    Yiddish="yi"
    Yoruba="yo"
    Zulu="zu"
