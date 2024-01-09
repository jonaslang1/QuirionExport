"""Build executable using py2exe"""

import os
import shutil
import py2exe

folder = './dist'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

py2exe.freeze(console=[{'script': 'main.py'}], options={'py2exe': {'bundle_files': 1, 'compressed': True}})
