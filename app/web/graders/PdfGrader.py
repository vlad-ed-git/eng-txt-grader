import os
from django.conf import settings
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_to_text(path, page_nums):
    res_mgr = PDFResourceManager()
    str_io = StringIO()
    codec = 'utf-8'
    l_a_params = LAParams()
    device = TextConverter(res_mgr, str_io, codec=codec, laparams=l_a_params)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(res_mgr, device)
    password = ""
    max_pages = 0
    caching = True

    for page in PDFPage.get_pages(fp, page_nums, maxpages=max_pages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = str_io.getvalue()

    fp.close()
    device.close()
    str_io.close()
    return text


class PdfGrader:
    def __init__(self, input_pdf, page_nums_as_list ):
        self.input_file_path = os.path.join(settings.MEDIA_ROOT) + "/input_txts/" + input_pdf
        # read all words from the input pdf
        self.pdf_text = convert_to_text(path=self.input_file_path, page_nums = page_nums_as_list )
        self.words_in_page = self.pdf_text.split()

