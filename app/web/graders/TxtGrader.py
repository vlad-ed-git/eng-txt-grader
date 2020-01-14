import os
from django.conf import settings


class TxtGrader:
    def __init__(self, input_txt):
        self.input_file_path = os.path.join(settings.MEDIA_ROOT) + "/input_txts/" + input_txt
        # read all words from the input text
        input_txt_f = open(self.input_file_path, "r")
        self.words_in_txt = [word for line in input_txt_f for word in line.split()]
        input_txt_f.close()
