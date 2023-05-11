# this is a script that converts all docx files in a given src_dir to txt files
import os
import docx2txt
import re

def get_files(dir: str):
    files = os.listdir(src_dir)
    files = [f"""{src_dir}/{file}""" for file in files]
    # files = [re.sub(r'\W+', '', filename) for filename in files]
    return files


def convert_docx_to_str(file_path: str):
    if file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
        return text


def write_to_txt(file_path: str, text: str):

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    f.close()

src_dir = "to_process"

files = get_files(src_dir)
print(files)
for file in files:

    if not file.endswith(".docx"):
        continue

    text = convert_docx_to_str(file)
    outfile = file.replace(".docx", ".txt")
    print(text)
    write_to_txt(outfile, text)


