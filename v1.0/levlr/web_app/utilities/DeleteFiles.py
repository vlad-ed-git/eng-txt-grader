import os
from django.conf import settings
from .AppConstants import INPUT_TXTS_DIR_NAME


def delete_file(file_name_with_ext):
    try:
        input_file_path = os.path.join(settings.MEDIA_ROOT, INPUT_TXTS_DIR_NAME , file_name_with_ext)
        print(input_file_path)
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
