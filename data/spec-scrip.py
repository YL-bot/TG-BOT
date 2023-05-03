import re

# "C:/Users/sorok/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytube/cipher.py"

with open('Python/Python39/Lib/site-packages/pytube/cipher.py', 'r') as file:
    filedata = file.read()

    filedata = filedata.replace('transform_plan_raw = find_object_from_startpoint(raw_code, match.span()[1] - 1)',
                                'transform_plan_raw = js')

with open("Python/Python39/Lib/site-packages/pytube/cipher.py", 'w') as file:
    file.write(filedata)

filedata
