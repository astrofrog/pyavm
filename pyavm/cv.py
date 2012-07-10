# -*- coding: utf-8 -*-
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
Storage for controlled vocabulary fields
"""

TYPE_CHOICES = [
    'Observation', 
    'Artwork',
    'Photographic',
    'Planetary',
    'Simulation',
    'Collage',
    'Chart'
]

IMAGE_PRODUCT_QUALITY_CHOICES = [
    'Good',
    'Moderate',
    'Poor'
]

SPECTRAL_COLOR_ASSIGNMENT_CHOICES = [
    'Purple',
    'Blue',
    'Cyan',
    'Green',
    'Yellow',
    'Orange',
    'Red',
    'Magenta',
    'Grayscale',
    'Pseudocolor',
    'Luminosity',
]

SPECTRAL_BAND_CHOICES = [
    'Radio',
    'Millimeter',
    'Infrared',
    'Optical',
    'Ultraviolet',
    'X-ray',
    'Gamma-ray'
]

SPATIAL_COORDINATE_FRAME_CHOICES = [
    'ICRS',
    'FK5',
    'FK4',
    'ECL',
    'GAL',
    'SGAL',
]

SPATIAL_EQUINOX_CHOICES = [
    'J2000',
    'B1950',
]

SPATIAL_COORDSYSTEM_PROJECTION_CHOICES = [
    'TAN',
    'SIN',
    'ARC',
    'AIT',
    'CAR',
    'CEA',
]

SPATIAL_QUALITY_CHOICES = [
    'Full',
    'Position',
]

METADATA_VERSION_CHOICES = [
	1.2,
    1.1,
    1.0,
] 



