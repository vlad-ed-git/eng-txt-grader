from django.shortcuts import render
from .forms import WordListsForm


# Create your views here.
def home(request):
    word_lists_form = WordListsForm()
    return render(request, 'web/home.html', {
        'word_lists_form': word_lists_form
    })


def update_word_lists(request):
    word_lists_notification = ""
    if request.method == 'POST':
        word_lists_form = WordListsForm(request.POST, request.FILES)
        if word_lists_form.is_valid():
            word_lists_form.save()
            word_lists_notification = "success"
        else:
            word_lists_notification = "fail"
    else:
        word_lists_form = WordListsForm()
    return render(request, 'web/home.html', {
        'word_lists_form': word_lists_form,
        'word_lists_notification': word_lists_notification,
    })
