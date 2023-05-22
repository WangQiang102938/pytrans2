from typing import *
from PIL.Image import Image
from pypdfium2 import PdfDocument


def load_local_pdf(path:str, progress_call: Callable[[int, int], None], scale=5):
    try:
        rendered_pages = list[Image]()
        pdf = PdfDocument(path)
        page_count = len(pdf)
        for index in range(page_count):
            progress_call(index, page_count)
            page = pdf.get_page(index)
            rendered_pages.append(page.render(scale=scale).to_pil())
            progress_call(index + 1, page_count)
        return rendered_pages
    except Exception:
        return None
