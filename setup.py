"""Build executable using py2exe"""

import os
import shutil
import py2exe

FOLDER = './dist'
for filename in os.listdir(FOLDER):
    file_path = os.path.join(FOLDER, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except (FileExistsError,  FileNotFoundError) as e:
        print(f'Failed to delete {file_path}. Reason: {e}')

py2exe.freeze(console=[{'script': 'src/main.py'}],
              options={'py2exe': {'bundle_files': 1, 'compressed': True}})
