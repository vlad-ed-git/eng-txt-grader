from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .utilities.AppConstants import USER_GROUP_WRITERS, USER_GROUP_LEVELERS, INPUT_TXTS_DIR_NAME, OUTPUT_TXTS_DIR_NAME
from .graders import TxtGrader, PdfGrader, DocxGrader
from .utilities import DeleteFiles
from .forms import InputTextsForm
from .models import InputTexts
from django.shortcuts import render
from django.http import JsonResponse
from .graders.grading_functions import *
from django.middleware import csrf
from django.http import HttpResponse, Http404


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return show_logged_in_home_page(request)
    sample_input_txt = "the_clever_fox.txt"
    return render(request, 'web_app/home.html', {'sample_input_txt': sample_input_txt})


def sign_in(request):
    if request.method == "POST" and 'sign_in_btn' in request.POST:
        try:
            username = request.POST['user_name']
            password = request.POST['user_password']
            old_user = authenticate(request, username=username, password=password)
            if old_user is not None:
                login(request, old_user)  # login this user
                return show_logged_in_home_page(request)
            else:
                sign_in_error = "Login failed! Please check your username & password."
                return render(request, 'web_app/home.html', {'sign_in_error': sign_in_error})
        except Exception as e:
            print(e)
            sign_in_error = "An unknown error occurred! Try again"
            return render(request, 'web_app/home.html', {'sign_in_error': sign_in_error})
    else:
        return sign_out(request)


""" LOGIN REQUIRED """


@login_required
def show_logged_in_home_page(request, input_txts_notification=None, action_message=None):
    user_group = get_user_group(request.user)
    if user_group is None:
        logout(request)
        sign_in_error = "Logged Out! Your access rights are still under review."
        return render(request, 'web_app/home.html', {'sign_in_error': sign_in_error})
    else:
        # prep empty forms
        input_txts_form = InputTextsForm(initial={'created_by': request.user})

        input_texts = None
        if user_group == USER_GROUP_WRITERS:
            input_texts_by_user = InputTexts.objects.filter(created_by=request.user).values_list('input_txts',
                                                                                                 flat=True).order_by(
                '-uploaded_at')
            remove_first_chars = len(INPUT_TXTS_DIR_NAME + '/')
            input_texts = []
            for input_txt in input_texts_by_user:
                input_texts.append(input_txt[remove_first_chars:])
            if len(input_texts) == 0:
                input_texts = "Empty"

        elif user_group == USER_GROUP_LEVELERS:
            all_input_texts = InputTexts.objects.all().order_by('-uploaded_at')
            remove_first_chars = len(INPUT_TXTS_DIR_NAME + '/')
            input_texts = []
            for uploaded_docs in all_input_texts:
                input_txt = str(uploaded_docs.input_txts)
                input_texts.append(input_txt[remove_first_chars:])
        return render(request, 'web_app/logged_in_home_page.html',
                      {
                          'user': request.user,
                          'user_group': user_group.capitalize(),
                          'input_texts': input_texts,
                          'input_txts_form': input_txts_form,
                          'input_txts_notification': input_txts_notification,
                          'action_message': action_message
                      })


def get_user_group(user):
    if is_leveler(user):
        return USER_GROUP_LEVELERS
    elif is_writer(user):
        return USER_GROUP_WRITERS
    else:
        return None


def is_leveler(user):
    return user.groups.filter(name=USER_GROUP_LEVELERS).exists()


def is_writer(user):
    return user.groups.filter(name=USER_GROUP_WRITERS).exists()


@login_required
def sign_out(request):
    logout(request)
    return home(request)


@login_required
def update_input_txts(request):
    notification = None
    if is_writer(request.user):
        if request.method == 'POST':
            post = request.POST.copy()
            post['created_by'] = request.user
            input_txts_form = InputTextsForm(post, request.FILES)
            if input_txts_form.is_valid():
                input_txts_form.save()
                notification = "success"
            else:
                print(input_txts_form.errors)
                notification = "fail"

        return show_logged_in_home_page(request, input_txts_notification=notification)

    else:
        notification = "Permissions denied!"
        return show_logged_in_home_page(request, input_txts_notification=notification)


@login_required
def show_delete_page(request, input_txt):
    user_group = get_user_group(request.user)
    return render(request, 'web_app/delete.html',
                  {'txt_title': input_txt,
                   'user_group': user_group.capitalize()})


# called when user confirms deletion
@login_required
def confirmed_delete(request, input_txt):
    input_txt_object = INPUT_TXTS_DIR_NAME + '/' + input_txt
    InputTexts.objects.filter(created_by=request.user, input_txts=input_txt_object).delete()
    success = DeleteFiles.delete_file(file_name_with_ext=input_txt)
    if success:
        action_message = "Successfully Deleted " + input_txt
    else:
        action_message = "Failed to Delete " + input_txt
    return show_logged_in_home_page(request, action_message=action_message)


"""" GRADING """


def show_grader_page(request, input_txt):
    user_group = get_user_group(request.user)
    if user_group is None:
        user_group = "Guests"
    return render(request, 'web_app/grader.html',
                  {'txt_title': input_txt,
                   'user_group': user_group.capitalize()}
                  )


def ajax_grader(request):
    input_file_name = request.GET.get('inputTxt', None)
    file_name_components = input_file_name.split('.')
    file_extension = file_name_components[-1].lower().strip()
    file_name_no_ext = file_name_components[0].lower().strip()
    form_crsf_input = get_token(request)
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


def get_token(request):
    token = csrf.get_token(request)
    token_input_html = '<input type = "hidden" name = "csrfmiddlewaretoken" value = "' + str(token) + '">'
    return token_input_html


def file_downloader(request):
    file_path = request.POST['path']
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404