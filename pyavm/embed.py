import struct
from zlib import crc32


def embed_xmp(image_in, image_out, xmp_packet):

    contents = open(image_in, 'rb').read()

    if image_in.lower().endswith('jpg') or image_in.lower().endswith('jpeg'):

        # Check length
        if len(xmp_packet) >= 65503:
            raise Exception("XMP packet is too long to embed in JPG file")

        # APP1 marker
        full_xmp_packet = "\xff\xe1"

        # Length of XMP packet + 2 + 29
        full_xmp_packet += struct.pack('>H', len(xmp_packet) + 29 + 2)

        # XMP Namespace URI (NULL-terminated)
        full_xmp_packet += "http://ns.adobe.com/xap/1.0/\x00"

        # XMP packet
        full_xmp_packet += xmp_packet

        # Position at which to insert the packet
        try:
            position = contents.index('\xff\xd8') + 2
        except:
            raise Exception("Could not find SOI marker")

        # Embed packet in image
        f_out = open(image_out, 'wb')
        f_out.write(contents[:position])
        f_out.write(full_xmp_packet)
        f_out.write(contents[position:])

    elif image_in.lower().endswith('png'):

        # Keyword
        chunk = 'XML:com.adobe.xmp'

        # Null separator
        chunk += '\xff'

        # Compression flag
        chunk += '\xff'

        # Compression method
        chunk += '\xff'

        # Null separator
        chunk += '\xff'

        # Null separator
        chunk += '\xff'

        # Text
        chunk += xmp_packet

        # Calculate CRC
        crc = struct.pack('>i', crc32('iTXt' + chunk))

        # Find chunk length
        length = struct.pack('>I', len(chunk))

        # Make full packet
        full_xmp_packet = length + 'iTXt' + chunk + crc

        # Position at which to insert the packet
        if contents[12:16] == 'IHDR':
            header_length = struct.unpack('>I', contents[8:12])[0]
            position = 20 + header_length
        else:
            raise Exception("Expected IHDR chunk in PNG file to appear first")

        # Embed packet in image
        f_out = open(image_out, 'wb')
        f_out.write(contents[:position])
        f_out.write(full_xmp_packet)
        f_out.write(contents[position:])

    elif image_in.lower().endswith('tif') or image_in.lower().endswith('tiff'):

        # Identify byte order (little endian or big endian)
        byte_order = contents[:2]
        if byte_order == 'II':
            endian = '<'
        elif byte_order == 'MM':
            endian = '>'
        else:
            raise Exception("Unexpected byte order: %s" % byte_order)

        position = 4

        while True:
            new_position = struct.unpack(endian + 'I', contents[position:position+4])[0]
            if new_position == 0:
                break
            position = new_position
            number = struct.unpack(endian + 'H', contents[position:position+2])[0]
            position = position + 2 + number * 12

        # Find file length
        file_length = len(contents)

        # Update offset to point to the end of the file
        contents = contents[:position] + struct.pack(endian + 'I', file_length) + contents[position+4:]

        # Number of directory entries
        ifd = struct.pack(endian + 'H', 1)

        # Field identification
        ifd += struct.pack(endian + 'H', 700)

        # Field type
        ifd += struct.pack(endian + 'H', 1)

        # XMP packet length
        ifd += struct.pack(endian + 'I', len(xmp_packet))

        # XMP packet
        ifd += struct.pack(endian + 'I', file_length + 18)

        # End of file
        ifd += struct.pack(endian + 'I', 0)

        # Embed packet in image
        f_out = open(image_out, 'wb')
        f_out.write(contents)
        f_out.write(ifd)
        f_out.write(xmp_packet)

    else:
        raise Exception("Only JPG and PNG files are supported at this time")
