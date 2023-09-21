# PyAVM - Simple pure-python AVM meta-data handling
# Copyright (c) 2011-13 Thomas P. Robitaille
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function, division

try:
    unicode
except:
    basestring = unicode = str

import warnings
from io import BytesIO
import xml.etree.ElementTree as et

from .specs import SPECS, REVERSE_SPECS
from .wcs_utils import get_cdelt_crota, get_cd


def register_namespace(tag, uri):
    try:
        et.register_namespace(tag, uri)
    except:
        et._namespace_map[uri] = tag

try:
    from astropy.wcs import WCS
    from astropy.io import fits
    astropy_installed = True
except ImportError:
    astropy_installed = False


class NoSpatialInformation(Exception):
    pass


from .embed import embed_xmp
from .extract import extract_xmp

# Define namespace to tag mapping

namespaces = {}
namespaces['http://www.communicatingastronomy.org/avm/1.0/'] = 'avm'
namespaces['http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/'] = 'Iptc4xmpCore'
namespaces['http://purl.org/dc/elements/1.1/'] = 'dc'
namespaces['http://ns.adobe.com/photoshop/1.0/'] = 'photoshop'
namespaces['http://ns.adobe.com/xap/1.0/rights/'] = 'xapRights'

reverse_namespaces = {}
for key in namespaces:
    reverse_namespaces[namespaces[key]] = key


class NoAVMPresent(Exception):
    pass


def capitalize(string):
    return string[0].upper() + string[1:]


def utf8(value):
    return unicode(value).encode('utf-8')


def decode_ascii(string):
    try:
        return string.decode('ascii')
    except AttributeError:  # already a string
        return string


def auto_type(string):
    """
    Try and convert a string to an integer or float
    """
    try:
        return int(string)
    except:
        try:
            return float(string)
        except:
            return string


class AVMContainer(object):

    def __init__(self, allow_value=False):
        if allow_value:
            self.value = None
        self._items = {}

    def __str__(self, indent=0):

        string = ""
        for family in self._items:

            if family.startswith('_'):
                continue

            if type(self._items[family]) is AVMContainer:
                substring = self._items[family].__str__(indent + 3)
                if substring != "":
                    if hasattr(self._items[family], 'value'):
                        string += indent * " " + "%s: %s\n" % (family, utf8(self._items[family].value))
                    else:
                        string += indent * " " + "%s:\n" % family
                    string += substring
            else:
                if type(self._items[family]) is list:
                    string += indent * " " + "%s:\n" % family
                    for elem in self._items[family]:
                        if elem is not None:
                            string += indent * " " + "   * %s\n" % utf8(elem)
                else:
                    if self._items[family] is not None:
                        string += indent * " " + \
                            "%s: %s\n" % (family, utf8(self._items[family]))

        return string

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, attribute, value):
        if attribute in ['_items', 'value']:
            object.__setattr__(self, attribute, value)
            return
        if attribute not in self._items:
            raise Exception("%s is not a valid AVM tag" % attribute)
        else:
            self._items[attribute] = value

    def __getattr__(self, attribute):
        if attribute in self._items:
            return self._items[attribute]
        else:
            return object.__getattr__(self, attribute)


def parse_avm_content(rdf):

    avm_content = {}

    for item in rdf.attrib:

        # Find URI
        uri, tag = item[1:].split('}')

        if uri in namespaces:
            avm_content[(namespaces[uri], tag)] = rdf.attrib[item]

    for item in rdf:

        # Find URI
        uri, tag = item.tag[1:].split('}')

        if uri == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#':
            sub_avm_content = parse_avm_content(item)
            for key in sub_avm_content:
                avm_content[key] = sub_avm_content[key]
        elif uri in namespaces:
            if len(item) == 0:
                avm_content[(namespaces[uri], tag)] = item.text
            elif len(item) == 1:
                c_uri, c_tag = item[0].tag[1:].split('}')
                if c_uri == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' and c_tag in ['Bag', 'Seq', 'Alt']:
                    avm_content[(namespaces[uri], tag)] = [x.text for x in item[0]]
                else:
                    raise Exception("Unexpected tag %s:%s" % (c_uri, c_tag))
            elif len(item) > 1:
                sub_avm_content = parse_avm_content(item)
                for key in sub_avm_content:
                    avm_content[key] = sub_avm_content[key]

    return avm_content


class AVM(AVMContainer):
    """
    There are several ways to initialize an AVM object:

    * Initialize an empty AVM object:

        >>> avm = AVM()

    * Parse AVM meta-data from an existing image:

        >>> avm = AVM.from_image('myexample.jpg')

    * Create an AVM object from a FITS header:

        >>> from astropy.io import fits
        >>> header = fits.getheader('image.fits')
        >>> avm = AVM.from_header(header)

    * Create an AVM meta-data object from an Astropy WCS instance:

        >>> from astropy.wcs import WCS
        >>> from pyavm import AVM
        >>> wcs = WCS('image.fits')
        >>> avm = AVM.from_wcs(wcs)

    View the contents of the AVM object:

        >>> print(avm)

    The AVM meta-data can be accessed using the attribute notation:

        >>> avm.Spatial.Equinox
        'J2000'
        >>> avm.Publisher
        'Chandra X-ray Observatory'

    Tags can be modified:

        >>> avm.Spatial.Equinox = "B1950"
        >>> avm.Spatial.Notes = "The WCS information was updated on 04/02/2010"

    Finally, it is possible to embed AVM meta-data into an image file:

        >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

    At this time, only JPG and PNG files are supported.
    """

    def __init__(self, origin=None, version=1.2):

        self._items = {}

        self.MetadataVersion = version

        self._update_attributes()

    def _update_attributes(self):

        # Remove attributes that are no longer in the specs

        remove_base = []
        for avm_name in self._items:
            item = self._items[avm_name]
            if isinstance(item, AVMContainer):
                remove_sub = []
                for avm_subset in item._items:
                    full_name = '{0}.{1}'.format(avm_name, avm_subset)
                    if not full_name in self._specs:
                        if item._items[avm_subset] is not None:
                            warnings.warn("{0} is not defined in format specification {1} and will be deleted".format(full_name, self.MetadataVersion))
                        remove_sub.append(avm_subset)
                for key in remove_sub:
                    item._items.pop(key)
            else:
                if not avm_name in self._specs:
                    if self._items[avm_name] is not None:
                        warnings.warn("{0} is not defined in format specification {1} and will be deleted".format(avm_name, self.MetadataVersion))
                    remove_base.append(avm_name)
        for key in remove_base:
            self._items.pop(key)

        # Add any missing ones

        # First pass for root-level attributes, second pass for nested ones
        for iteration in range(2):
            for avm_name in self._specs:

                if avm_name == "MetadataVersion":
                    continue

                if "Distance" in avm_name:
                    if not "Distance" in self._items:
                        self._items['Distance'] = AVMContainer(allow_value=True)

                if iteration == 0 and not '.' in avm_name:

                    if avm_name not in self._items:
                        if "Distance" in avm_name:
                            self._items[avm_name] = AVMContainer(allow_value=True)
                        else:
                            self._items[avm_name] = None

                elif iteration == 1 and '.' in avm_name:

                    family, key = avm_name.split('.')
                    if not family in self._items:
                        self._items[family] = AVMContainer()
                    if not key in self._items[family]._items:
                        self._items[family]._items[key] = None

    def __dir__(self):
        attributes = []
        for key in self._items:
            if '.' in key:
                attribute = key.split('.')[0]
            else:
                attribute = key
            if not attribute in attributes:
                attributes.append(attribute)
        return attributes

    @property
    def _specs(self):
        return SPECS[self.MetadataVersion]

    @property
    def _reverse_specs(self):
        return REVERSE_SPECS[self.MetadataVersion]

    @property
    def MetadataVersion(self):
        if 'MetadataVersion' in self._items:
            return self._items['MetadataVersion']
        else:
            return None

    @MetadataVersion.setter
    def MetadataVersion(self, value):
        self._items['MetadataVersion'] = value
        self._update_attributes()

    def __setattr__(self, attribute, value):

        if attribute in ['_items', 'MetadataVersion']:
            object.__setattr__(self, attribute, value)
            return

        if attribute not in self._specs:
            raise AttributeError("{0} is not a valid AVM group or tag in the {1} standard".format(attribute, self.MetadataVersion))

        avm_class = self._specs[attribute]
        value = avm_class.check_data(value)

        if attribute in self._items and isinstance(self._items[attribute], AVMContainer):
            if hasattr(self._items[attribute], "value"):
                self._items[attribute].value = value
            else:
                raise AttributeError("{0} is an AVM group, not a tag".format(attribute))
        else:
            self._items[attribute] = value

    def __getattr__(self, attribute):
        if attribute in self._items:
            return self._items[attribute]
        else:
            return object.__getattr__(self, attribute)

    @classmethod
    def from_image(cls, filename, xmp_packet_index=None):
        """
        Instantiate an AVM object from an existing image.

        Parameters
        ----------
        filename : str
            The filename of the image to read the AVM meta-data from
        xmp_packet_index : int, optional
            In cases where multiple XMP packets are present in the file, this
            can be used to indicate which one to use. If not specified, this
            defaults to the first XMP packet found.
        """

        # Get XMP data from file
        xmp = extract_xmp(filename, xmp_packet_index=xmp_packet_index)

        # Extract XML
        start = xmp.index(b"<?xpacket begin=")
        start = xmp.index(b"?>", start) + 2
        end = xmp.index(b"</x:xmpmeta>") + 12

        # Extract XML
        xml = xmp[start:end]
        return cls.from_xml(xml)

    @classmethod
    def from_xml_file(cls, filename):
        """
        Instantiate an AVM object from an xml file.
        """
        with open(filename, 'rb') as f:
            return cls.from_xml(f.read())

    @classmethod
    def from_xml(cls, xml):
        """
        Instantiate an AVM object from an XML string
        """

        self = cls()

        # Parse XML
        tree = et.parse(BytesIO(xml))
        root = tree.getroot()
        avm_content = parse_avm_content(root)

        for tag, name in avm_content:

            content = avm_content[(tag, name)]

            if (tag, name) in self._reverse_specs:

                avm_name = self._reverse_specs[tag, name]

                # Add to AVM dictionary
                avm_class = self._specs[avm_name]
                content = avm_class.check_data(content)
                if "." in avm_name:
                    family, key = avm_name.split('.')
                    self._items[family]._items[key] = content
                else:
                    if hasattr(self._items[avm_name], 'value'):
                        self._items[avm_name].value = content
                    else:
                        self._items[avm_name] = content

        return self

    def to_wcs(self, use_full_header=False, target_image=None, target_shape=None):
        """
        Convert AVM projection information into a Astropy WCS object.

        Parameters
        ----------
        use_full_header : bool, optional
            Whether to use the full embedded Header if available. If set to
            `False`, the WCS is determined from the regular AVM keywords.
        target_image : str, optional
            In some cases, the dimensions of the image containing the AVM/WCS
            information is different from the dimensions of the image for which
            the AVM was defined. The `target_image` option can be used to pass
            the path of an image from which the size will be used to re-scale
            the WCS.
        target_shape : tuple of ``(nx: int, ny: int)``, optional
            Serves the same function as `target_image`, but for cases where the
            target dimensions are known without having to open and read an image
            file. If both this and `target_image` are specified, `target_image`
            takes precedence.
        """

        if not astropy_installed:
            raise Exception("Astropy is required to use to_wcs()")

        if repr(self.Spatial) == '':
            raise NoSpatialInformation("AVM meta-data does not contain any spatial information")

        if use_full_header and self.Spatial.FITSheader is not None:
            header = fits.Header.from_string(self.Spatial.FITSheader)
            return WCS(header)

        # Initializing WCS object
        wcs = WCS(naxis=2)

        # Find the coordinate type
        if self.Spatial.CoordinateFrame is not None:
            ctype = self.Spatial.CoordinateFrame
        else:
            warnings.warn("Spatial.CoordinateFrame not found, assuming ICRS")
            ctype = 'ICRS'

        if ctype in ['ICRS', 'FK5', 'FK4']:
            xcoord = "RA--"
            ycoord = "DEC-"
            wcs.wcs.radesys = ctype.encode('ascii')
        elif ctype in ['ECL']:
            xcoord = "ELON"
            ycoord = "ELAT"
        elif ctype in ['GAL']:
            xcoord = "GLON"
            ycoord = "GLAT"
        elif ctype in ['SGAL']:
            xcoord = "SLON"
            ycoord = "SLAT"
        else:
            raise Exception("Unknown coordinate system: %s" % ctype)

        # Find the projection type
        cproj = ('%+4s' % self.Spatial.CoordsystemProjection).replace(' ', '-')

        wcs.wcs.ctype[0] = (xcoord + cproj).encode('ascii')
        wcs.wcs.ctype[1] = (ycoord + cproj).encode('ascii')

        # Find the equinox
        if self.Spatial.Equinox is None:
            warnings.warn("Spatial.Equinox is not present, assuming 2000")
            wcs.wcs.equinox = 2000.
        elif type(self.Spatial.Equinox) is str:
            if self.Spatial.Equinox == "J2000":
                wcs.wcs.equinox = 2000.
            elif self.Spatial.Equinox == "B1950":
                wcs.wcs.equinox = 1950.
            else:
                try:
                    wcs.wcs.equinox = float(self.Spatial.Equinox)
                except ValueError:
                    raise ValueError("Unknown equinox: %s" % self.Spatial.Equinox)
        else:
            wcs.wcs.equinox = float(self.Spatial.Equinox)

        # Set standard WCS parameters
        if self.Spatial.ReferenceDimension is not None:
            wcs_naxis1, wcs_naxis2 = self.Spatial.ReferenceDimension
            if hasattr(wcs, 'naxis1'):  # PyWCS and Astropy < 0.4
                wcs.naxis1, wcs.naxis2 = wcs_naxis1, wcs_naxis2
        else:
            wcs_naxis1, wcs_naxis2 = None, None

        wcs.wcs.crval = self.Spatial.ReferenceValue
        wcs.wcs.crpix = self.Spatial.ReferencePixel

        if self.Spatial.CDMatrix is not None:
            wcs.wcs.cd = [self.Spatial.CDMatrix[0:2],
                          self.Spatial.CDMatrix[2:4]]
        elif self.Spatial.Scale is not None:
            # AVM Standard 1.2:
            #
            # "The scale should follow the standard FITS convention for sky
            # projections in which the first element is negative (indicating
            # increasing RA/longitude to the left) and the second is positive.
            # In practice, only the absolute value of the first term should be
            # necessary to identify the pixel scale since images should always
            # be presented in an undistorted 1:1 aspect ratio as they appear in
            # the sky when viewed from Earth.This field can be populated from
            # the FITS keywords: CDELT1, CDELT2 (or derived from CD matrix)."
            #
            # Therefore, we have to enforce the sign of CDELT:
            wcs.wcs.cdelt[0] = - abs(self.Spatial.Scale[0])
            wcs.wcs.cdelt[1] = + abs(self.Spatial.Scale[1])
            if self.Spatial.Rotation is not None:
                wcs.wcs.crota = self.Spatial.Rotation, self.Spatial.Rotation

        # If `target_image` is set, we have to rescale the reference pixel and
        # the scale
        if target_image is not None:
            from PIL import Image
            target_shape = Image.open(target_image).size

        if target_shape is not None:
            if self.Spatial.ReferenceDimension is None:
                raise ValueError("Spatial.ReferenceDimension should be set in order to determine scale in target image")

            # Find scale in x and y
            scale_x = target_shape[0] / float(wcs_naxis1)
            scale_y = target_shape[1] / float(wcs_naxis2)

            # Check that scales are consistent
            if abs(scale_x - scale_y) / (scale_x + scale_y) * 2. < 0.01:
                scale = scale_x
            else:
                raise ValueError("Cannot scale WCS to target image consistently in x and y direction")

            wcs.wcs.cdelt /= scale
            wcs.wcs.crpix *= scale

            if hasattr(wcs, 'naxis1'):  # PyWCS and Astropy < 0.4
                wcs.naxis1 = target_shape[0]
                wcs.naxis2 = target_shape[1]

        return wcs

    @classmethod
    def from_header(cls, header, include_full_header=True):
        """
        Instantiate an AVM object from a FITS header
        """

        if not astropy_installed:
            raise Exception("Astropy is required to use from_wcs()")

        wcs = WCS(header)
        shape = (header['NAXIS2'], header['NAXIS1'])
        self = cls.from_wcs(wcs, shape=shape)

        if include_full_header:
            self.Spatial.FITSheader = str(header)

        return self

    @classmethod
    def from_wcs(cls, wcs, shape=None):
        """
        Instantiate an AVM object from a WCS transformation

        Parameters
        ----------
        wcs : `~astropy.wcs.WCS` instance
            The WCS to convert to AVM
        shape : tuple, optional
            The shape of the image (using Numpy y, x order)
        """

        if not astropy_installed:
            raise Exception("Astropy is required to use from_wcs()")

        self = cls()

        # Equinox

        self.Spatial.Equinox = wcs.wcs.equinox

        # Projection

        proj1 = wcs.wcs.ctype[0][-3:]
        proj2 = wcs.wcs.ctype[1][-3:]
        if proj1 == proj2:
            self.Spatial.CoordsystemProjection = decode_ascii(proj1)
        else:
            raise Exception("Projections do not agree: %s / %s" % (proj1, proj2))

        try:
            self.Spatial.ReferenceDimension = [wcs.naxis1, wcs.naxis2]
        except:
            if shape is None:
                warnings.warn("no shape specified, so Spatial.ReferenceDimension will not be set")
            else:
                self.Spatial.ReferenceDimension = [shape[1], shape[0]]

        self.Spatial.ReferenceValue = wcs.wcs.crval.tolist()
        self.Spatial.ReferencePixel = wcs.wcs.crpix.tolist()

        try:
            cdelt1, cdelt2, crota2 = get_cdelt_crota(wcs)
            self.Spatial.Scale = cdelt1, cdelt2
            self.Spatial.Rotation = crota2
        except ValueError:
            warnings.warn("cannot represent WCS as a Scale and Rotation, using deprecated CDMatrix instead")
            cd = get_cd(wcs)
            self.Spatial.CDMatrix = cd

        xcoord = decode_ascii(wcs.wcs.ctype[0][:4])
        ycoord = decode_ascii(wcs.wcs.ctype[1][:4])

        if xcoord == 'RA--' and ycoord == 'DEC-':
            if wcs.wcs.radesys in ('ICRS', 'FK5', 'FK4'):
                self.Spatial.CoordinateFrame = str(wcs.wcs.radesys)
            else:  # assume epoch-independent coordinate system
                warnings.warn("RADESYS header keyword not found, assuming ICRS")
                self.Spatial.CoordinateFrame = 'ICRS'
        elif xcoord == 'ELON' and ycoord == 'ELAT':
            self.Spatial.CoordinateFrame = 'ECL'
        elif xcoord == 'GLON' and ycoord == 'GLAT':
            self.Spatial.CoordinateFrame = 'GAL'
        elif xcoord == 'SLON' and ycoord == 'SLAT':
            self.Spatial.CoordinateFrame = 'SGAL'
        else:
            raise Exception("Unknown coordinate system: {0}/{1}".format(xcoord, ycoord))

        self.Spatial.Quality = "Full"

        return self

    def to_xml(self):
        """
        Convert the AVM meta-data to an XML string
        """

        # Register namespaces
        register_namespace('x', "adobe:ns:meta/")
        register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        for namespace in namespaces:
            register_namespace(namespaces[namespace], namespace)

        # Create containing structure
        root = et.Element("{adobe:ns:meta/}xmpmeta")
        trunk = et.SubElement(root, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
        branch = et.SubElement(trunk, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")

        self.MetadataVersion = 1.1

        # Write all the elements
        for name in self._items:
            if isinstance(self._items[name], AVMContainer):
                for key in self._items[name]._items:
                    if self._items[name]._items[key] is not None:
                        if key == "value":
                            avm_class = self._specs['%s' % name]
                            avm_class.to_xml(branch, self._items[name].value)
                        else:
                            avm_class = self._specs['%s.%s' % (name, key)]
                            avm_class.to_xml(branch, self._items[name]._items[key])
            else:
                if self._items[name] is not None and name in self._specs:
                    avm_class = self._specs[name]
                    avm_class.to_xml(branch, self._items[name])

        # Create XML Tree
        tree = et.ElementTree(root)

        # Need to create a BytesIO object to write to
        s = BytesIO()
        tree.write(s, encoding='utf-8')

        # Rewind and read the contents
        s.seek(0)
        xml_string = s.read()

        return xml_string

    def to_xmp(self):
        """
        Convert the AVM meta-data to an XMP packet
        """
        packet = b'<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        packet += self.to_xml()
        packet += b'<?xpacket end="w"?>'

        return packet

    def embed(self, filename_in, filename_out, verify=False):
        """
        Embed the AVM meta-data in an image file
        """

        # Embed XMP packet into file
        embed_xmp(filename_in, filename_out, self.to_xmp())

        # Verify file if needed
        if verify:
            try:
                from PIL import Image
            except ImportError:
                raise ImportError("PIL is required for the verify= option")
            image = Image.open(filename_out)
            image.verify()
