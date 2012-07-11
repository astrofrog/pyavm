# -*- coding: utf-8 -*-
#
# The following source file is based on libavm/specs.py
#
# The original copyright notice is below:
#
# Copyright (c) 2009, European Space Agency & European Southern Observatory (ESA/ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#      * Neither the name of the European Space Agency, European Southern
#        Observatory nor the names of its contributors may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESA/ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

"""
Specification for various versions of AVM

.. todo:: Write specification for version 1.0
"""

from .datatypes import *
from .cv import *

SPECS = {}

SPECS['1.1'] = {

    # Creator Metadata
    'Creator': AVMString('photoshop:Source'),
    'CreatorURL': AVMURL('Iptc4xmpCore:CreatorContactInfo.CiUrlWork'),
    'Contact.Name': AVMOrderedList('dc:creator'),
    'Contact.Email': AVMEmail('Iptc4xmpCore:CreatorContactInfo.CiEmailWork'),
    'Contact.Address': AVMString('Iptc4xmpCore:CreatorContactInfo.CiAdrExtadr'),
    'Contact.Telephone': AVMString('Iptc4xmpCore:CreatorContactInfo.CiTelWork'),
    'Contact.City': AVMString('Iptc4xmpCore:CreatorContactInfo.CiAdrCity'),
    'Contact.StateProvince': AVMString('Iptc4xmpCore:CreatorContactInfo.CiAdrRegion'),
    'Contact.PostalCode': AVMString('Iptc4xmpCore:CreatorContactInfo.CiAdrPcode'),
    'Contact.Country': AVMString('Iptc4xmpCore:CreatorContactInfo.CiAdrCtry'),
    'Rights': AVMLocalizedString('xmpRights:UsageTerms'),

    # Content Metadata
    'Title': AVMLocalizedString('dc:title'),
    'Headline': AVMString('photoshop:Headline'),
    'Description': AVMLocalizedString('dc:description'),
    'Subject.Category': AVMUnorderedStringList('avm:Subject.Category'),
    'Subject.Name': AVMUnorderedStringList('dc:subject'),
    'Distance': AVMOrderedFloatList('avm:Distance', length=2, strict_length=False),
    'Distance.Notes': AVMString('avm:Distance.Notes'),
    'ReferenceURL': AVMURL('avm:ReferenceURL'),
    'Credit': AVMString('photoshop:Credit'),
    'Date': AVMDateTime('photoshop:DateCreated'),
    'ID': AVMString('avm:ID'),
    'Type': AVMStringCVCapitalize('avm:Type', TYPE_CHOICES),
    'Image.ProductQuality': AVMStringCVCapitalize('avm:Image.ProductQuality', IMAGE_PRODUCT_QUALITY_CHOICES),

    # Observation Metadata
    'Facility': AVMOrderedList('avm:Facility'),
    'Instrument': AVMOrderedList('avm:Instrument'),
    'Spectral.ColorAssignment': AVMOrderedListCV('avm:Spectral.ColorAssignment', SPECTRAL_COLOR_ASSIGNMENT_CHOICES),
    'Spectral.Band': AVMOrderedListCV('avm:Spectral.Band', SPECTRAL_BAND_CHOICES),
    'Spectral.Bandpass': AVMOrderedList('avm:Spectral.Bandpass'),
    'Spectral.CentralWavelength': AVMOrderedFloatList('avm:Spectral.CentralWavelength'),
    'Spectral.Notes': AVMLocalizedString('avm:Spectral.Notes'),
    'Temporal.StartTime': AVMDateTimeList('avm:Temporal.StartTime'),
    'Temporal.IntegrationTime': AVMOrderedFloatList('avm:Temporal.IntegrationTime'),
    'DatasetID': AVMOrderedList('avm:DatasetID'),

    # Coordinate Metadata
    'Spatial.CoordinateFrame': AVMStringCVUpper('avm:Spatial.CoordinateFrame', SPATIAL_COORDINATE_FRAME_CHOICES),
    'Spatial.Equinox': AVMStringCVUpper('avm:Spatial.Equinox', SPATIAL_EQUINOX_CHOICES),
    'Spatial.ReferenceValue': AVMOrderedFloatList('avm:Spatial.ReferenceValue', length=2, strict_length=True),
    'Spatial.ReferenceDimension': AVMOrderedFloatList('avm:Spatial.ReferenceDimension', length=2, strict_length=True),
    'Spatial.ReferencePixel': AVMOrderedFloatList('avm:Spatial.ReferencePixel', length=2, strict_length=True),
    'Spatial.Scale': AVMOrderedFloatList('avm:Spatial.Scale', length=2, strict_length=True),
    'Spatial.Rotation': AVMFloat('avm:Spatial.Rotation'),
    'Spatial.CoordsystemProjection': AVMStringCVUpper('avm:Spatial.CoordsystemProjection', SPATIAL_COORDSYSTEM_PROJECTION_CHOICES),
    'Spatial.Quality': AVMStringCVCapitalize('avm:Spatial.Quality', SPATIAL_QUALITY_CHOICES),
    'Spatial.Notes': AVMLocalizedString('avm:Spatial.Notes'),
    'Spatial.FITSheader': AVMString('avm:Spatial.FITSheader'),
    'Spatial.CDMatrix': AVMOrderedFloatList('avm:Spatial.CDMatrix', length=4, strict_length=True, deprecated=True),

    # Publisher Metadata
    'Publisher': AVMString('avm:Publisher'),
    'PublisherID': AVMString('avm:PublisherID'),
    'ResourceID': AVMString('avm:ResourceID'),
    'ResourceURL': AVMURL('avm:ResourceURL'),
    'RelatedResources': AVMUnorderedStringList('avm:RelatedResources'),
    'MetadataDate': AVMDateTime('avm:MetadataDate'),
    'MetadataVersion': AVMFloat('avm:MetadataVersion'),
}

SPECS['1.2'] = SPECS['1.1']

# Content Metadata

SPECS['1.2']['PublicationID'] = AVMUnorderedStringList('avm:PublicationID')
SPECS['1.2']['ProposalID'] = AVMUnorderedStringList('avm:ProposalID')
SPECS['1.2']["RelatedResources"] = AVMUnorderedStringList('avm:RelatedResources', deprecated=True)

# Create reverse lookup

REVERSE_SPECS = {}
for spec in SPECS:
    REVERSE_SPECS[spec] = {}
    for key in SPECS[spec]:
        value = SPECS[spec][key]
        REVERSE_SPECS[spec][value.namespace, value.tag] = key
