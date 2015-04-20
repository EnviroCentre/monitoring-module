import os
from os import path

def relativeFolder(folder, dssFilePath, createFolder='ifrelative'):
    """
    Return an absolute path to :arg:`folder` relative to :arg:`dssFilePath`.
    
    If the path :arg:`folder` is already absolute, it will simply return the path. :arg:`createFolder` is one of
    'ifrelative', 'ifabsolute' or 'allways'.
    """
    if path.isabs(folder):
        absPath = folder
        if not path.isdir(absPath) and createFolder.lower() in ['allways', 'ifabsolute']:
            os.mkdir(absPath)
    else:
        absPath = path.join(path.dirname(dssFilePath), folder)
        if not path.isdir(absPath) and createFolder.lower() in ['allways', 'ifrelative']:
            os.mkdir(absPath)
    return absPath
