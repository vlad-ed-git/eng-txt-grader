import os
import math
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from django.conf import settings


def get_avg_in_dictionary(dictionary_obj):
    index = 0
    total = 0
    for key, item in dictionary_obj.items():
        total += item
        index = key
    return math.floor(total / index)


def get_max_in_dictionary(dictionary_obj):
    max_value = 0
    for key, item in dictionary_obj.items():
        if item > max_value:
            max_value = item
    return max_value


def get_max_val_key_in_dictionary(dictionary_obj):
    max_value = 0
    key_value = "*Not Graded"
    for key, item in dictionary_obj.items():
        if item > max_value:
            max_value = item
            key_value = key
    return key_value


def get_min_in_dictionary(dictionary_obj):
    min_value = 0
    index = 0
    for key, item in dictionary_obj.items():
        if index == 0:
            min_value = item
        elif item < min_value and item != 0:
            min_value = item
        index += 1
    return min_value


def prepare_guide(grades):
    color_guide = ""
    for grade_index, grade in enumerate(grades):
        color_guide = color_guide + '<span class="gradeColorBg' + str(grade_index) + '";>' + grade + '</span>   '
    color_guide = color_guide + '   <span class="gradeColorBlack";> *Not Graded</span>'
    return color_guide


class TxtGrader:
    def __init__(self, input_txt):
        self.input_file = input_txt
        self.input_file_path = os.path.join(settings.MEDIA_ROOT) + "/input_txts/" + self.input_file
        self.word_lists_file_path = os.path.join(settings.MEDIA_ROOT) + "/word_lists/word_lists.xlsx"
        self.word_list_file = pd.read_excel(self.word_lists_file_path, sheet_name=None)
        self.grades = self.word_list_file.keys()

    def begin_grading(self):
        color_guide = prepare_guide(self.grades)

        # read all words from the input text
        input_txt_f = open(self.input_file_path, "r")
        words_in_txt = [word for line in input_txt_f for word in line.split()]
        input_txt_f.close()

        # prepare output texts
        output_html = "<p class='font-weight-bolder'>"

        words_counter = 0
        total_sentences = 0
        words_per_sentence = {total_sentences: 0}
        commas_per_sentence = {total_sentences: 0}
        special_words = {'for': 0, 'and': 0, 'not': 0, 'but': 0, 'so': 0, 'or': 0}
        special_words_result = ""
        words_per_grade = {}
        for word_in_txt in words_in_txt:
            if len(word_in_txt) == 1 and (word_in_txt.isalpha() or word_in_txt.isdigit()):
                words_per_sentence[total_sentences] += 1
                words_counter += 1
            elif len(word_in_txt) > 1:
                words_per_sentence[total_sentences] += 1
                words_counter += 1

            graded_txt = ' <span class="black";>' + word_in_txt + '</span>'

            already_graded = False
            for grade_index, grade in enumerate(self.grades):
                if already_graded:
                    break
                for col_name in self.word_list_file[grade]:
                    grade_words = self.word_list_file[grade][col_name]
                    for grade_word in grade_words:
                        if word_in_txt.lower().strip() == grade_word.lower().strip():
                            # grade the found word
                            graded_txt = ' <span class="gradeColor' + str(
                                grade_index) + '">' + word_in_txt + '</span>'
                            try:
                                words_per_grade[grade] += 1
                            except KeyError:
                                words_per_grade[grade] = 1
                            already_graded = True

            if "." in word_in_txt:
                graded_txt += "  <span class='badge badge-info'>" + str(
                    words_per_sentence[total_sentences]) + " words " + str(
                    commas_per_sentence[total_sentences]) + " commas</span><br>"
                total_sentences += 1
                words_per_sentence[total_sentences] = 0
                commas_per_sentence[total_sentences] = 0

            if "," in word_in_txt:
                commas_per_sentence[total_sentences] += 1

            special_words_result = ""
            for key in special_words:
                word_to_check = word_in_txt.lower().strip()
                letters_in_word = ''.join(ch for ch in word_to_check if ch.isalpha())
                if key == letters_in_word:
                    special_words[key] = special_words[key] + 1
                special_words_result += "<br><span class='badge badge-primary'> " + str(
                    special_words[key]) + " " + key + "</span>"

            output_html += graded_txt + ""

        output_html += "</p>"
        avg_words_per_sentence = get_avg_in_dictionary(words_per_sentence)
        max_words_in_sentence = get_max_in_dictionary(words_per_sentence)
        min_words_in_sentence = get_min_in_dictionary(words_per_sentence)
        grading_results = "<p class='text-monospace' >Words: <span class='badge badge-primary'>" + str(
            words_counter) + "</span></p>"
        grading_results += "<p class='text-monospace' >Sentences: <span class='badge badge-primary'>" + str(
            total_sentences) + "</span></p>"
        grading_results += "<p class='text-monospace' >Average number of words per sentence: <span class='badge " \
                           "badge-primary'>" + str(avg_words_per_sentence) + "</span></p>"
        grading_results += "<p class='text-monospace' >Longest sentence: <span class='badge badge-primary'>" + str(
            max_words_in_sentence) + " Words</span></p>"
        grading_results += "<p class='text-monospace' >Shortest sentence: <span class='badge badge-primary'>" + str(
            min_words_in_sentence) + " Words</span></p>"
        grading_results += "<p class='text-monospace' >Special words count : " + special_words_result + "</p>"

        grading_results += "<p class='text-monospace' >Grades: "
        for key, item in words_per_grade.items():
            grading_results += "<br><span class='badge badge-primary'> " + str(item) + " " + key + " words</span>"
        grading_results += "</p>"

        grade = get_max_val_key_in_dictionary(words_per_grade)
        grading_results += "<p class='font-weight-bold' >Final Grade:<br><span class='badge badge-warning'> " + str(
            grade) + "</span></p>"

        return {'color_guide': color_guide, 'graded_txt': output_html,
                'grading_results': grading_results}
