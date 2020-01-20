import math
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from django.conf import settings
from .CreateDownloadableList import getDownloadableList


def get_avg_in_dictionary(dictionary_obj):
    index = 0
    total = 0
    for key, item in dictionary_obj.items():
        total += item
        index = key
    if index == 0:
        return 0
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
    color_guide = ''
    for grade_index, grade in enumerate(grades):
        color_guide = color_guide + '<span id="gradeColor' + str(grade_index) + '" class="gradeBtns gradeColorBg' + str(
            grade_index) + '">' + grade + '</span>   '
    color_guide = color_guide + '   <span id="gradeColorBlack" class="gradeBtns gradeColorBlackBg"> *Not Graded</span>'
    return color_guide


def begin_grading(og_file_name, words_to_grade, output_html_header="<p class='font-weight-bolder'>",
                  form_crsf_input=None, page_num = None):
    word_lists_file_path = os.path.join(settings.MEDIA_ROOT) + "/word_lists/word_lists.xlsx"
    word_list_file = pd.read_excel(word_lists_file_path, sheet_name=None)
    grades = word_list_file.keys()

    color_guide = prepare_guide(grades)
    # prepare output texts
    output_html = output_html_header

    words_counter = 0
    total_sentences = 0
    words_per_sentence = {total_sentences: 0}
    commas_per_sentence = {total_sentences: 0}
    special_words = {'for': 0, 'and': 0, 'not': 0, 'but': 0, 'so': 0, 'or': 0}
    special_words_result = ""
    words_per_grade = {'Not Graded': set()}
    unique_words = set()
    for word_to_grade in words_to_grade:
        word_in_txt = word_to_grade.strip()
        lower_stripped_word = word_in_txt.lower().strip()
        word_only_alpha = "".join([c if c.isalpha() else "" for c in lower_stripped_word])
        if len(word_only_alpha) == 1:
            words_per_sentence[total_sentences] += 1
            words_counter += 1
            unique_words.add(word_only_alpha)
            words_per_grade['Not Graded'].add(word_only_alpha)
        elif len(word_only_alpha) > 1:
            words_per_sentence[total_sentences] += 1
            words_counter += 1
            unique_words.add(word_only_alpha)
            words_per_grade['Not Graded'].add(word_only_alpha)

        graded_txt = ' <span class="gradeColorBlack">' + word_in_txt + '</span>'

        already_graded = False
        for grade_index, grade in enumerate(grades):
            if already_graded:
                break
            for col_name in word_list_file[grade]:
                grade_words = word_list_file[grade][col_name]
                for grade_word in grade_words:
                    if word_only_alpha == grade_word.lower().strip():
                        # grade the found word
                        graded_txt = ' <span class="gradeColor' + str(
                            grade_index) + '">' + word_in_txt + '</span>'
                        try:
                            words_per_grade['Not Graded'].remove(word_only_alpha)
                        except KeyError:
                            pass
                        try:
                            words_per_grade[grade].add(word_only_alpha)
                        except KeyError:
                            words_per_grade[grade] = set()
                            words_per_grade[grade].add(word_only_alpha)
                        already_graded = True

        if "." in word_in_txt or "!" in word_in_txt or ":" in word_in_txt or "?" in word_in_txt:
            graded_txt += "<br><span class='badge badge-info'>" + str(
                words_per_sentence[total_sentences]) + " words " + str(
                commas_per_sentence[total_sentences]) + " commas</span><br><br>"
            total_sentences += 1
            words_per_sentence[total_sentences] = 0
            commas_per_sentence[total_sentences] = 0

        if "," in word_in_txt:
            commas_per_sentence[total_sentences] += 1

        special_words_result = ""
        for key in special_words:
            word_to_check = word_in_txt.lower()
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
    grading_results = "<p class='text-monospace' >Total Word Count: <span class='badge badge-primary'>" + str(
        words_counter) + "</span></p>"
    grading_results += "<p class='text-monospace' >Unique Words Count: <span class='badge badge-primary'>" + str(
        len(unique_words)) + "</span></p>"
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
        grading_results += "<br><span class='badge badge-primary'> " + str(len(item)) + " " + key + " words</span>"
    grading_results += "</p>"

    """
    grade = get_max_val_key_in_dictionary(words_per_grade)
    grading_results += "<p class='font-weight-bold' >Final Grade:<br><span class='badge badge-warning'> " + str(
        grade) + "</span></p>"
    """
    grading_results += "<p>Available Downloads : </p>" + getDownloadableList(og_file_name, words_per_grade,
                                                                             form_crsf_input, page_num)
    return {'color_guide': color_guide, 'graded_txt': output_html,
            'grading_results': grading_results}
