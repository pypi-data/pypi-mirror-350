from numpy.typing import NDArray
from sklearn.manifold import TSNE


def compute_tsne(
    data: NDArray,
    n_components: int = 2,
    random_state: int | None = 42,
    perplexity: int = None,
) -> NDArray:
    """Compute t-SNE dimensionality reduction.

    Args:
        data (NDArray): Input data matrix of shape (n_samples, n_features).
        n_components (int, optional): Dimension of the embedded space. Defaults to 2.
        random_state (int | None, optional): Random state for reproducibility. Defaults to 42.
        perplexity (int, optional): Perplexity parameter for t-SNE. Defaults to None.

    Returns:
        NDArray: t-SNE embedding of the data with shape (n_samples, n_components).
    """
    if perplexity is None:
        perplexity = min(30, max(1, data.shape[0] - 1))
    tsne = TSNE(
        n_components=n_components,
        random_state=random_state,
        perplexity=perplexity,
    )
    return tsne.fit_transform(data)
