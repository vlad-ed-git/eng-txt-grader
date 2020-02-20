import os
from django.conf import settings
from .graders.grader_constants import *
from .graders import TxtGrader, PdfGrader, DocxGrader
from .utils import DeleteFiles
from django.shortcuts import render
from .forms import WordListsForm, InputTextsForm
from django.conf import settings
from django.http import JsonResponse
from .graders.grading_functions import *
from django.middleware import csrf
from django.http import HttpResponse, Http404


# Create your views here.
def show_home_page(request, input_txts_notification=None, word_lists_notification=None, action_message=None):
    # prep empty forms
    input_txts_form = InputTextsForm()
    word_lists_form = WordListsForm()

    input_texts = os.listdir(os.path.join(settings.MEDIA_ROOT, "input_txts"))

    return render(request, 'web/home.html', {
        'input_texts': input_texts,
        'input_txts_form': input_txts_form,
        'word_lists_form': word_lists_form,
        'input_txts_notification': input_txts_notification,
        'word_lists_notification': word_lists_notification,
        'action_message': action_message
    })


def home(request):
    return show_home_page(request)


def update_word_lists(request):
    word_lists_notification = ""
    if request.method == 'POST':
        word_lists_form = WordListsForm(request.POST, request.FILES)
        if word_lists_form.is_valid():
            word_lists_form.save()
            word_lists_notification = "success"
        else:
            word_lists_notification = "fail"
    return show_home_page(request, word_lists_notification=word_lists_notification)


def update_input_txts(request):
    input_txts_notification = ""
    if request.method == 'POST':
        input_txts_form = InputTextsForm(request.POST, request.FILES)
        if input_txts_form.is_valid():
            input_txts_form.save()
            input_txts_notification = "success"
        else:
            input_txts_notification = "fail"

    return show_home_page(request, input_txts_notification=input_txts_notification)


def show_grader_page(request, input_txt):
    return render(request, 'web/grader.html',
                  {'txt_title': input_txt}
                  )


def show_delete_page(request, input_txt):
    return render(request, 'web/delete.html',
                  {'txt_title': input_txt})


# called when user confirms deletion
def confirmed_delete(request, input_txt):
    success = DeleteFiles.delete_file(file_name_with_ext=input_txt)
    if success:
        action_message = "Successfully Deleted " + input_txt
    else:
        action_message = "Failed to Delete" + input_txt
    return show_home_page(request, action_message=action_message)


def ajax_grader(request):
    input_file_name = request.GET.get('inputTxt', None)
    file_name_components = input_file_name.split('.')
    file_extension = file_name_components[-1].lower().strip()
    file_name_no_ext = file_name_components[0].lower().strip()
    form_crsf_input = getTokenInput(request)
    input_file_path = os.path.join(settings.MEDIA_ROOT, INPUT_TXTS_DIR_NAME, input_file_name)
    if file_extension == "txt":
        words_in_txt = TxtGrader.extract_words_from_txt_file(input_file_path)
        grade_results_html = grade_txt(words_to_grade_as_list=words_in_txt, form_crsf_input=form_crsf_input,
                                       input_file_name_no_ext=file_name_no_ext)
    elif file_extension == "pdf":
        words_in_pdf = PdfGrader.extract_words_from_pdf_file(input_file_path)
        grade_results_html = grade_txt(input_file_name_no_ext=file_name_no_ext, words_to_grade_as_list=words_in_pdf,
                                       form_crsf_input=form_crsf_input)
    elif file_extension == "docx":
        words_in_doc = DocxGrader.extract_words_from_docx_file(input_file_path)
        grade_results_html = grade_txt(input_file_name_no_ext=file_name_no_ext, words_to_grade_as_list=words_in_doc,
                                       form_crsf_input=form_crsf_input)
    else:
        grade_results_html = {}
    return JsonResponse(grade_results_html)


def getTokenInput(request):
    token = csrf.get_token(request)
    token_input_html = '<input type = "hidden" name = "csrfmiddlewaretoken" value = "' + str(token) + '">'
    return token_input_html


def file_downloader(request):
    file_path = request.GET.get('path', None)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
