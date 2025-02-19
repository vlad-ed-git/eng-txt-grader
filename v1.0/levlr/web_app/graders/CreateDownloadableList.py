from pandas import DataFrame
import os
from django.conf import settings
from docx import Document
from web_app.utilities.AppConstants import *


def get_download_links(input_file_name_no_ext, words_per_grade, unique_words, form_crsf_input):
    html_form = '<div class="paragraph_font">'
    counter = 0
    try:
        for key, item in words_per_grade.items():
            counter += 1
            file_name = input_file_name_no_ext + "_" + key + "_words.csv"
            df = DataFrame(sorted(item))
            file_path = os.path.join(settings.MEDIA_ROOT, OUTPUT_TXTS_DIR_NAME, file_name.replace(" ", "_"))
            df.to_csv(file_path, index=None, header=True)
            html_form += get_html_download_form(form_crsf_input, file_path, file_name)

        # for all words
        df2 = DataFrame(sorted(unique_words))
        unique_words_file_name = input_file_name_no_ext + "_all_unique_words.csv"
        unique_words_file_path = os.path.join(
            settings.MEDIA_ROOT, OUTPUT_TXTS_DIR_NAME, unique_words_file_name)
        df2.to_csv(unique_words_file_path, index=None, header=True)
        html_form += get_html_download_form(form_crsf_input, unique_words_file_path, unique_words_file_name)

    except Exception as e:
        print(e)
        html_form += "<span class='red_bg_img_color'>Ooops! Failed to extract words for download!</span>"
    html_form += "</div>"
    return html_form


def get_html_download_form(form_crsf_input, file_path, file_name):
    html_form = '<form action="/file_downloader/" method ="POST" ><div class="form-group">'
    html_form += form_crsf_input + '</div><div class="form-group">'
    html_form += '<input type = "hidden" name = "path" value = "' + str(file_path) + '"></div>'
    html_form += '<button type="submit" class="downloadBtn standard_header">' \
                 + file_name + '</button></form>'
    return html_form


# todo implement this method?
def get_formatted_txt_download_link(input_file_name_no_ext, graded_words, form_csrf_input):
    document = Document()
    document.add_heading('Color Grades', level=2)
    document_file_path = os.path.join(
        settings.MEDIA_ROOT, OUTPUT_TXTS_DIR_NAME, ("graded_" + input_file_name_no_ext.replace(" ", "_") + ".docx"))
    document.save(document_file_path)
    html_form = '<div>' + get_html_download_form(form_csrf_input, document_file_path, input_file_name_no_ext) + '</div>'
    return html_form
