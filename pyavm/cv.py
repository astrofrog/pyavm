# -*- coding: utf-8 -*-

from __future__ import print_function, division

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