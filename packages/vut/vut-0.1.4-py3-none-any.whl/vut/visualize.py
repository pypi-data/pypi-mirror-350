from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from vut.palette import ColorMapName, create_palette, template


def plot_palette(
    *,
    name: ColorMapName | None = None,
    palette: NDArray | list[tuple[float, float, float]] = None,
    n: int = 256,
    path: str | Path = "palette.png",
) -> None:
    """Plot a color palette.

    Args:
        name (ColorMapName | None, optional): The name of the colormap to use. Defaults to None.
        palette (NDArray | list[tuple[float, float, float]], optional): A custom color palette. Defaults to None.
        n (int, optional): The number of colors in the colormap. Defaults to 256.
        path (str | Path, optional): The file path to save the plot. Defaults to "palette.png".
    """
    assert name is not None or palette is not None, (
        "Either name or palette must be provided"
    )
    if name is not None:
        cmap = template(n, name)
    else:
        assert palette.ndim == 2, "Palette must be a 2D array"
        cmap = create_palette(palette)
    gradient = np.linspace(0, 1, n)
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.imshow(
        np.vstack((gradient, gradient)),
        aspect="auto",
        cmap=cmap,
        interpolation="nearest",
    )
    ax.set_axis_off()
    plt.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_image(
    data: NDArray,
    path: str | Path = "image.png",
    title: str = None,
    show_axis: bool = False,
    is_jupyter: bool = False,
    return_canvas: bool = False,
) -> NDArray | None:
    """Plot a 3D array as an image.

    Args:
        data (NDArray): The 3D array to plot.
        path (str | Path, optional): The file path to save the image. Defaults to "image.png".
        title (str, optional): The title of the plot. Defaults to None.
        show_axis (bool, optional): Whether to show the axis. Defaults to False.
        is_jupyter (bool, optional): Whether to display the plot in a Jupyter notebook. Defaults to False.
        return_canvas (bool, optional): Whether to return the canvas as a numpy array. Defaults to False.

    Returns:
        NDArray: The canvas as a numpy array if return_canvas is True, otherwise None.
    """
    assert data.ndim == 3, "Data must be a 3D array"

    fig, ax = plt.subplots()
    ax.imshow(data)
    if not show_axis:
        ax.axis("off")

    if title:
        ax.set_title(title)

    plt.tight_layout()

    if return_canvas:
        fig.canvas.draw()
        canvas = np.array(fig.canvas.buffer_rgba())
        plt.close(fig)
        return canvas[:, :, :3]

    if is_jupyter:
        plt.show()
    else:
        plt.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_images(
    data: list[NDArray],
    paths: list[str | Path] | None = None,
    titles: list[str] | None = None,
    show_axis: bool = False,
    is_jupyter: bool = False,
    return_canvas: bool = False,
    ncols: int = None,
    nrows: int = None,
) -> list[NDArray] | None:
    """Plot a list of 3D arrays as images.

    Args:
        data (list[NDArray]): List of 3D arrays to plot.
        paths (list[str | Path] | None): List of file paths to save the images. Defaults to None.
        titles (list[str] | None, optional): List of titles for each plot. Defaults to None.
        show_axis (bool, optional): Whether to show the axis. Defaults to False.
        is_jupyter (bool, optional): Whether to display the plots in a Jupyter notebook. Defaults to False.
        return_canvas (bool, optional): Whether to return the canvases as numpy arrays. Defaults to False.
        ncols (int, optional): Number of columns in the grid layout. Defaults to None.
        nrows (int, optional): Number of rows in the grid layout. Defaults to None.

    Returns:
        list[NDArray]: List of canvases as numpy arrays if return_canvas is True, otherwise None.
    """
    assert all(d.ndim == 3 for d in data), "All data must be 3D arrays"
    assert paths is None or len(paths) == len(data), (
        "Paths must be provided for each image if specified"
    )
    assert titles is None or len(titles) == len(data), (
        "Titles must be provided for each image if specified"
    )

    if paths is None:
        paths = [None] * len(data)
    if titles is None:
        titles = [None] * len(data)

    num_images = len(data)
    if ncols is None and nrows is None:
        ncols = int(np.ceil(np.sqrt(num_images)))
        nrows = int(np.ceil(num_images / ncols))
    elif ncols is None:
        ncols = int(np.ceil(num_images / nrows))
    elif nrows is None:
        nrows = int(np.ceil(num_images / ncols))
    assert ncols * nrows >= num_images, (
        "Number of columns and rows must accommodate all images"
    )

    canvases = []
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3))
    axs = axs.flatten() if nrows > 1 or ncols > 1 else [axs]
    for i, (ax, img, path) in enumerate(zip(axs, data, paths)):
        ax.imshow(img)
        if not show_axis:
            ax.axis("off")
        if titles and titles[i]:
            ax.set_title(titles[i])
        if return_canvas:
            fig.canvas.draw()
            canvas = np.array(fig.canvas.buffer_rgba())
            canvases.append(canvas[:, :, :3])
        elif path:
            plt.savefig(path, bbox_inches="tight")
    plt.tight_layout()
    if return_canvas:
        plt.close(fig)
        return canvases
    if is_jupyter:
        plt.show()
        plt.close(fig)


def plot_feature(
    data: NDArray,
    path: str | Path = "feature.png",
    title: str = None,
    is_jupyter: bool = False,
    return_canvas: bool = False,
    palette: ColorMapName | list[tuple[float, float, float]] | None = "plasma",
) -> NDArray | None:
    """Plot a 2D feature map.

    Args:
        data (NDArray): The 2D array to plot.
        path (str | Path, optional): The file path to save the image. Defaults to "feature.png".
        title (str, optional): The title of the plot. Defaults to None.
        is_jupyter (bool, optional): Whether to display the plot in a Jupyter notebook. Defaults to False.
        return_canvas (bool, optional): Whether to return the canvas as a numpy array. Defaults to False.
        palette (ColorMapName | list[tuple[float, float, float]], optional): The colormap to use. Defaults to "plasma".

    Returns:
        NDArray: The canvas as a numpy array if return_canvas is True, otherwise None.
    """
    assert data.ndim == 2, "Data must be a 2D array"

    fig, ax = plt.subplots()
    cax = ax.imshow(
        data, cmap=create_palette(palette) if isinstance(palette, list) else palette
    )
    if title:
        ax.set_title(title)
    fig.colorbar(cax)

    plt.tight_layout()

    if return_canvas:
        fig.canvas.draw()
        canvas = np.array(fig.canvas.buffer_rgba())
        plt.close(fig)
        return canvas[:, :, :3]

    if is_jupyter:
        plt.show()
        plt.close(fig)
    else:
        plt.savefig(path, bbox_inches="tight")
        plt.close(fig)


def plot_features(
    data: list[NDArray],
    paths: list[str | Path] | None = None,
    titles: list[str] | None = None,
    is_jupyter: bool = False,
    return_canvas: bool = False,
    ncols: int = None,
    nrows: int = None,
    palette: ColorMapName | list[tuple[float, float, float]] | None = "plasma",
) -> list[NDArray] | None:
    """Plot a list of 2D feature maps.

    Args:
        data (list[NDArray]): List of 2D arrays to plot.
        paths (list[str | Path] | None): List of file paths to save the images. Defaults to None.
        titles (list[str] | None, optional): List of titles for each plot. Defaults to None.
        is_jupyter (bool, optional): Whether to display the plots in a Jupyter notebook. Defaults to False.
        return_canvas (bool, optional): Whether to return the canvases as numpy arrays. Defaults to False.
        ncols (int, optional): Number of columns in the grid layout. Defaults to None.
        nrows (int, optional): Number of rows in the grid layout. Defaults to None.
        palette (ColorMapName | list[tuple[float, float, float]], optional): The colormap to use. Defaults to "plasma".

    Returns:
        list[NDArray]: List of canvases as numpy arrays if return_canvas is True, otherwise None.
    """
    assert all(d.ndim == 2 for d in data), "All data must be 2D arrays"
    assert paths is None or len(paths) == len(data), (
        "Paths must be provided for each image if specified"
    )
    assert titles is None or len(titles) == len(data), (
        "Titles must be provided for each image if specified"
    )

    if paths is None:
        paths = [None] * len(data)
    if titles is None:
        titles = [None] * len(data)

    num_features = len(data)
    if ncols is None and nrows is None:
        ncols = int(np.ceil(np.sqrt(num_features)))
        nrows = int(np.ceil(num_features / ncols))
    elif ncols is None:
        ncols = int(np.ceil(num_features / nrows))
    elif nrows is None:
        nrows = int(np.ceil(num_features / ncols))

    canvases = []
    fig, axs = plt.subplots(
        nrows=nrows if nrows is not None else 1,
        ncols=ncols if ncols is not None else len(data),
        figsize=(ncols * 3, nrows * 3) if nrows and ncols else (len(data) * 3, 3),
    )
    axs = axs.flatten() if nrows > 1 or ncols > 1 else [axs]
    for i, (ax, img, path) in enumerate(zip(axs, data, paths)):
        cax = ax.imshow(
            img,
            cmap=create_palette(palette) if isinstance(palette, list) else palette,
        )
        if titles and titles[i]:
            ax.set_title(titles[i])
        fig.colorbar(cax, ax=ax)
        if return_canvas:
            fig.canvas.draw()
            canvas = np.array(fig.canvas.buffer_rgba())
            canvases.append(canvas[:, :, :3])
        elif path:
            plt.savefig(path, bbox_inches="tight")
    plt.tight_layout()
    if return_canvas:
        plt.close(fig)
        return canvases
    if is_jupyter:
        plt.show()
        plt.close(fig)
