def format_avm(name, value):
    avm = "<avm:%s>" % name

    if type(value) in [list, tuple]:
        avm += "\n <rdf:Seq>\n"
        for item in value:
            if type(item) is float:
                avm += "  <rdf:li>%.16f</rdf:li>\n" % item
            else:
                avm += "  <rdf:li>%s</rdf:li>\n" % str(item)
        avm += " </rdf:Seq>\n"
    else:
        if type(value) is float:
            avm += "%.16f" % value
        else:
            avm += "%s" % str(value)

    avm += "</avm:%s>\n" % name

    return avm


def wcs2avm(wcs):

    packet = ''

    # AVM header

    packet += '<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
    packet += '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="PyAVM">\n'
    packet += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
    packet += '<rdf:Description rdf:about="" xmlns:avm="http://www.communicatingastronomy.org/avm/1.0/">\n'

    # AVM information

    packet += format_avm("MetadataVersion", "1.1")
    packet += format_avm("Spatial.Quality", "Full")

    # Equinox

    packet += format_avm("Spatial.Equinox", wcs.wcs.equinox)

    # Projection

    proj1 = wcs.wcs.ctype[0][-3:]
    proj2 = wcs.wcs.ctype[1][-3:]
    if proj1 == proj2:
        packet += format_avm("Spatial.CoordsystemProjection", proj1)
    else:
        raise Exception("Projections do not agree: %s / %s" % (proj1, proj2))

    packet += format_avm("Spatial.ReferenceDimensions", [wcs.naxis1, wcs.naxis2])
    packet += format_avm("Spatial.ReferenceValue", wcs.wcs.crval.tolist())
    packet += format_avm("Spatial.ReferencePixel", wcs.wcs.crpix.tolist())
    packet += format_avm("Spatial.Scale", wcs.wcs.cdelt.tolist())
    # packet += format_avm("Spatial.Rotation", wcs.wcs.crota[1])

    packet += '</rdf:Description>\n'
    packet += '</rdf:RDF>\n'
    packet += '</x:xmpmeta>\n'
    packet += '<?xpacket end="w"?>\n'

    return packet
