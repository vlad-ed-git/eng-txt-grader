import os
from django.conf import settings


def delete_file(file_name_with_ext):
    try:
        input_file_path = os.path.join(settings.MEDIA_ROOT) + "/input_txts/" + file_name_with_ext
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
        return True
    except:
        return False
