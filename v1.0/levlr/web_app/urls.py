from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# register namespace
app_name = 'web_app'
urlpatterns = [
    path('', views.home, name="home"),
    path('sign_in/', views.sign_in, name="login"),
    path('user_home/', views.show_logged_in_home_page, name="user_home"),
    path('user_home/logout/', views.sign_out, name="log_out"),
    path('user_home/update_input_txts', views.update_input_txts, name="upload_doc"),
    path('grader/<str:input_txt>/', views.show_grader_page, name="grade_doc"),
    path('user_home/delete/<str:input_txt>/', views.show_delete_page, name="delete_doc"),
    path('user_home/confirmed_delete/<str:input_txt>/', views.confirmed_delete, name="delete_confirmation"),
    path('ajax_grader/', views.ajax_grader, name="ajax_grader"),
    path('file_downloader/', views.file_downloader, name="download_doc")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

