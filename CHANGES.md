# Changelog

## v0.9.8

### What's Changed
* Accept more JPEG formats by @astrofrog in https://github.com/astrofrog/pyavm/pull/47
* Fix bad function call by @keflavich in https://github.com/astrofrog/pyavm/pull/46
* remove some Python2 leftovers by @a-detiste in https://github.com/astrofrog/pyavm/pull/45

### New Contributors
* @a-detiste made their first contribution in https://github.com/astrofrog/pyavm/pull/45

**Full Changelog**: https://github.com/astrofrog/pyavm/compare/v0.9.7...v0.9.8

## v0.9.7

### What's Changed
* Correct XML output: ordered lists are rdf:Seq, not rdf:Bag by @pkgw in https://github.com/astrofrog/pyavm/pull/44

**Full Changelog**: https://github.com/astrofrog/pyavm/compare/v0.9.6...v0.9.7

## v0.9.6

* Fix header initialization when `use_full_header=True`
* Updated package infrastructure
* Remove unnecessary print statement and reduce warnings

## v0.9.5

* Add `target_shape` argument to `AVM.to_wcs()`
* Fix compatibility with Python 3.8

## v0.9.4

* Properly extract scale and rotation for arbitrary WCS objects.

## v0.9.3

* Fix compatibility with Python 3.
* Add a keyword argument `xmp_packet_index` in AVM.from_image, which can
  be used to indicate which XMP packet to load if there are multiple ones.

## v0.9.2

* Fix compatibility with latest Astropy version. AVM.from_wcs now requires an
  image shape to be passed to set Spatial.ReferenceDimension, for recent
  versions of Astropy. [#28]

## v0.9.1

* Allow AVM meta-data to be read from any file format by simply searching
  for the XMP packet by scanning the file contents.

## v0.9.0

* Complete re-factoring. Embedding for PNG and JPEG is now
  standard-compliant. Initialization from headers, WCS objects, and images
  is now done via class methods (see README.md).

## v0.1.4

* Now write XMP packet using ElementTree to ensure XML compliance

## v0.1.3

* Rewrote XML parsing using ElementTree. Compact XMP tags are now read
  properly. All example images parse without errors.

## v0.1.2

* Added support for embedding AVM meta-data in TIF files

## v0.1.1

* Added support for embedding AVM meta-data in JPG and PNG files, and
  added methods to create AVM container from WCS or FITS header
  information.

## v0.1.0

* Initial Release
