from __future__ import print_function, division

import re
import struct
import warnings

from .jpeg import is_jpeg, JPEGFile, JPEGSegment
from .png import is_png, PNGFile, PNGChunk
from .exceptions import NoXMPPacketFound

def extract_xmp(image, xmp_packet_index=0):

    if is_jpeg(image):

        # Read in input file
        jpeg_file = JPEGFile.read(image)

        xmp_segments = []

        # Loop through segments and search for XMP packet
        for segment in jpeg_file.segments:
            if segment.type == 'APP1':
                if segment.bytes[4:32] == b'http://ns.adobe.com/xap/1.0/':
                    xmp_segments.append(segment.bytes[32:])

        if len(xmp_segments) > 0:
            return xmp_segments[xmp_packet_index]
        else:  # No XMP data was found
            raise NoXMPPacketFound("No XMP packet present in file")

    elif is_png(image):

        # Read in input file
        png_file = PNGFile.read(image)

        xmp_chunks = []

        # Loop through chunks and search for XMP packet
        for chunk in png_file.chunks:
            if chunk.type == 'iTXt':
                if chunk.data.startswith(b'XML:com.adobe.xmp'):
                    xmp_chunks.append(chunk.data[22:])

        if len(xmp_chunks) > 0:
            return xmp_chunks[xmp_packet_index]
        else:  # No XMP data was found
            raise NoXMPPacketFound("No XMP packet present in file")

    else:

        warnings.warn("Only PNG and JPEG files can be properly parsed - scanning file contents for XMP packet")

        with open(image, 'rb') as fileobj:
            contents = fileobj.read()

        start_positions = [m.start() for m in re.finditer(b"<?xpacket begin=", contents)]

        if len(start_positions) > 0:
            start = start_positions[xmp_packet_index] - 2
            end = contents.index(b"</x:xmpmeta>", start) + 12
        else:
            raise NoXMPPacketFound("No XMP packet present in file")

        return contents[start:end]
