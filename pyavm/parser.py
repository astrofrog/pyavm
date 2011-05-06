# PyAVM - Simple pure-python AVM meta-data parsing
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
               'Spatial.FITSHeader',
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
    AVM is a class to retrieve AVM meta-data from an image file.

    To use, simply create an instance of this class using the filename of the
    image:

    >>> avm = AVM('myexample.jpg')

    Then, you can view the contents by using

    >>> print avm
    ...

    or

    >>> avm
    ...

    Finally, the AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'

    >>> avm.Publisher
    'Chandra X-ray Observatory'
    '''

    def __init__(self, filename):

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

    def to_wcs(self):
        '''
        Convert AVM projection information into a pywcs.WCS object
        '''

        # Try importing pywcs
        try:
            import pywcs
        except:
            raise Exception("PyWCS is required to use to_wcs()")

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
