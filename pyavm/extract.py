import re
import warnings

from .exceptions import NoXMPPacketFound
from .jpeg import JPEGFile, is_jpeg
from .png import PNGFile, is_png

__all__ = ["extract_xmp"]


def _select_packet(packets, xmp_packet_index):
    """
    Select an XMP packet from a list based on the given index.

    If xmp_packet_index is None and multiple packets exist, warns and defaults to 0.
    Raises IndexError if index is out of range.
    Raises NoXMPPacketFound if no packets exist.
    """
    if not packets:
        raise NoXMPPacketFound("No XMP packet present in file")

    if xmp_packet_index is None:
        if len(packets) > 1:
            warnings.warn(
                "Multiple XMP packets are present but "
                "xmp_packet_index was not specified, assuming "
                "xmp_packet_index=0"
            )
        xmp_packet_index = 0
    elif xmp_packet_index >= len(packets):
        raise IndexError(
            f"xmp_packet was set to {xmp_packet_index} but only {len(packets)} packets are present"
        )

    return packets[xmp_packet_index]


def extract_xmp(image, xmp_packet_index=None):
    if is_jpeg(image):
        # Read in input file
        jpeg_file = JPEGFile.read(image)

        # Loop through segments and search for XMP packet
        xmp_segments = [
            segment.bytes[32:]
            for segment in jpeg_file.segments
            if segment.type == "APP1" and segment.bytes[4:32] == b"http://ns.adobe.com/xap/1.0/"
        ]

        return _select_packet(xmp_segments, xmp_packet_index)

    elif is_png(image):
        # Read in input file
        png_file = PNGFile.read(image)

        # Loop through chunks and search for XMP packet
        xmp_chunks = [
            chunk.data[22:]
            for chunk in png_file.chunks
            if chunk.type == b"iTXt" and chunk.data.startswith(b"XML:com.adobe.xmp")
        ]

        return _select_packet(xmp_chunks, xmp_packet_index)

    else:
        warnings.warn(
            "Only PNG and JPEG files can be properly parsed - scanning file contents for XMP packet"
        )

        with open(image, "rb") as fileobj:
            contents = fileobj.read()

        start_positions = [m.start() for m in re.finditer(b"<?xpacket begin=", contents)]

        if not start_positions:
            raise NoXMPPacketFound("No XMP packet present in file")

        if xmp_packet_index is None:
            if len(start_positions) > 1:
                warnings.warn(
                    "Multiple XMP packets are present but "
                    "xmp_packet_index was not specified, assuming "
                    "xmp_packet_index=0"
                )
            xmp_packet_index = 0
        elif xmp_packet_index >= len(start_positions):
            raise IndexError(
                f"xmp_packet was set to {xmp_packet_index} but only {len(start_positions)} "
                "packets are present"
            )

        start = start_positions[xmp_packet_index] - 2
        end = contents.index(b"</x:xmpmeta>", start) + 12

        return contents[start:end]
