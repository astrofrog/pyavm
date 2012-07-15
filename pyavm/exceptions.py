# -*- coding: utf-8 -*-


class AVMListLengthError(Exception):
    """ Raised when a list is not the correct length """
    pass


class AVMItemNotInControlledVocabularyError(Exception):
    """ Raise when an string is not in a required controlled vocabulary """
    pass


class AVMEmptyValueError(Exception):
    """ Raise when a list is given with no relevant data """
    pass
