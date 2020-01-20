import os
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

    input_texts = os.listdir(os.path.join(settings.MEDIA_ROOT) + "/input_txts/")

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
    input_txt = request.GET.get('inputTxt', None)
    file_name = input_txt.split('.')
    input_ext = file_name[-1].lower().strip()
    file_name_no_ext = file_name[0].lower().strip()
    form_crsf_input = getTokenInput(request)
    if input_ext == "txt":
        grader_obj = TxtGrader.TxtGrader(input_txt)
        data = begin_grading(og_file_name=file_name_no_ext, words_to_grade=grader_obj.words_in_txt,
                             form_crsf_input=form_crsf_input)
    elif input_ext == "pdf":
        page_num = 0
        output_html_header = generateHeaderWithJumpToPage(request, query=input_txt, current_page=(page_num + 1))
        grader_obj = PdfGrader.PdfGrader(input_txt, page_nums_as_list=[0])
        data = begin_grading(og_file_name=file_name_no_ext, words_to_grade=grader_obj.words_in_page,
                             output_html_header=output_html_header, form_crsf_input=form_crsf_input, page_num=page_num)
    elif input_ext == "docx":
        grader_obj = DocxGrader.DocxGrader(input_txt)
        data = begin_grading(og_file_name=file_name_no_ext, words_to_grade=grader_obj.words_in_doc,
                             form_crsf_input=form_crsf_input)
    else:
        data = {}
    return JsonResponse(data)


def ajax_page_grader(request):
    input_txt = request.GET.get("input_txt", None)
    page_num = request.GET.get("page_number", None)
    file_name = input_txt.split('.')
    input_ext = file_name[-1].lower().strip()
    file_name_no_ext = file_name[0].lower().strip()
    form_crsf_input = getTokenInput(request)
    if page_num.isnumeric():
        page_as_num = int(page_num.strip())
        if input_ext == "pdf":
            output_html_header = generateHeaderWithJumpToPage(request, query=input_txt, current_page=page_as_num)
            grader_obj = PdfGrader.PdfGrader(input_txt, page_nums_as_list=[page_as_num - 1])
            data = begin_grading(og_file_name=file_name_no_ext, words_to_grade=grader_obj.words_in_page,
                                 output_html_header=output_html_header, form_crsf_input=form_crsf_input,
                                 page_num=page_num)
        else:
            data = {}
    else:
        output_html_header = generateHeaderWithJumpToPage(request, query=input_txt, current_page=0)
        data = {"graded_txt": output_html_header}
    return JsonResponse(data)


def getTokenInput(request):
    token = csrf.get_token(request)
    token_input_html = '<input type = "hidden" name = "csrfmiddlewaretoken" value = "' + str(token) + '">'
    return token_input_html


def generateHeaderWithJumpToPage(request, query, current_page):
    return '<kbd>Now Showing Page ' + str(current_page) + '</kbd><form class="form-inline" ' + getTokenInput(
        request) + '<input type="hidden" id="input_txt" name="input_txt" value="' + str(
        query) + '"><label class="sr-only" ' \
                 'for="page_number">Name</label><input type="text" class="form-control mb-2 mr-sm-2" id="page_number" ' \
                 'name="page_number" placeholder="Enter Page No." required><button id="jump_to_page_btn" ' \
                 'type="button" class="btn btn-primary mb-2">Jump To Page</button></form><br><p class="font-weight-bolder">'


def file_downloader(request):
    file_path = request.GET.get('path', None)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
