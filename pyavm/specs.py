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
from .consts import *


AVM_SCHEMAS = {
    XMP_NS_IPTCCore: 'Iptc4xmpCore',
    XMP_NS_DC: 'dc',
    XMP_NS_AVM: 'avm',
    XMP_NS_XMP: 'xmpRights',
    XMP_NS_Photoshop: 'photoshop',
}

SPECS_1_1 = {

    # Creator Metadata
    'Creator' : AVMString(XMP_NS_Photoshop, 'photoshop:Source'),
    'CreatorURL': AVMURL(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiUrlWork'),
    'Contact.Name': AVMOrderedList(XMP_NS_DC, 'dc:creator'),
    'Contact.Email': AVMEmail(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiEmailWork'),
    'Contact.Address': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiAdrExtadr'),
    'Contact.Telephone': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiTelWork'),
    'Contact.City': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiAdrCity'),
    'Contact.StateProvince': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiAdrRegion'),
    'Contact.PostalCode': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiAdrPcode'),
    'Contact.Country': AVMString(XMP_NS_IPTCCore, 'Iptc4xmpCore:CreatorContactInfo/Iptc4xmpCore:CiAdrCtry'),
    'Rights': AVMLocalizedString(XMP_NS_XMP_Rights, 'xmpRights:UsageTerms'),
    
    # Content Metadata
    'Title': AVMLocalizedString(XMP_NS_DC, 'dc:title'),
    'Headline': AVMString(XMP_NS_Photoshop, 'photoshop:Headline'),
    'Description': AVMLocalizedString(XMP_NS_DC, 'dc:description'),
    'Subject.Category': AVMUnorderedStringList(XMP_NS_AVM, 'avm:Subject.Category'),
    'Subject.Name': AVMUnorderedStringList(XMP_NS_DC, 'dc:subject'),
    'Distance': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Distance', length=2, strict_length=False),
    'Distance.Notes': AVMString(XMP_NS_AVM, 'avm:Distance.Notes'),
    'ReferenceURL': AVMURL(XMP_NS_AVM, 'avm:ReferenceURL'),
    'Credit': AVMString(XMP_NS_Photoshop, 'photoshop:Credit'),
    'Date': AVMDateTime(XMP_NS_Photoshop, 'photoshop:DateCreated'),
    'ID': AVMString(XMP_NS_AVM, 'avm:ID'),
    'Type': AVMStringCVCapitalize(XMP_NS_AVM, 'avm:Type', TYPE_CHOICES),
    'Image.ProductQuality': AVMStringCVCapitalize(XMP_NS_AVM, 'avm:Image.ProductQuality', IMAGE_PRODUCT_QUALITY_CHOICES),
    
    # Observation Metadata
    'Facility': AVMOrderedList(XMP_NS_AVM, 'avm:Facility'),
    'Instrument': AVMOrderedList(XMP_NS_AVM, 'avm:Instrument'),
    'Spectral.ColorAssignment': AVMOrderedListCV(XMP_NS_AVM, 'avm:Spectral.ColorAssignment', SPECTRAL_COLOR_ASSIGNMENT_CHOICES),
    'Spectral.Band': AVMOrderedListCV(XMP_NS_AVM, 'avm:Spectral.Band', SPECTRAL_BAND_CHOICES),
    'Spectral.Bandpass': AVMOrderedList(XMP_NS_AVM, 'avm:Spectral.Bandpass'),
    'Spectral.CentralWavelength': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spectral.CentralWavelength'),
    'Spectral.Notes': AVMLocalizedString(XMP_NS_AVM, 'avm:Spectral.Notes'),
    'Temporal.StartTime': AVMDateTimeList(XMP_NS_AVM, 'avm:Temporal.StartTime'),
    'Temporal.IntegrationTime': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Temporal.IntegrationTime'),
    'DatasetID': AVMOrderedList(XMP_NS_AVM, 'avm:DatasetID'),
    
    # Coordinate Metadata
    'Spatial.CoordinateFrame': AVMStringCVUpper(XMP_NS_AVM, 'avm:Spatial.CoordinateFrame', SPATIAL_COORDINATE_FRAME_CHOICES),
    'Spatial.Equinox': AVMStringCVUpper(XMP_NS_AVM, 'avm:Spatial.Equinox', SPATIAL_EQUINOX_CHOICES),
    'Spatial.ReferenceValue': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spatial.ReferenceValue', length=2, strict_length=True),
    'Spatial.ReferenceDimension': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spatial.ReferenceDimension', length=2, strict_length=True),
    'Spatial.ReferencePixel': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spatial.ReferencePixel', length=2, strict_length=True),
    'Spatial.Scale': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spatial.Scale', length=2, strict_length=True),
    'Spatial.Rotation': AVMFloat(XMP_NS_AVM, 'avm:Spatial.Rotation'),
    'Spatial.CoordsystemProjection': AVMStringCVUpper(XMP_NS_AVM, 'avm:Spatial.CoordsystemProjection', SPATIAL_COORDSYSTEM_PROJECTION_CHOICES),
    'Spatial.Quality': AVMStringCVCapitalize(XMP_NS_AVM, 'avm:Spatial.Quality', SPATIAL_QUALITY_CHOICES),
    'Spatial.Notes': AVMLocalizedString(XMP_NS_AVM, 'avm:Spatial.Notes'),
    'Spatial.FITSheader': AVMString(XMP_NS_AVM, 'avm:Spatial.FITSheader'),
    'Spatial.CDMatrix': AVMOrderedFloatList(XMP_NS_AVM, 'avm:Spatial.CDMatrix', length=4, strict_length=True, deprecated=True),
    
    # Publisher Metadata
    'Publisher': AVMString(XMP_NS_AVM, 'avm:Publisher'),
    'PublisherID': AVMString(XMP_NS_AVM, 'avm:PublisherID'),
    'ResourceID': AVMString(XMP_NS_AVM, 'avm:ResourceID'),
    'ResourceURL': AVMURL(XMP_NS_AVM, 'avm:ResourceURL'),
    'RelatedResources': AVMUnorderedStringList(XMP_NS_AVM, 'avm:RelatedResources'),
    'MetadataDate': AVMDateTime(XMP_NS_AVM, 'avm:MetadataDate'),
    'MetadataVersion': AVMFloat(XMP_NS_AVM, 'avm:MetadataVersion'),
}

SPECS_1_2 = SPECS_1_1

# Content Metadata

SPECS_1_2['PublicationID'] = AVMUnorderedStringList(XMP_NS_AVM, 'avm:PublicationID')
SPECS_1_2['ProposalID'] = AVMUnorderedStringList(XMP_NS_AVM, 'avm:ProposalID')
SPECS_1_2["RelatedResources"] = AVMUnorderedStringList(XMP_NS_AVM, 'avm:RelatedResources', deprecated=True)