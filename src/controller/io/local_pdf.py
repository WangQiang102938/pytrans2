from pypdfium2 import PdfDocument
from model.doc import WorkingDoc
from controller.io.io_hub import OpenModule

import pypdfium2


class LocalPDFOpener(OpenModule):
    def __init__(self, path, scale=5) -> None:
        self.path = path
        self.scale = scale

    def open(self) -> WorkingDoc:
        try:
            pdf = PdfDocument(self.path)
            tmp_doc = WorkingDoc(path=self.path)
            pdf_page_count = len(pdf)
            renderer = pdf.render(
                pypdfium2.PdfBitmap.to_pil,
                page_indices=list(range(len(pdf))),
                scale=300/72.0
            )
            for image in renderer:
                tmp_doc.page_cache.append(image)
            # for i in range(pdf_page_count):
            #     tmp_doc.page_cache.append(
            #         pdf[i].render_topil(scale=self.scale)
            #     )
            tmp_doc.page_no = 0
            tmp_doc.status = tmp_doc.STATUS.NORMAL
            return tmp_doc
        except Exception:
            return super().open()
