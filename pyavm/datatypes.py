from __future__ import print_function, division

try:
    unicode
except:
    basestring = unicode = str

import re
import datetime
import warnings
import xml.etree.ElementTree as et

from .exceptions import AVMItemNotInControlledVocabularyError, AVMListLengthError

__all__ = [
    'AVMString',
    'AVMStringCVCapitalize',
    'AVMStringCVUpper',
    'AVMURL',
    'AVMEmail',
    'AVMLocalizedString',
    'AVMFloat',
    'AVMUnorderedStringList',
    'AVMOrderedList',
    'AVMOrderedListCV',
    'AVMOrderedFloatList',
    'AVMDate',
    'AVMDateTime',
    'AVMDateTimeList',
]


namespaces = {}
namespaces['http://www.communicatingastronomy.org/avm/1.0/'] = 'avm'
namespaces['http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/'] = 'Iptc4xmpCore'
namespaces['http://purl.org/dc/elements/1.1/'] = 'dc'
namespaces['http://ns.adobe.com/photoshop/1.0/'] = 'photoshop'
namespaces['http://ns.adobe.com/xap/1.0/rights/'] = 'xapRights'

reverse_namespaces = {}
for key in namespaces:
    reverse_namespaces[namespaces[key]] = key


class AVMData(object):
    """
    Abstract AVM data class.  All other data classes inherit from AVMData.
    """

    def __init__(self, path, deprecated=False, **kwargs):
        """ """
        self.namespace, self.tag = path.split(':')
        self.deprecated = deprecated

    def check_data(self, value):
        """
        All other data classes should define check_data() based on the type of data.
        Encoding of string into UTF-8 happens here.

        :return: String (UTF-8)
        """
        return value


class AVMString(AVMData):
    """
    Data type for strings
    """

    def check_data(self, value):
        """
        Check that the data is a string or unicode, otherwise it raises a TypeError.

        :return: String (UTF-8)
        """
        if not value:
            return None
        if isinstance(value, (list, tuple)) and len(value) == 1:
            value = value[0]
        if isinstance(value, basestring):
            return value
        elif value is None:
            return None
        else:
            raise TypeError("{0:s} is not a string or unicode".format(self.tag))

    def to_xml(self, parent, value):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))
        element.text = "%s" % value
        return element


class AVMURL(AVMString):
    """
    Data type for URLs.

    :return: String (UTF-8)
    """

    def check_data(self, value):
        """
        Checks the data is a string or unicode, and checks data
        against a regular expression for a URL.  If the user leaves
        off the protocol,then 'http://' is attached as a default.

        :return: String (UTF-8)
        """
        if not value:
            return None

        if not (isinstance(value, basestring)):
            raise TypeError("{0:s} is not a string or unicode".format(self.tag))

        value = value

        if value and '://' not in value:
            value = 'http://%s' % value

        url_re = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9-]+\.)+[A-Z]{2,6}|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|/\S+)$', re.IGNORECASE)

        if not re.search(url_re, value):
            warnings.warn("{0:s} is not a valid URL".format(self.tag))

        return value


class AVMEmail(AVMString):
    """
    Data type for email addresses.

    :return: String (UTF-8)
    """

    def check_data(self, value):
        """
        Checks data is a string or unicode, and checks against a regular expression
        for an email.  If value is not a string or unicode, a TypeError is raised.
        If the value is not a proper email, then a ValueError is raised.

        :return: String (UTF-8)
        """
        if not (isinstance(value, basestring)):
            raise TypeError("{0:s} is not a string or unicode".format(self.tag))

        value = value

        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
            r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE
        )

        if not re.search(email_re, value):
            warnings.warn("{0:s} is not a valid email address".format(self.tag))

        return value


class AVMStringCV(AVMString):
    """ """

    def __init__(self, path, cv, **kwargs):
        self.controlled_vocabulary = cv
        super(AVMStringCV, self).__init__(path, **kwargs)

    def format_data(self, value):
        """
        :return: String
        """
        return value

    def check_cv(self, value):
        """
        If a controlled vocabulary is specified, this function checks the input value against the allowed values.
        AVMItemNotInControlledVocabularyError is raised if not in the controlled vocabulary

        :return: Boolean
        """
        if value in self.controlled_vocabulary:
            return True
        else:
            return False

    def check_data(self, value):
        """
        Check that the data is a string or unicode, formats the data appropriately using format_data()
        and calls check_cv()

        :return: String (UTF-8)
        """
        if not value:
            return None

        if isinstance(value, basestring):
            value = value
            value = self.format_data(value)

            if self.check_cv(value):
                return value
            else:
                raise AVMItemNotInControlledVocabularyError(
                    "Item is not in the controlled vocabulary.")
        else:
            raise TypeError("{0:s} is not a string or unicode".format(self.tag))


class AVMStringCVCapitalize(AVMStringCV):

    def format_data(self, value):
        """
        Formats the data to be a capitalized string

        :return: String
        """
        return value.capitalize()


class AVMStringCVUpper(AVMStringCV):

    def format_data(self, value):
        """
        Formats the data to be an upper case string

        :return: String:
        """
        return value.upper()


class AVMLocalizedString(AVMString):

    def to_xml(self, parent, value):

        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))
        subelement = et.SubElement(element, "rdf:Alt")
        li = et.SubElement(subelement, "rdf:li")
        li.text = "%s" % value
        li.attrib['xml:lang'] = 'x-default'
        return element

# TODO: implement these
AVMDate = AVMString
AVMDateTime = AVMString


class AVMFloat(AVMData):
    """
    Data type for float fields
    """
    def check_data(self, value):
        """
        Checks that data can be represented as a number.

        :return: String (UTF-8)
        """
        if not value:
            return None

        try:
            value = float(value)
        except:
            raise TypeError(
                "Enter a value that can be represented as a number.")

        return value

    def to_xml(self, parent, value):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))
        element.text = "%.16f" % value
        return element


class AVMUnorderedList(AVMData):
    """
    Generic data type for lists (i.e xmp bag arrays)
    """
    def __init__(self, path, **kwargs):
        # Optional keyword arguments
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = False

        if 'strict_length' in kwargs:
            self.strict_length = kwargs['strict_length']
        else:
            self.strict_length = False

        super(AVMUnorderedList, self).__init__(path, **kwargs)

    def check_length(self, values):
        """
        Checks the length of the Python List.

        :return: Boolean
        """
        if self.strict_length:
            if len(values) is self.length:
                return True
            else:
                return False
        elif self.length:
            if len(values) <= self.length:
                return True
            else:
                return False
        else:
            return True

    def check_data(self, values):
        """
        Checks that the data type is a Python List.  Calls check_length() first.

        .. todo :: Redo this function.  Implement the dash functionality only for ordered lists.

        :return: List (UTF-8 elements)
        """
        if not values:
            return None
        # Check data type
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")

        # Check if all are None
        if all([v is None for v in values]):
            return None

        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")

        # Convert to UTF-8
        checked_data = []
        length = 0

        for value in values:
            value = value
            length += len(value)
            if value == "":
                value = "-"
            checked_data.append(value)

        if len(set(checked_data)) == 1 and checked_data[0] == "-":
            checked_data = []

        return checked_data

    def to_xml(self, parent, values):

        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))

        subelement = et.SubElement(element, "rdf:Bag")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if type(item) is float:
                li.text = "%.16f" % item
            else:
                li.text = "%s" % item

        return element


class AVMUnorderedStringList(AVMUnorderedList):
    """
    Data type for an unordered list of strings
    """

    def check_data(self, values):
        """
        Check that the passed data is a Python List, and checks that the elements
        are strings or unicode.

        :return: List of strings (UTF-8)
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")

        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")

        checked_data = []
        # Check data type in list
        for value in values:
            if (isinstance(value, basestring)):
                value = value
                checked_data.append(value)
            else:
                raise TypeError(
                    "Elements of list need to be string or unicode.")

        return checked_data

    def to_xml(self, parent, values):

        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))

        subelement = et.SubElement(element, "rdf:Bag")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            li.text = "%s" % item

        return element


class AVMOrderedList(AVMUnorderedList):
    """
    Data type for ordered lists (i.e. seq arrays)
    """
    def to_xml(self, parent, values):

        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))

        subelement = et.SubElement(element, "rdf:Seq")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if type(item) is float:
                li.text = "%.16f" % item
            else:
                li.text = "%s" % item

        return element


class AVMOrderedListCV(AVMOrderedList, AVMStringCVCapitalize):
    """
    Data type for an ordered list constrained to a controlled vocabulary.
    """
    def __init__(self, path, cv, deprecated=False, **kwargs):

        self.namespace, self.tag = path.split(':')
        self.deprecated = deprecated
        self.controlled_vocabulary = cv

        # Optional keyword arguments
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = False

        if 'strict_length' in kwargs:
            self.strict_length = kwargs['strict_length']
        else:
            self.strict_length = False

    def check_data(self, values):
        """
        Checks that the data is a list, elements are strings, and strings are in the specified controlled vocabulary.

        :return: List of CV-Strings (UTF-8)
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")

        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("List is not the correct length.")

        checked_data = []
        # Check data type in list
        for value in values:
            if (isinstance(value, basestring)):
                value = value
                value = self.format_data(value)

                if self.check_cv(value):
                    checked_data.append(value)
                else:
                    raise AVMItemNotInControlledVocabularyError(
                        "Item is not in the controlled vocabulary.")
            else:
                if value is None:
                    checked_data.append("-")
                else:
                    raise TypeError(
                        "Elements of list need to be string or unicode.")

        if len(set(checked_data)) == 1 and checked_data[0] == "-":
            checked_data = []

        return checked_data


class AVMOrderedFloatList(AVMOrderedList):
    """
    Data type for ordered lists of floats.
    """
    def check_data(self, values):
        """
        Checks that the data is of the correct type, length and elements
        are strings able to be represented as floats.

        :return: List of strings (UTF-8)
        """
        checked_data = []

        if values:
            # Check type for list
            if not isinstance(values, list):
                raise TypeError("Data needs to be a list.")

            # Check length
            if not self.check_length(values):
                raise AVMListLengthError("Data is not the correct length.")

            # Check data type in list
            for value in values:
                if value.strip() == '-':
                    checked_data.append(None)
                else:
                    value = value
                    try:
                        checked_data.append(float(value))
                    except Exception:
                        raise TypeError("Enter a string that can be represented as a number.")

            if len(set(checked_data)) == 1 and checked_data[0] == "-":
                checked_data = []

        return checked_data

    def to_xml(self, parent, values):

        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, "{%s}%s" % (uri, self.tag))

        subelement = et.SubElement(element, "rdf:Bag")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if item is None:
                li.text = '-'
            else:
                li.text = "%.16f" % item

        return element


class AVMDateTimeList(AVMOrderedList):
    """
    Data type for lists composed of DateTime objects
    """
    def check_data(self, values):
        """
        Checks that the data passed is a Python List,
        and that the elements are Date or Datetime objects.

        :return: List of Datetime objects in ISO format (i.e. Strings encoded as UTF-8)
        """
        if not isinstance(values, list):
            raise TypeError("Data needs to be a list.")

        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")

        checked_data = []
        # Check data type in list
        for value in values:
            if value:
                if (isinstance(value, datetime.date) or isinstance(value, datetime.datetime)):
                    value = value.isoformat()
                    checked_data.append(value)
                elif isinstance(value, basestring):
                    value = value
                    checked_data.append(value)
                else:
                    raise TypeError("Elements of the list need to be a Python Date or Datetime object.")
            else:
                checked_data.append("-")

        if len(set(checked_data)) == 1 and checked_data[0] == "-":
            checked_data = []

        return checked_data
