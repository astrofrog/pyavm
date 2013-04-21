import pytest
import warnings
warnings.filterwarnings('always')

from ..avm import AVM, AVMContainer


@pytest.mark.parametrize('version', [1.1, 1.2])
def test_specs(version):

    a = AVM(version=version)

    # Creator Metadata
    a.Creator = "PyAVM"
    a.CreatorURL = "http://www.github.com"
    a.Contact.Name = ["Thomas Robitaille"]
    a.Contact.Email = "thomas.robitaille@gmail.com"
    a.Contact.Address = "None of your business"
    a.Contact.Telephone = "I think we're getting a little too personal"
    a.Contact.City = "Heidelberg"
    a.Contact.StateProvince = "Baden-Wuttemburg"
    a.Contact.PostalCode = "What could you possibly need this for?"
    a.Contact.Country = "Germany"
    a.Rights = "Wrongs"

    # Content Metadata
    a.Title = "A very thorough test"
    a.Headline = "What I said above"
    a.Description = "Um, I guess there's not much more to say about this!"
    a.Subject.Category = ["Tests"]
    a.Subject.Name = ["PyAVM"]
    a.Distance = ["3"]
    a.Distance.Notes = "Not much to say, really"
    a.ReferenceURL = "http://www.github.com"
    a.Credit = "Me"
    a.Date = "10 April 2013"
    a.ID = "123123123"
    a.Type = "Simulation"
    a.Image.ProductQuality = "Moderate"

    # Observation Metadata
    a.Facility = ["Python"]
    a.Instrument = ["CPython"]
    a.Spectral.ColorAssignment = ["Purple"]
    a.Spectral.Band = ["Optical"]
    a.Spectral.Bandpass = ["Arbitrary"]
    a.Spectral.CentralWavelength = [5.]
    a.Spectral.Notes = "Still testing"
    a.Temporal.StartTime = ["5 Feb 2011"]
    a.Temporal.IntegrationTime = [4.4]
    a.DatasetID = ["12421412"]

    # Coordinate Metadata
    a.Spatial.CoordinateFrame = "GAL"
    a.Spatial.Equinox = '2000'
    a.Spatial.ReferenceValue = [33.3, 44.4]
    a.Spatial.ReferenceDimension = [300, 400]
    a.Spatial.ReferencePixel = [2., 3.]
    a.Spatial.Scale = [0.2, 0.3]
    a.Spatial.Rotation = 122.
    a.Spatial.CoordsystemProjection = "CAR"
    a.Spatial.Quality = "Full"
    a.Spatial.Notes = "Not much to say"
    a.Spatial.FITSheader = "SIMPLE = T"
    a.Spatial.CDMatrix = [3.4, 3.3, 5.5, 2.1]

    # Publisher Metadata
    a.Publisher = "Tom"
    a.PublisherID = "125521"
    a.ResourceID = "3995611"
    a.ResourceURL = "http://www.github.com"
    a.RelatedResources = ["Testing", "Python", "PyAVM"]
    a.MetadataDate = "20 April 2013"

    # FITS Liberator Metadata

    a.FL.BackgroundLevel = [3.4]
    a.FL.BlackLevel = [4.4]
    a.FL.ScaledPeakLevel = [5.5]
    a.FL.PeakLevel = [10.2]
    a.FL.WhiteLevel = [11.3]
    a.FL.ScaledBackgroundLevel = [4.5]
    a.FL.StretchFunction = ['Log']

    # Spec-dependent keywords
    if version == 1.1:
        with pytest.raises(AttributeError) as exc:
            a.ProposalID = ["12421412"]
        assert exc.value.args[0] == "ProposalID is not a valid AVM group or tag in the 1.1 standard"
        with pytest.raises(AttributeError) as exc:
            a.PublicationID = ['799292']
        assert exc.value.args[0] == "PublicationID is not a valid AVM group or tag in the 1.1 standard"
    else:
        a.ProposalID = ["12421412"]
        a.PublicationID = ['799292']

    x = a.to_xml()

    b = AVM.from_xml(x)

    for key in a._items:
        if isinstance(a._items[key], AVMContainer):
            for subkey in a._items[key]._items:
                assert a._items[key]._items[subkey] == b._items[key]._items[subkey]
        else:
            assert a._items[key] == b._items[key]


def test_warning():

    # Start of with a version=1.2 AVM object
    a = AVM(version=1.2)
    a.ProposalID = ["25661"]

    # Then change to version=1.1, which doesn't contain ProposalID
    with warnings.catch_warnings(record=True) as w:
        a.MetadataVersion = 1.1
        assert len(w) == 1
        assert str(w[0].message) == "ProposalID is not defined in format specification 1.1 and will be deleted"

    try:
        a.ProposalID = ["44663"]
    except AttributeError as exc:
        assert exc.args[0] == "ProposalID is not a valid AVM group or tag in the 1.1 standard"
