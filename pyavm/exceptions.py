# -*- coding: utf-8 -*-

from __future__ import print_function, division


class AVMListLengthError(Exception):
    """
    Raised when a list is not the correct length
    """
    pass


class AVMItemNotInControlledVocabularyError(Exception):
    """
    Raised when an string is not in a required controlled vocabulary
    """
    pass


class AVMEmptyValueError(Exception):
    """
    Raised when a list is given with no relevant data
    """
    pass


class NoXMPPacketFound(Exception):
    """
    Raised when no XMP packet is found in a file
    """
    pass
