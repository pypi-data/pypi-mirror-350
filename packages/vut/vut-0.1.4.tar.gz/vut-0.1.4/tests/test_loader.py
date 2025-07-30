from vut.loader import loader


def test_loader():
    assert loader() == 1, "Loader should return 1"
