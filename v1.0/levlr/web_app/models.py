from django.db import models
import os
from django.core.files.storage import FileSystemStorage
from .utilities.AppConstants import INPUT_TXTS_DIR_NAME, WORD_LISTS_TXTS_DIR_NAME
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


# Create your models here.
class WordLists(models.Model):
    updated_by = models.OneToOneField(User, on_delete=models.CASCADE)
    word_list_dir = WORD_LISTS_TXTS_DIR_NAME + '/'
    word_lists = models.FileField(max_length=15, storage=OverwriteStorage(), upload_to=word_list_dir)
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=WordLists)
def submission_delete(sender, instance, **kwargs):
    instance.word_lists.delete(False)


class InputTexts(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    graded_txts_dir = INPUT_TXTS_DIR_NAME + '/'
    input_txts = models.FileField(upload_to=graded_txts_dir, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
