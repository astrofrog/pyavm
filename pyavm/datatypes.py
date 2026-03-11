import datetime
import re
import warnings
import xml.etree.ElementTree as et

from .exceptions import AVMItemNotInControlledVocabularyError, AVMListLengthError

__all__ = [
    "AVMString",
    "AVMStringCVCapitalize",
    "AVMStringCVUpper",
    "AVMURL",
    "AVMEmail",
    "AVMLocalizedString",
    "AVMFloat",
    "AVMUnorderedStringList",
    "AVMOrderedList",
    "AVMOrderedListCV",
    "AVMOrderedFloatList",
    "AVMDate",
    "AVMDateTime",
    "AVMDateTimeList",
]


namespaces = {
    "http://www.communicatingastronomy.org/avm/1.0/": "avm",
    "http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/": "Iptc4xmpCore",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://ns.adobe.com/photoshop/1.0/": "photoshop",
    "http://ns.adobe.com/xap/1.0/rights/": "xapRights",
}

reverse_namespaces = {v: k for k, v in namespaces.items()}


class AVMData:
    """
    Abstract AVM data class.  All other data classes inherit from AVMData.
    """

    def __init__(self, path, deprecated=False, **kwargs):
        """ """
        self.namespace, self.tag = path.split(":")
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
        if isinstance(value, str):
            return value
        elif value is None:
            return None
        else:
            raise TypeError(f"{self.tag:s} is not a string or unicode")

    def to_xml(self, parent, value):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")
        element.text = f"{value}"
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

        if not isinstance(value, str):
            raise TypeError(f"{self.tag:s} is not a string or unicode")

        if value and "://" not in value:
            value = f"http://{value}"

        url_re = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9-]+\.)+[A-Z]{2,6}|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|/\S+)$",
            re.IGNORECASE,
        )

        if not re.search(url_re, value):
            warnings.warn(f"{self.tag:s} is not a valid URL")

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
        if not isinstance(value, str):
            raise TypeError(f"{self.tag:s} is not a string or unicode")

        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
            r")@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$",
            re.IGNORECASE,
        )

        if not re.search(email_re, value):
            warnings.warn(f"{self.tag:s} is not a valid email address")

        return value


class AVMStringCV(AVMString):
    """ """

    def __init__(self, path, cv, **kwargs):
        self.controlled_vocabulary = cv
        super().__init__(path, **kwargs)

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
        return value in self.controlled_vocabulary

    def check_data(self, value):
        """
        Check that the data is a string or unicode, formats the data appropriately using format_data()
        and calls check_cv()

        :return: String (UTF-8)
        """
        if not value:
            return None

        if isinstance(value, str):
            value = self.format_data(value)

            if self.check_cv(value):
                return value
            else:
                raise AVMItemNotInControlledVocabularyError(
                    "Item is not in the controlled vocabulary."
                )
        else:
            raise TypeError(f"{self.tag:s} is not a string or unicode")


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
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")
        subelement = et.SubElement(element, "rdf:Alt")
        li = et.SubElement(subelement, "rdf:li")
        li.text = f"{value}"
        li.attrib["xml:lang"] = "x-default"
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
        except (ValueError, TypeError):
            raise TypeError("Enter a value that can be represented as a number.")

        return value

    def to_xml(self, parent, value):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")
        element.text = f"{value:.16f}"
        return element


class AVMUnorderedList(AVMData):
    """
    Generic data type for lists (i.e xmp bag arrays)
    """

    def __init__(self, path, **kwargs):
        self.length = kwargs.get("length", False)
        self.strict_length = kwargs.get("strict_length", False)
        super().__init__(path, **kwargs)

    def check_length(self, values):
        """
        Checks the length of the Python List.

        :return: Boolean
        """
        if self.strict_length:
            return len(values) == self.length
        elif self.length:
            return len(values) <= self.length
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
        if all(v is None for v in values):
            return None

        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")

        # Convert to UTF-8
        checked_data = ["-" if v == "" else v for v in values]

        if len(set(checked_data)) == 1 and checked_data[0] == "-":
            checked_data = []

        return checked_data

    def to_xml(self, parent, values):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")

        subelement = et.SubElement(element, "rdf:Bag")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if isinstance(item, float):
                li.text = f"{item:.16f}"
            else:
                li.text = f"{item}"

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

        # Check data type in list
        for value in values:
            if not isinstance(value, str):
                raise TypeError("Elements of list need to be string or unicode.")

        return list(values)

    def to_xml(self, parent, values):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")

        subelement = et.SubElement(element, "rdf:Bag")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            li.text = f"{item}"

        return element


class AVMOrderedList(AVMUnorderedList):
    """
    Data type for ordered lists (i.e. seq arrays)
    """

    def to_xml(self, parent, values):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")

        subelement = et.SubElement(element, "rdf:Seq")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if isinstance(item, float):
                li.text = f"{item:.16f}"
            else:
                li.text = f"{item}"

        return element


class AVMOrderedListCV(AVMOrderedList, AVMStringCVCapitalize):
    """
    Data type for an ordered list constrained to a controlled vocabulary.
    """

    def __init__(self, path, cv, deprecated=False, **kwargs):
        self.namespace, self.tag = path.split(":")
        self.deprecated = deprecated
        self.controlled_vocabulary = cv
        self.length = kwargs.get("length", False)
        self.strict_length = kwargs.get("strict_length", False)

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
            if isinstance(value, str):
                value = self.format_data(value)

                if self.check_cv(value):
                    checked_data.append(value)
                else:
                    raise AVMItemNotInControlledVocabularyError(
                        "Item is not in the controlled vocabulary."
                    )
            else:
                if value is None:
                    checked_data.append("-")
                else:
                    raise TypeError("Elements of list need to be string or unicode.")

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
                if value.strip() == "-":
                    checked_data.append(None)
                else:
                    try:
                        checked_data.append(float(value))
                    except (ValueError, TypeError):
                        raise TypeError("Enter a string that can be represented as a number.")

            if len(set(checked_data)) == 1 and checked_data[0] == "-":
                checked_data = []

        return checked_data

    def to_xml(self, parent, values):
        uri = reverse_namespaces[self.namespace]
        element = et.SubElement(parent, f"{{{uri}}}{self.tag}")

        subelement = et.SubElement(element, "rdf:Seq")

        for item in values:
            li = et.SubElement(subelement, "rdf:li")
            if item is None:
                li.text = "-"
            else:
                li.text = f"{item:.16f}"

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
                if isinstance(value, datetime.date):
                    # datetime.datetime is a subclass of datetime.date
                    checked_data.append(value.isoformat())
                elif isinstance(value, str):
                    checked_data.append(value)
                else:
                    raise TypeError(
                        "Elements of the list need to be a Python Date or Datetime object."
                    )
            else:
                checked_data.append("-")

        if len(set(checked_data)) == 1 and checked_data[0] == "-":
            checked_data = []

        return checked_data
