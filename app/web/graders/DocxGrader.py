from docx import Document


def extract_words_from_docx_file(input_docx_file_path):
    document = Document(input_docx_file_path)
    words_in_doc = []
    total_paragraphs = 0
    for p in document.paragraphs:
        total_paragraphs += 1
        words_in_doc.extend(p.text.split())
        last_item = words_in_doc[-1]
        if "." not in last_item and "!" not in last_item and ":" not in last_item and "?" not in last_item:
            last_item += "."
            words_in_doc.pop()
            words_in_doc.extend([last_item])
    return words_in_doc
