from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph


def extract_words_from_docx_file(input_docx_file_path):
    document = Document(input_docx_file_path)
    words_in_doc = []
    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            words_in_doc.extend(block.text.split())
            last_item = words_in_doc[-1]
            if "." not in last_item and "!" not in last_item and ":" not in last_item and "?" not in last_item:
                last_item += "."
                words_in_doc.pop()
                words_in_doc.extend([last_item])
        elif isinstance(block, Table):
            for row in block.rows:
                row_data = []
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        row_data.append(paragraph.text)
                table_data = "\t".join(row_data)
                words_in_doc.extend([table_data])
    return words_in_doc


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)
