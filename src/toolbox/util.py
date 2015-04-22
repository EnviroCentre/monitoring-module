# -*- coding: utf-8 -*-

import os
from os import path


def relativeFolder(folder, dssFilePath, createFolder='ifrelative'):
    """
    Return an absolute path to ``folder`` relative to ``dssFilePath``.
    
    If the path ``folder`` is already absolute, it will simply return the path. ``createFolder`` is one of
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
    
    Based on :class:`django.core.exceptions.ValidationError`. Copyright © Django Software Foundation and individual 
    contributors. All rights reserved.
    """
    
    def __init__(self, message):
        """
        The ``message`` argument can be a single error, a list of errors. What we define as an "error" can be either 
        a simple string or an instance of ValidationError with its message attribute set, and what we define as
        list can be an actual `list` or an instance of :class:`ValidationError` with its :attr:`.error_list`` attribute
        set.
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
            
    def __getitem__(self, index):
        return self.error_list[index]
            
    def __str__(self):
        return repr(list(self))

    def __repr__(self):
        return "ValidationError(%r)" % self.message
    
