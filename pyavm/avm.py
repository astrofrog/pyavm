# PyAVM - Simple pure-python AVM meta-data handling
# Copyright (c) 2011 Thomas P. Robitaille
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

# Please note: this should 'do the job' but could probably be written in a
# more efficient way - suggestions are welcome!

# Try importing pywcs

from StringIO import StringIO

try:
    import pywcs
    pywcs_installed = True
except:
    pywcs_installed = False

try:
    import pyfits
    pyfits_installed = True
except:
    pyfits_installed = False

from pyavm.embed import embed_xmp

# Define acceptable tags to avoid reading in non-AVM meta-data

tags = {}

tags['xapRights'] = [
                     'UsageTerms',
                    ]

tags['Iptc4xmpCore'] = [
                        'CiUrlWork',
                        'CiEmailWork',
                        'CiTelWork',
                        'CiAdrExtadr',
                        'CiAdrCity',
                        'CiAdrRegion',
                        'CiAdrPcode',
                        'CiAdrCtry',
                       ]

tags['dc'] = [
              'creator',
              'rights',  # Not in 1.1 standard, but in all examples
              'format',  # Not in 1.1 standard, but in all examples
              'title',
              'description',
              'subject',
             ]

tags['avm'] = [
               'CreatorURL',  # Not in 1.1 standard, but in all examples
               'Subject.Category',
               'Distance',
               'Distance.Notes',
               'ReferenceURL',
               'ID',
               'Type',
               'Image.ProductQuality',
               'Facility',
               'Instrument',
               'Spectral.ColorAssignment',
               'Spectral.Band',
               'Spectral.Bandpass',
               'Spectral.CentralWavelength',
               'Spectral.Notes',
               'Temporal.StartTime',
               'Temporal.IntegrationTime',
               'DatasetID',
               'Spatial.CoordinateFrame',
               'Spatial.Equinox',
               'Spatial.ReferenceValue',
               'Spatial.ReferenceDimension',
               'Spatial.ReferencePixel',
               'Spatial.Scale',
               'Spatial.Rotation',
               'Spatial.CoordsystemProjection',
               'Spatial.Quality',
               'Spatial.Notes',
               'Spatial.FITSheader',
               'Spatial.CDMatrix',
               'Publisher',
               'PublisherID',
               'ResourceID',
               'ResourceURL',
               'RelatedResources',
               'MetadataDate',
               'MetadataVersion',
              ]


def capitalize(string):
    return string[0].upper() + string[1:]


def auto_type(string):
    '''Try and convert a string to an integer or float'''
    try:
        return int(string)
    except:
        try:
            return float(string)
        except:
            return string


def parse_rdf_seq(rdf):
    '''Parse and RDF Seq/Bag/Alt and return a list'''
    start = rdf.find("<rdf:Seq>")
    end = rdf.find("</rdf:Seq>")
    content = rdf[start + 9:end].strip()
    start = 0
    seq = []
    while True:
        start = content.find("<rdf:li", start)
        if start < 0:
            break
        start = content.index(">", start)
        end = content.find("</rdf:li", start)
        seq.append(auto_type(content[start + 1:end].strip()))
    return seq


def format_rdf_seq(seq):

    rdf = " <rdf:Seq>\n"
    for item in seq:
        if type(item) is float:
            rdf += "  <rdf:li>%.16f</rdf:li>\n" % item
        else:
            rdf += "  <rdf:li>%s</rdf:li>\n" % str(item)
    rdf += " </rdf:Seq>\n"

    return rdf


def parse_object(tag, string):
    '''Parse a single AVM tag'''

    start1 = string.index('<%s:' % tag)
    end1 = string.index('>', start1)
    name = string[start1 + 2 + len(tag):end1]
    name = name.split()[0]

    start2 = string.index('</%s' % tag)
    end2 = string.index('>', start2)

    content = string[end1 + 1:start2]

    if "<rdf" in content:
        if "<rdf:Seq>" in content:
            content = parse_rdf_seq(content)
        elif "<rdf:Bag>" in content:
            content = parse_rdf_seq(content)
        elif "<rdf:Alt>" in content:
            content = parse_rdf_seq(content)
        else:
            raise Exception("Unexpected RDF content: %s" % content)
    else:
        content = auto_type(content.strip())

    return name, content


def format_object(name, content):

    string = "<avm:%s>" % name

    if type(content) in [list, tuple]:
        string += '\n' + format_rdf_seq(content)
    else:
        if type(content) is float:
            string += "%.16f" % content
        else:
            string += "%s" % str(content)

    string += "</avm:%s>\n" % name

    return string


class AVMContainer(object):

    def __str__(self, indent=0):

        string = ""
        for family in self.__dict__:
            if type(self.__dict__[family]) is AVMContainer:
                string += indent * " " + "%s:\n" % family
                string += self.__dict__[family].__str__(indent + 3)
            else:
                if type(self.__dict__[family]) is list:
                    string += indent * " " + "%s:\n" % family
                    for elem in self.__dict__[family]:
                        string += indent * " " + "   * %s\n" % str(elem)
                else:
                    string += indent * " " + \
                              "%s: %s\n" % (family, str(self.__dict__[family]))

        return string


class AVM(AVMContainer):
    '''
    To parse AVM meta-data from an existing file, simply create an instance of this class using the filename of the image (or any file-like object):

        >>> avm = AVM('myexample.jpg')

    Then, you can view the contents by using

        >>> print avm

    or

        >>> avm

    The AVM meta-data can be accessed using the attribute notation:

        >>> avm.Spatial.Equinox
        'J2000'

        >>> avm.Publisher
        'Chandra X-ray Observatory'

    It is also possible to initialize an AVM object using a pywcs.WCS instance:

        >>> import pyfits
        >>> import pywcs
        >>> from pyavm import AVM
        >>> wcs = pywcs.WCS(pyfits.getheader('image.fits'))
        >>> avm = AVM(wcs)

    Finally, it is possible to embed AVM meta-data into an image file:

        >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

    At this time, only JPG and PNG files are supported for embedding.
    '''

    def __init__(self, *args):

        if len(args) == 1:
            if type(args[0]) is str:
                self.from_file(args[0])
            elif pyfits_installed and isinstance(args[0], pyfits.Header):
                self.from_header(args[0])
            elif pywcs_installed and isinstance(args[0], pywcs.WCS):
                self.from_wcs(args[0])
            else:
                raise Exception("Unknown arguemnt type: %s" % type(args[0]))
        elif len(args) > 1:
            raise Exception("Too many arguments")

    def create_group(self, group):
        if hasattr(self, group):
            raise Exception("Group %s already exists" % group)
        else:
            self.__dict__[group] = AVMContainer()

    def from_file(self, filename):

        # Read in image
        if hasattr(filename, 'read'):
            contents = filename.read()
        else:
            contents = file(filename, 'rb').read()

        # Look for XMP packets
        start = 0
        while True:
            start = contents.find("<?xpacket begin=", start)
            if start < 0:
                raise Exception("No AVM data found")
            start = contents.index("?>", start) + 2
            end = contents.index("</x:xmpmeta>")
            print "Found XMP packet with %i bytes" % (end - start)
            if "<avm:" in contents[start:end]:
                print "Found AVM meta-data in XMP packet"
                break
            else:
                print "Did not find AVM meta-data in XMP packet"

        # AVM data has been found
        xml = contents[start:end]

        for tag in tags:

            end = 0

            while True:

                # Search for next AVM block
                start = xml.find('<%s' % tag, end)
                if start < 0:
                    break
                end = xml.index('</%s' % tag, start)
                end = xml.index('>', end)

                # Parse the AVM
                name, content = parse_object(tag, xml[start:end + 1])

                if name in tags[tag]:

                    # Add to AVM dictionary
                    if "." in name:
                        family, key = name.split('.')
                        if not family in self.__dict__:
                            self.__dict__[capitalize(family)] = AVMContainer()
                        self.__dict__[capitalize(family)].__dict__[capitalize(key)] = content
                    else:
                        self.__dict__[capitalize(name)] = content

                else:

                    print "WARNING: ignoring tag %s:%s" % (tag, name)

    def to_wcs(self, use_full_header=True):
        '''
        Convert AVM projection information into a pywcs.WCS object
        '''

        if not pywcs_installed:
            raise Exception("PyWCS is required to use to_wcs()")

        if use_full_header and hasattr(self.Spatial, 'FITSheader'):
            print "Using full FITS header from Spatial.FITSheader"
            header = pyfits.Header(txtfile=StringIO(self.Spatial.FITSheader))
            return pywcs.WCS(header)

        # Initializing WCS object
        wcs = pywcs.WCS(naxis=2)

        # Find the coordinate type
        try:
            ctype = self.Spatial.CoordinateFrame
        except:
            print "WARNING: Spatial.CoordinateFrame not found, assuming ICRS"
            ctype = 'ICRS'

        wcs.wcs.radesys = ctype

        if ctype in ['ICRS', 'FK5', 'FK4']:
            xcoord = "RA--"
            ycoord = "DEC-"
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

        wcs.wcs.ctype[0] = xcoord + cproj
        wcs.wcs.ctype[1] = ycoord + cproj

        # Find the equinox
        equinox = self.Spatial.Equinox

        if type(equinox) is str:
            if equinox == "J2000":
                wcs.wcs.equinox = 2000.
            elif equinox == "B1950":
                wcs.wcs.equinox = 1950.
            else:
                raise Exception("Unknown equinox: %s" % equinox)
        else:
            wcs.wcs.equinox = float(equinox)

        # Set standard WCS parameters
        wcs.naxis1, wcs.naxis2 = self.Spatial.ReferenceDimension
        wcs.wcs.crval = self.Spatial.ReferenceValue
        wcs.wcs.crpix = self.Spatial.ReferencePixel

        if hasattr(self.Spatial, "CDMatrix"):
            wcs.wcs.cd = [self.Spatial.CDMatrix[0:2],
                          self.Spatial.CDMatrix[2:4]]
        elif hasattr(self.Spatial, "Scale"):
            wcs.wcs.cdelt = self.Spatial.Scale
            if hasattr(self.Spatial, "Rotation"):
                wcs.wcs.crota = self.Spatial.Rotation, self.Spatial.Rotation

        return wcs

    def from_header(self, header, include_full_header=True):
        '''
        Convert a FITS header into AVM information
        '''

        if not pyfits_installed:
            raise Exception("PyWCS is required to use from_wcs()")

        if not hasattr(self, 'Spatial'):
            self.Spatial = AVMContainer()

        if include_full_header:
            self.Spatial.FITSheader = str(header)

        if pywcs_installed:
            wcs = pywcs.WCS(header)
            self.from_wcs(wcs)

    def from_wcs(self, wcs):
        '''
        Convert a pywcs.WCS object into AVM information
        '''

        if not pywcs_installed:
            raise Exception("PyWCS is required to use from_wcs()")

        if not hasattr(self, 'Spatial'):
            self.Spatial = AVMContainer()

        # Equinox

        self.Spatial.Equinox = wcs.wcs.equinox

        # Projection

        proj1 = wcs.wcs.ctype[0][-3:]
        proj2 = wcs.wcs.ctype[1][-3:]
        if proj1 == proj2:
            self.Spatial.CoordsystemProjection = proj1
        else:
            raise Exception("Projections do not agree: %s / %s" % (proj1, proj2))

        self.Spatial.ReferenceDimension = [wcs.naxis1, wcs.naxis2]
        self.Spatial.ReferenceValue = wcs.wcs.crval.tolist()
        self.Spatial.ReferencePixel = wcs.wcs.crpix.tolist()
        self.Spatial.Scale = wcs.wcs.cdelt.tolist()
        try:
            self.Spatial.Rotation, wcs.wcs.crota[1]
        except:
            pass

        self.Spatial.Quality = "Full"

    def to_xmp(self):

        packet = ''

        # AVM header

        packet += '<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        packet += '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="PyAVM">\n'
        packet += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        packet += '<rdf:Description rdf:about="" xmlns:avm="http://www.communicatingastronomy.org/avm/1.0/">\n'

        # AVM information

        packet += format_object("MetadataVersion", "1.1")

        for name in self.__dict__:
            if isinstance(self.__dict__[name], AVMContainer):
                for key in self.__dict__[name].__dict__:
                    packet += format_object('%s.%s' % (name, key), self.__dict__[name].__dict__[key])
            else:
                packet += format_object(name, self.__dict__[name])

        packet += '</rdf:Description>\n'
        packet += '</rdf:RDF>\n'
        packet += '</x:xmpmeta>\n'
        packet += '<?xpacket end="w"?>\n'

        return packet

    def embed(self, filename_in, filename_out, verify=False):

        # Embed XMP packet into file
        embed_xmp(filename_in, filename_out, self.to_xmp())

        # Verify file if needed
        if verify:
            import Image
            image = Image.open(filename_out)
            image.verify()
