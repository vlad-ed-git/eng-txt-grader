import os
from django.conf import settings
from docx import Document


class DocxGrader:
    def __init__(self, input_txt):
        self.input_file_path = os.path.join(settings.MEDIA_ROOT) + "/input_txts/" + input_txt
        # read all words from the input text
        document = Document(self.input_file_path)
        self.words_in_doc = []
        total_paragraphs = 0
        for p in document.paragraphs:
            total_paragraphs += 1
            self.words_in_doc.extend(p.text.split())
            last_item = self.words_in_doc[-1]
            if "." not in last_item and "!" not in last_item and ":" not in last_item and "?" not in last_item:
                last_item += "."
                self.words_in_doc.pop()
                self.words_in_doc.extend([last_item])
