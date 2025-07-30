from vut.loader import loader


def test_loader():
    """Test loader function returns expected value."""
    assert loader() == 1, "Loader should return 1"
