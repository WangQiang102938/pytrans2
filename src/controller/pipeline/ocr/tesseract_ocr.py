from enum import Enum
from typing import Any, List
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
from controller.pipeline.pipeline_hub import PipeMemo, PipeUpdateMode, PipelineHub, PipelineNode
from model.capture.capture_node import CaptureNode
import my_utils.qt_utils as qt_utils
import my_utils
import pytesseract

class PortEnum(Enum):
    IN_IMAGE='input image'
    OUT_TEXT='output text'

class Memo(PipeMemo):
    def __init__(self, pipe_ins: PipelineNode) -> None:
        super().__init__(pipe_ins)
        self.image_in:Image=None
        self.out_txt:str=None

class TesseractOCR(PipelineNode):
    name="Tesseract OCR"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)
        self.widget = TesseractWidget().bind()

    def option_ui_setup(self, container: QWidget):
        container_layout = QHBoxLayout(container) if container.layout()==None else container.layout()
        container_layout.setContentsMargins(2, 2, 2, 2)
        container_layout.addWidget(self.widget)
        container.setVisible(True)
        container.show()

    def get_port_keys(self, input_port=True) -> List[str]:
        return [
            PortEnum.IN_IMAGE.value
            ] if input_port else [
            PortEnum.OUT_TEXT.value
            ]

    def process_capnode(self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input):
        if mode==PipeUpdateMode.BYPASS:
            return True
        memo=self.find_memo(node,Memo,True)
        img=my_utils.safe_get_dict_val(input,PortEnum.IN_IMAGE.value,Image)
        if img==None:
            return False
        memo.image_in=img
        lang_combo = self.widget.lang_select_combo
        ocr_result = pytesseract.image_to_string(
            img, lang=lang_combo.currentData())
        memo.out_txt=ocr_result
        return True

    def get_output(self, node: CaptureNode, key: str) -> Any:
        memo=self.find_memo(node,Memo,False)
        if key==PortEnum.OUT_TEXT.value:
            return memo.out_txt
        return None


class TesseractWidget(QFrame):
    def bind(self):
        self.main_layout = QVBoxLayout()
        # self.setStyleSheet("border:1px solid red")
        self.setLayout(self.main_layout)

        self.realtime_check =qt_utils.FormItem(self).setup(
            "",self.main_layout
        ).add_content(QCheckBox("Realtiem Update"))

        self.lang_select_combo =qt_utils.FormItem(self).setup(
            "OCR Lang",self.main_layout
        ).add_content(QComboBox())

        self.lang_select_combo.setMaximumWidth(100)
        self.lang_select_combo.setMaxVisibleItems(10)
        self.lang_select_combo.setStyleSheet(
            "QComboBox{combobox-popup:0;}"
        )
        for enum in TesseractLangEnum:
            self.lang_select_combo.addItem(enum.name, enum.value)
        self.lang_select_combo.setCurrentText(TesseractLangEnum.English.name)

        self.main_layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        # self.setStyleSheet('border:1px solid red')
        return self


class TesseractLangEnum(Enum):
    Afrikaans = 'afr'
    Amharic = 'amh'
    Arabic = 'ara'
    Assamese = 'asm'
    Azerbaijani = 'aze'
    Azerbaijani_Cyrilic = 'aze_cyrl'
    Belarusian = 'bel'
    Bengali = 'ben'
    Tibetan = 'bod'
    Bosnian = 'bos'
    Bulgarian = 'bul'
    Catalan_Valencian = 'cat'
    Cebuano = 'ceb'
    Czech = 'ces'
    Chinese_Simplified = 'chi_sim'
    Chinese_Traditional = 'chi_tra'
    Cherokee = 'chr'
    Welsh = 'cym'
    Danish = 'dan'
    Danish_Fraktur = 'dan_frak'
    German = 'deu'
    German_Fraktur = 'deu_frak'
    Dzongkha = 'dzo'
    Greek_Modern_1453 = 'ell'
    English = 'eng'
    English_Middle_1100_1500 = 'enm'
    Esperanto = 'epo'
    Math_equation_detection_module = 'equ'
    Estonian = 'est'
    Basque = 'eus'
    Persian = 'fas'
    Finnish = 'fin'
    French = 'fra'
    Frankish = 'frk'
    French_Middleca_1400_1600 = 'frm'
    Irish = 'gle'
    Galician = 'glg'
    Greek_Ancient_to_1453 = 'grc'
    Gujarati = 'guj'
    Haitian_Haitian_Creole = 'hat'
    Hebrew = 'heb'
    Hindi = 'hin'
    Croatian = 'hrv'
    Hungarian = 'hun'
    Inuktitut = 'iku'
    Indonesian = 'ind'
    Icelandic = 'isl'
    Italian = 'ita'
    Italian_Old = 'ita_old'
    Javanese = 'jav'
    Japanese = 'jpn'
    Kannada = 'kan'
    Georgian = 'kat'
    Georgian_Old = 'kat_old'
    Kazakh = 'kaz'
    Central_Khmer = 'khm'
    Kirghiz_Kyrgyz = 'kir'
    Korean = 'kor'
    Kurdish = 'kur'
    Lao = 'lao'
    Latin = 'lat'
    Latvian = 'lav'
    Lithuanian = 'lit'
    Malayalam = 'mal'
    Marathi = 'mar'
    Macedonian = 'mkd'
    Maltese = 'mlt'
    Malay = 'msa'
    Burmese = 'mya'
    Nepali = 'nep'
    Dutch_Flemish = 'nld'
    Norwegian = 'nor'
    Oriya = 'ori'
    Orientation_and_script_detection_module = 'osd'
    Panjabi_Punjabi = 'pan'
    Polish = 'pol'
    Portuguese = 'por'
    Pushto_Pashto = 'pus'
    Romanian_Moldavian_Moldovan = 'ron'
    Russian = 'rus'
    Sanskrit = 'san'
    Sinhala_Sinhalese = 'sin'
    Slovak = 'slk'
    Slovak_Fraktur = 'slk_frak'
    Slovenian = 'slv'
    Spanish_Castilian = 'spa'
    Spanish_Castilian_Old = 'spa_old'
    Albanian = 'sqi'
    Serbian = 'srp'
    Serbian_Latin = 'srp_latn'
    Swahili = 'swa'
    Swedish = 'swe'
    Syriac = 'syr'
    Tamil = 'tam'
    Telugu = 'tel'
    Tajik = 'tgk'
    Tagalog = 'tgl'
    Thai = 'tha'
    Tigrinya = 'tir'
    Turkish = 'tur'
    Uighur_Uyghur = 'uig'
    Ukrainian = 'ukr'
    Urdu = 'urd'
    Uzbek = 'uzb'
    Uzbek_Cyrilic = 'uzb_cyrl'
    Vietnamese = 'vie'
    Yiddish = 'yid'
