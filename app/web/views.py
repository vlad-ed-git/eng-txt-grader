from django.shortcuts import render
from .forms import WordListsForm, InputTextsForm
from django.conf import settings
import os


# Create your views here.
def show_home_page(request, input_txts_notification=None, word_lists_notification=None):
    # prep empty forms
    input_txts_form = InputTextsForm()
    word_lists_form = WordListsForm()

    input_texts = os.listdir(os.path.join(settings.MEDIA_ROOT) + "/input_txts/")

    return render(request, 'web/home.html', {
        'input_texts': input_texts,
        'input_txts_form': input_txts_form,
        'word_lists_form': word_lists_form,
        'input_txts_notification': input_txts_notification,
        'word_lists_notification': word_lists_notification
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


def grader(request, input_txt):
    # todo os.listdir(os.path.join(settings.MEDIA_ROOT) + "/input_txts/")
    return render(request, 'web/grader.html',
                  {'txt_title': input_txt}
                  )
