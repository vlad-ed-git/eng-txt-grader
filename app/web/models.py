from django.db import models
import os
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        self.delete(name)
        return name


# Create your models here.
class WordLists(models.Model):
    word_lists = models.FileField(max_length=15, storage=OverwriteStorage(), upload_to='word_lists/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class InputTexts(models.Model):
    input_txts = models.FileField(storage=OverwriteStorage(), upload_to='input_txts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


def image_path(instance):
    return os.path.join('some_dir', str(instance.some_identifier), 'filename.ext')
