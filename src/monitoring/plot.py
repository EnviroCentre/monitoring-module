import os
from os import path

def exportImages(config, dssFilePath):
    if path.isabs(config['output_folder']):
        outputFolder = config['output_folder']
        # assume folder exists if absolute path
    else:
        outputFolder = path.join(path.dirname(dssFilePath), config['output_folder'])
        if not path.isdir(outputFolder):
            # create relative folder if required
            os.mkdir(outputFolder)