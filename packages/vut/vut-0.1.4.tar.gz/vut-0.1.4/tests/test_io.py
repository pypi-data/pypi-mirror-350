import os
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest
import torch

from vut.io import (
    get_dirs,
    get_images,
    load_file,
    load_image,
    load_images,
    load_list,
    load_np,
    load_tensor,
    save,
    save_image,
    save_list,
)


def test_get_dirs__non_recursive():
    path = os.path.dirname(__file__)
    dirs = get_dirs(path, recursive=False)
    assert all(os.path.isdir(d) for d in dirs), "All items should be directories"


def test_get_dirs__recursive():
    path = os.path.dirname(__file__)
    dirs = get_dirs(path, recursive=True)
    assert all(os.path.isdir(d) for d in dirs), "All items should be directories"


def test_get_dirs__empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        dirs = get_dirs(temp_dir, recursive=False)
        assert dirs == [], "Empty directory should return an empty list"


def test_get_dirs__non_existent_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_path = os.path.join(temp_dir, "non_existent")
        dirs = get_dirs(non_existent_path, recursive=False)
        assert dirs == [], "Non-existent path should return an empty list"


def test_get_dirs__not_a_directory():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"test")
        temp_file_path = temp_file.name
    dirs = get_dirs(temp_file_path, recursive=False)
    assert dirs == [], "File path should return an empty list"
    os.remove(temp_file_path)


def test_get_images():
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = [Path(temp_dir) / f"image_{i}.jpg" for i in range(3)]
        for path in image_paths:
            with open(path, "wb") as f:
                f.write(b"test")
        images = get_images(temp_dir)
        assert len(images) == 3, "Should find 3 images"


def test_get_images__non_existent_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_dir = os.path.join(temp_dir, "non_existent")
        with pytest.raises(FileNotFoundError):
            get_images(non_existent_dir)


def test_get_images__not_a_directory():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"test")
        temp_file_path = temp_file.name
    with pytest.raises(NotADirectoryError):
        get_images(temp_file_path)
    os.remove(temp_file_path)


def test_save_list_with_callback():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save_list(data, file_path, callback=lambda x: f"{x}0")
    with open(file_path, "r") as f:
        content = f.read()
    assert content == "10\n20\n30\n", "File content should match the list"
    os.remove(file_path)


def test_save__list():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save(data, file_path)
    with open(file_path, "r") as f:
        content = f.read()
    assert content == "1\n2\n3\n", "File content should match the list"
    os.remove(file_path)


def test_save__ndarray():
    data = np.array([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".npy"
        save(data, file_path)
    loaded_data = np.load(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded data should match the original array"
    )


def test_save__tensor():
    data = torch.tensor([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save(data, file_path)
    loaded_data = torch.load(file_path)
    assert torch.equal(loaded_data, data), (
        "Loaded data should match the original tensor"
    )


def test_save_image():
    data = np.zeros((100, 100, 3), dtype=np.uint8)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".png"
        save_image(data, file_path)
    loaded_data = cv2.imread(file_path)
    assert loaded_data is not None, "Loaded image should not be None"


def test_load_list():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.writelines(f"{item}\n" for item in data)
    loaded_data = load_list(file_path)
    assert loaded_data == [str(i) for i in data], (
        "Loaded data should match the original list"
    )
    os.remove(file_path)


def test_load_list_with_callback():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.writelines(f"{item}\n" for item in data)
    loaded_data = load_list(file_path, callback=int)
    assert loaded_data == data, "Loaded data should match the original list"
    os.remove(file_path)


def test_load_np():
    data = np.array([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".npy"
        np.save(file_path, data)
    loaded_data = load_np(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded data should match the original array"
    )
    os.remove(file_path)


def test_load_tensor():
    data = torch.tensor([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        torch.save(data, file_path)
    loaded_data = load_tensor(file_path)
    assert torch.equal(loaded_data, data), (
        "Loaded data should match the original tensor"
    )
    os.remove(file_path)


def test_load_file():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.writelines(f"{item}\n" for item in data)
    loaded_data = load_file(file_path)
    assert loaded_data == [str(i) for i in data], (
        "Loaded data should match the original list"
    )
    os.remove(file_path)


def test_load_file__not_a_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(IsADirectoryError):
            load_file(temp_dir)


def test_load_file__non_existent_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "non_existent.txt"
        with pytest.raises(FileNotFoundError):
            load_file(file_path)


def test_load_image():
    data = np.array([[1, 2], [3, 4]], dtype=np.uint8)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".png"
        cv2.imwrite(file_path, data)
    loaded_data = load_image(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded image should match the original array"
    )
    os.remove(file_path)


def test_load_image__non_image_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.write(b"test")
    result = load_image(file_path)
    assert result is None, "Loading a non-image file should return None"
    os.remove(file_path)


def test_load_images():
    data = [np.array([[1, 2], [3, 4]], dtype=np.uint8) for _ in range(3)]
    with tempfile.TemporaryDirectory() as temp_dir:
        file_paths = []
        for i, img in enumerate(data):
            file_path = os.path.join(temp_dir, f"image_{i}.png")
            cv2.imwrite(file_path, img)
            file_paths.append(file_path)
        loaded_data = load_images(file_paths)
    assert len(loaded_data) == len(data), "Loaded data should match the original list"
    for i in range(len(data)):
        assert np.array_equal(loaded_data[i], data[i]), (
            f"Loaded image {i} should match the original image"
        )


def test_load_images__non_existent_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_file = os.path.join(temp_dir, "non_existent.png")
        result = load_images([non_existent_file])
        assert result == [None], "Loading a non-existent file should return [None]"


def test_load_images__empty_list():
    loaded_data = load_images([])
    assert loaded_data == [], "Empty list should return an empty list"


def test_load_images__mixed_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        image_file = os.path.join(temp_dir, "image.png")
        with open(image_file, "wb") as f:
            f.write(b"test")
        non_image_file = os.path.join(temp_dir, "not_a_file.txt")
        with open(non_image_file, "w") as f:
            f.write("test")
        result = load_images([image_file, non_image_file])
        assert result == [None, None], (
            "Loading a non-image file should return [None, None]"
        )
        os.remove(image_file)
        os.remove(non_image_file)
