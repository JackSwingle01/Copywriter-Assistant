# delete all docx files in the directory provided by argument

import os
import sys

dir = sys.argv[1]

files = os.listdir(dir)

for file in files:

    if file.endswith(".docx"):
        os.remove(file)

print("done")
