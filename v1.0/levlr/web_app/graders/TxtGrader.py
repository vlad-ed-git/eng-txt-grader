

def extract_words_from_txt_file(input_txt_file_path):
    input_txt_file = open(input_txt_file_path, "r", errors='ignore')
    words_in_txt = [word for line in input_txt_file for word in line.split()]
    input_txt_file.close()
    return words_in_txt
