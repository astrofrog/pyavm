from __future__ import print_function, division

import struct

from .jpeg import is_jpeg, JPEGFile, JPEGSegment
from .png import is_png, PNGFile, PNGChunk


def extract_xmp(image):

    if is_jpeg(image):

        # Read in input file
        jpeg_file = JPEGFile.read(image)

        # Loop through segments and search for XMP packet
        for segment in jpeg_file.segments:
            if segment.type == 'APP1':
                if segment.bytes[4:32] == b'http://ns.adobe.com/xap/1.0/':
                    return segment.bytes[32:]

        # No XMP data was found
        raise Exception("No XMP packet present in file")

    elif is_png(image):

        # Read in input file
        png_file = PNGFile.read(image)

        # Loop through chunks and search for XMP packet
        for chunk in png_file.chunks:
            if chunk.type == 'iTXt':
                if chunk.data.startswith(b'XML:com.adobe.xmp'):
                    return chunk.data[22:]

        # No XMP data was found
        raise Exception("No XMP packet present in file")

    else:

        raise Exception("Only JPG and PNG files are supported at this time")
