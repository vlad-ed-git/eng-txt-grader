import math
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from django.conf import settings
from .CreateDownloadableList import get_download_links
from .grader_constants import *


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


def prepare_legend(grades, special_words):
    color_guide = '<p>'
    for grade_index, grade in enumerate(grades):
        color_guide += '<span id="gradedWordsColor' + str(
            grade_index) + '" class="gradeBtns gradedWordsColorBg' + str(
            grade_index) + '">' + grade + '</span>   '
    color_guide += '   <span id="nonGradedWordsColor" class="gradeBtns nonGradedWordsColorBg"> *Not Graded</span></p>'

    special_words_guide = '<p class="text-monospace"> Specials : '
    for special_word in special_words:
        special_words_guide = special_words_guide + '<kbd>' + str(special_word) + '</kbd> '
    special_words_guide += '</p>'
    return color_guide + special_words_guide


def grade_txt(words_to_grade_as_list, form_crsf_input, input_file_name_no_ext):
    special_words = {'for': 0, 'and': 0, 'not': 0, 'but': 0, 'so': 0, 'or': 0}
    unique_words = set()
    total_word_count = 0
    total_sentences = 0
    words_per_sentence = {total_sentences: 0}
    commas_per_sentence = {total_sentences: 0}
    special_words_per_sentence = {total_sentences: 0}
    words_per_grade = {'Not Graded': set()}

    # get the grades
    word_lists_file_path = os.path.join(
        settings.MEDIA_ROOT) + "/" + WORD_LISTS_TXTS_DIR_NAME + "/" + WORD_LISTS_FILE_NAME
    word_list_file = pd.read_excel(word_lists_file_path, sheet_name=None)
    grades = word_list_file.keys()

    # prepare the legend that explains color codes
    legend = prepare_legend(grades, special_words)

    # prepare output texts
    output_html = "<p class = 'font-weight-bold' "
    special_words_html_output = ""

    for word_to_grade in words_to_grade_as_list:
        # start the graded text
        graded_txt = ' <span class="nonGradedWordsColor">' + word_to_grade + '</span>'

        # check the word
        lower_stripped_word = word_to_grade.lower().strip()
        true_word_only_letters = "".join([c if c.isalpha() else "" for c in lower_stripped_word])
        if len(true_word_only_letters) >= 1:
            words_per_sentence[total_sentences] += 1
            total_word_count += 1
            unique_words.add(true_word_only_letters)
            words_per_grade['Not Graded'].add(true_word_only_letters)

            if "," in true_word_only_letters:
                commas_per_sentence[total_sentences] += 1

            # count special words per sentence
            special_words_html_output = ""
            for special_word in special_words:
                if special_word == true_word_only_letters:
                    special_words_per_sentence[total_sentences] += 1
                    special_words[true_word_only_letters] = special_words[true_word_only_letters] + 1
                    special_words_html_output += "<br><span class='badge badge-primary'> " + str(
                        special_words[special_word]) + " " + special_word + "</span>"

            already_graded = False
            for grade_index, grade in enumerate(grades):
                if already_graded:
                    break
                for col_name in word_list_file[grade]:
                    grade_words = word_list_file[grade][col_name]
                    for grade_word in grade_words:
                        if true_word_only_letters == grade_word.lower().strip():
                            # grade the found word
                            graded_txt = ' <span class="gradedWordsColor' + str(
                                grade_index) + '">' + word_to_grade + '</span>'
                            try:
                                words_per_grade['Not Graded'].remove(true_word_only_letters)
                            except KeyError:
                                # no word to remove
                                pass
                            try:
                                words_per_grade[grade].add(true_word_only_letters)
                            except KeyError:
                                words_per_grade[grade] = set()
                                words_per_grade[grade].add(true_word_only_letters)
                            already_graded = True

        # check for end of sentence
        if "." in word_to_grade or "!" in word_to_grade or ":" in word_to_grade or "?" in word_to_grade:
            graded_txt += "<br><span class='badge badge-info'>" + str(
                words_per_sentence[total_sentences]) + " words " + str(
                commas_per_sentence[total_sentences]) + " commas " + str(
                special_words_per_sentence[total_sentences]) + " specials</span><br><br>"
            total_sentences += 1
            special_words_per_sentence[total_sentences] = 0
            words_per_sentence[total_sentences] = 0
            commas_per_sentence[total_sentences] = 0

        output_html += graded_txt + ""

    output_html += "</p>"
    avg_words_per_sentence = get_avg_in_dictionary(words_per_sentence)
    max_words_in_sentence = get_max_in_dictionary(words_per_sentence)
    min_words_in_sentence = get_min_in_dictionary(words_per_sentence)
    grading_output_html = "<p class='text-monospace' >Total Word Count: <span class='badge badge-primary'>" + str(
        total_word_count) + "</span></p>"
    grading_output_html += "<p class='text-monospace' >Unique Words Count: <span class='badge badge-primary'>" + str(
        len(unique_words)) + "</span></p>"
    grading_output_html += "<p class='text-monospace' >Sentences: <span class='badge badge-primary'>" + str(
        total_sentences) + "</span></p>"
    grading_output_html += "<p class='text-monospace' >Average number of words per sentence: <span class='badge " \
                           "badge-primary'>" + str(avg_words_per_sentence) + "</span></p>"
    grading_output_html += "<p class='text-monospace' >Longest sentence: <span class='badge badge-primary'>" + str(
        max_words_in_sentence) + " Words</span></p>"
    grading_output_html += "<p class='text-monospace' >Shortest sentence: <span class='badge badge-primary'>" + str(
        min_words_in_sentence) + " Words</span></p>"
    grading_output_html += "<p class='text-monospace' >Special words count : " + special_words_html_output + "</p>"

    grading_output_html += "<p class='text-monospace' >Grades: "
    for key, item in words_per_grade.items():
        grading_output_html += "<br><span class='badge badge-primary'> " + str(len(item)) + " " + key + " words</span>"
    grading_output_html += "</p>"

    """
       grade = get_max_val_key_in_dictionary(words_per_grade)
       grading_output_html += "<p class='font-weight-bold' >Final Grade:<br><span class='badge badge-warning'> " + str(
           grade) + "</span></p>"
       """
    grading_output_html += "<p>Available Downloads : </p>" + get_download_links(input_file_name_no_ext,
                                                                                words_per_grade,
                                                                                unique_words,
                                                                                form_crsf_input)
    return {'color_guide': legend, 'graded_txt': output_html,
            'grading_output_html': grading_output_html}
