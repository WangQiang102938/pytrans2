from enum import Enum
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

from controller.pipeline.pipeline_hub import PipelineHub, PipelineNode
from model.capture.capture_node import CaptureNode
import utils.pipeline_utils as pipeline_utils
import utils
import pytesseract


class TesseractOCR(PipelineNode):
    name="Tesseract OCR"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)
        self.widget = TesseractWidget().bind()

    def get_title(self):
        return "Tesseract OCR"

    def option_ui_setup(self, container: QWidget) -> QWidget:
        container_layout = QHBoxLayout(container) if container.layout()==None else container.layout()
        container_layout.setContentsMargins(2, 2, 2, 2)
        container_layout.addWidget(self.widget)
        container.setVisible(True)
        container.show()

    def process_node(self, node: CaptureNode, dfs_mode=False, update_flag=False):
        if node.node_type() != node.node_type().TEXT and node.get_visual_memo() != None:
            return
        if self.widget.realtime_check.checkState()==Qt.CheckState.Unchecked and update_flag:
            return
        visual_memo = node.get_visual_memo()
        img = node.working_doc.page_cache[visual_memo.page_no]
        node_rect = utils.preview_utils.map_rect_from_ratio(
            QRectF(visual_memo.left, visual_memo.top,
                   visual_memo.right, visual_memo.bottom),
            QRectF(0, 0, img.size[0], img.size[1])
        )
        node_img = img.crop(
            (node_rect.left(), node_rect.top(), node_rect.width(), node_rect.height()))
        lang_combo = self.widget.lang_select_combo
        ocr_result = pytesseract.image_to_string(
            node_img, lang=lang_combo.currentData())
        print(ocr_result)
        return super().process_node(node, dfs_mode)


class TesseractWidget(QFrame):
    def bind(self):
        self.main_layout = QVBoxLayout(self)

        self.realtime_check = QCheckBox(self)
        self.realtime_checkF = pipeline_utils.FormItem(self).setup(
            'Realtime Update', self.realtime_check
        )

        self.lang_select_combo = QComboBox(self)
        self.lang_select_conboF = pipeline_utils.FormItem(self).setup(
            "OCR Lang", self.lang_select_combo
        )

        for enum in TesseractLangEnum:
            self.lang_select_combo.addItem(enum.name, enum.value)
        self.lang_select_combo.setCurrentText(TesseractLangEnum.English.name)

        self.main_layout.addWidget(self.realtime_checkF)
        self.main_layout.addWidget(self.lang_select_conboF)
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
