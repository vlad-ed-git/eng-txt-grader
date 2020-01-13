from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# register namespace
app_name = 'web'
urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('home/update_word_lists', views.update_word_lists, name="updateWordLists"),
    path('home/update_input_txts', views.update_input_txts, name="updateInputTxts"),
    path('home/grader/<str:input_txt>/', views.grader, name="gradeTxt"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)