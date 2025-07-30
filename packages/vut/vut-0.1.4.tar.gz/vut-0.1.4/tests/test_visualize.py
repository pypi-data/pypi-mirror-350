import os
import tempfile

import numpy as np
import pytest
from pytest_mock import MockerFixture

from vut.visualize import (
    plot_feature,
    plot_features,
    plot_image,
    plot_images,
    plot_palette,
)


@pytest.fixture
def img():
    return np.ceil(np.random.rand(100, 100, 3) * 255).astype(np.uint8)


def test_plot_palette__save_as_file(mocker: MockerFixture):
    mocker.patch("matplotlib.pyplot.get_cmap", return_value="viridis")
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path = tmp_file.name
    plot_palette(name="viridis", path=path)
    assert os.path.exists(path)
    os.remove(path)


def test_plot_palette__with_palette():
    palette = np.random.rand(10, 3)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path = tmp_file.name
    plot_palette(palette=palette, path=path)
    assert os.path.exists(path)
    os.remove(path)


def test_plot_image__save_as_file(img):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path = tmp_file.name
    plot_image(img, path=path)
    assert os.path.exists(path)
    os.remove(path)


def test_plot_image__show_in_jupyter(img, mocker: MockerFixture):
    mock = mocker.patch("matplotlib.pyplot.show")
    plot_image(img, is_jupyter=True)
    mock.assert_called_once()


def test_plot_image__return_canvas(img):
    canvas = plot_image(img, return_canvas=True)
    assert canvas.shape == (480, 640, 3)


def test_plot_images__save_as_file(img):
    images = [img, img]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path1 = tmp_file.name
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path2 = tmp_file.name
    plot_images(images, paths=[path1, path2])
    assert os.path.exists(path1)
    assert os.path.exists(path2)
    os.remove(path1)
    os.remove(path2)


def test_plot_images__show_in_jupyter(img, mocker: MockerFixture):
    images = [img, img]
    mock = mocker.patch("matplotlib.pyplot.show")
    plot_images(images, is_jupyter=True)
    mock.assert_called_once()


def test_plot_images__return_canvas(img):
    images = [img, img]
    canvas = plot_images(images, return_canvas=True)
    assert len(canvas) == 2


def test_plot_feature__save_as_file():
    feature = np.random.rand(10, 10)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path = tmp_file.name
    plot_feature(feature, path=path)
    assert os.path.exists(path)
    os.remove(path)


def test_plot_feature__show_in_jupyter(mocker: MockerFixture):
    feature = np.random.rand(10, 10)
    mock = mocker.patch("matplotlib.pyplot.show")
    plot_feature(feature, is_jupyter=True)
    mock.assert_called_once()


def test_plot_feature__return_canvas():
    feature = np.random.rand(10, 10)
    canvas = plot_feature(feature, return_canvas=True)
    assert canvas.shape == (480, 640, 3)


def test_plot_features__save_as_file():
    features = [np.random.rand(10, 10), np.random.rand(10, 10)]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path1 = tmp_file.name
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        path2 = tmp_file.name
    plot_features(features, paths=[path1, path2])
    assert os.path.exists(path1)
    assert os.path.exists(path2)
    os.remove(path1)
    os.remove(path2)


def test_plot_features__show_in_jupyter(mocker: MockerFixture):
    features = [np.random.rand(10, 10), np.random.rand(10, 10)]
    mock = mocker.patch("matplotlib.pyplot.show")
    plot_features(features, is_jupyter=True)
    mock.assert_called_once()


def test_plot_features__return_canvas():
    features = [np.random.rand(10, 10), np.random.rand(10, 10)]
    canvas = plot_features(features, return_canvas=True)
    assert len(canvas) == 2
