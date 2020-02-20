from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def extract_words_from_pdf_file(input_pdf_file_path):
    pdf_text = grab_txt_from_pdf(input_file_path=input_pdf_file_path)
    return pdf_text.split()


def grab_txt_from_pdf(input_file_path, page_nums_as_list=None):
    res_mgr = PDFResourceManager()
    str_io = StringIO()
    codec = 'utf-8'
    l_a_params = LAParams()
    device = TextConverter(res_mgr, str_io, codec=codec, laparams=l_a_params)
    fp = open(input_file_path, 'rb')
    interpreter = PDFPageInterpreter(res_mgr, device)
    password = ""
    max_pages = 0
    caching = True

    for page in PDFPage.get_pages(fp, page_nums_as_list, maxpages=max_pages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = str_io.getvalue()

    fp.close()
    device.close()
    str_io.close()

    return text
