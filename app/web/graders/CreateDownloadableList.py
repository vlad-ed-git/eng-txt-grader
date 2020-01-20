from pandas import DataFrame
import os
from django.conf import settings


def getDownloadableList(og_file_name, words_list, form_crsf_input, page_num = None):
    html_links = '<div>'
    counter = 0

    if page_num is not None:
        og_file_name += "_page_" + str(page_num).replace(" ", "")
    try:
        for key, item in words_list.items():
            counter += 1
            file_name = og_file_name + "_" + key + "_words.csv"
            df = DataFrame(list(item))
            file_path = os.path.join(settings.MEDIA_ROOT) + "/output_txts/" + file_name.replace(" ", "_")
            df.to_csv(file_path, index=None,
                      header=True)
            html_links += '<form action="/home/file_downloader/" method ="get" ><div class="form-group">'
            html_links += form_crsf_input + '</div><div class="form-group">'
            html_links += '<input type = "hidden" name = "path" value = "' + str(file_path) + '"></div>'
            html_links += '<button type="submit" class="btn btn-primary btn-sm downloadBtns">' + file_name + '</button></form>'

    except:
        html_links += "Ooops! Failed to extract words for download!"
    html_links += "</div>"
    return html_links
