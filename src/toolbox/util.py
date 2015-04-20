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


class ValidationError(Exception):
    """
    An error while validating data.
    
    Based django.core.exceptions.ValidationError
    Copyright (c) Django Software Foundation and individual contributors. All rights reserved.
    """
    
    def __init__(self, message):
        """
        The :arg:`message` argument can be a single error, a list of errors. What we define as an "error" can be either 
        a simple string or an instance of ValidationError with its message attribute set, and what we define as
        list can be an actual `list` or an instance of ValidationError with its `error_list` attribute set.
        """

        if isinstance(message, ValidationError):
            message = message.message
        
        elif isinstance(message, list):
            self.error_list = []
            for message in message:
                if not isinstance(message, ValidationError):
                    message = ValidationError(message)
                self.error_list.extend(message.error_list)
        
        else:
            self.message = message
            self.error_list = [self]
            
    def __str__(self):
        message = ""
        for error in self.error_list:
            message += "ValidationError(%s)\n" % error.message
        return message
