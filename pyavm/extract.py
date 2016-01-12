from __future__ import print_function, division

import re
import warnings

from .jpeg import is_jpeg, JPEGFile
from .png import is_png, PNGFile
from .exceptions import NoXMPPacketFound

__all__ = ['extract_xmp']


def extract_xmp(image, xmp_packet_index=None):

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
            if xmp_packet_index is None:
                if len(xmp_segments) > 1:
                    warnings.warn("Multiple XMP packets are present but "
                                  "xmp_packet_index was not specified, assuming "
                                  "xmp_packet_index=0")
                xmp_packet_index = 0
            elif xmp_packet_index >= len(xmp_segments):
                raise IndexError("xmp_packet was set to {0} but only {1} "
                                 "packets are present".format(xmp_packet_index,
                                                              len(xmp_segments)))
            return xmp_segments[xmp_packet_index]
        else:  # No XMP data was found
            raise NoXMPPacketFound("No XMP packet present in file")

    elif is_png(image):

        # Read in input file
        png_file = PNGFile.read(image)

        xmp_chunks = []

        # Loop through chunks and search for XMP packet
        for chunk in png_file.chunks:
            if chunk.type == b'iTXt':
                if chunk.data.startswith(b'XML:com.adobe.xmp'):
                    xmp_chunks.append(chunk.data[22:])

        if len(xmp_chunks) > 0:
            if xmp_packet_index is None:
                if len(xmp_chunks) > 1:
                    warnings.warn("Multiple XMP packets are present but "
                                  "xmp_packet_index was not specified, assuming "
                                  "xmp_packet_index=0")
                xmp_packet_index = 0
            elif xmp_packet_index >= len(xmp_chunks):
                raise IndexError("xmp_packet was set to {0} but only {1} "
                                 "packets are present".format(xmp_packet_index,
                                                              len(xmp_chunks)))
            return xmp_chunks[xmp_packet_index]
        else:  # No XMP data was found
            raise NoXMPPacketFound("No XMP packet present in file")

    else:

        warnings.warn("Only PNG and JPEG files can be properly parsed "
                      "- scanning file contents for XMP packet")

        with open(image, 'rb') as fileobj:
            contents = fileobj.read()

        start_positions = [m.start() for m in re.finditer(b"<?xpacket begin=", contents)]

        if len(start_positions) > 0:
            if xmp_packet_index is None:
                if len(start_positions) > 1:
                    warnings.warn("Multiple XMP packets are present but "
                                  "xmp_packet_index was not specified, assuming "
                                  "xmp_packet_index=0")
                xmp_packet_index = 0
            elif xmp_packet_index >= len(start_positions):
                raise IndexError("xmp_packet was set to {0} but only {1} "
                                 "packets are present".format(xmp_packet_index,
                                                              len(start_positions)))
            start = start_positions[xmp_packet_index] - 2
            end = contents.index(b"</x:xmpmeta>", start) + 12
        else:
            raise NoXMPPacketFound("No XMP packet present in file")

        return contents[start:end]
