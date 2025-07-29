import numpy as np
from scipy import linalg


def make_regression(
    n_samples=100,
    n_features=100,
    n_informative=10,
    n_targets=1,
    bias=0.0,
    effective_rank=None,
    tail_strength=0.5,
    noise=0.0,
    shuffle=True,
    coef=False,
    random_state=None,
):
    """Generates a random regression problem.

    Args:
        n_samples (int, optional): Number of samples (default is 100).
        n_features (int, optional): Number of features (default is 100).
        n_informative (int, optional): Number of informative features used to build the linear model (default is 10).
        n_targets (int, optional): Number of regression targets (default is 1).
        bias (float, optional): Bias term in the underlying linear model (default is 0.0).
        effective_rank (int or None, optional): Approximate dimension of the data matrix (default is None).
        tail_strength (float, optional): Relative importance of the noisy tail of the singular values profile (default is 0.5).
        noise (float, optional): Standard deviation of the Gaussian noise applied to the output (default is 0.0).
        shuffle (bool, optional): Whether to shuffle the samples and features (default is True).
        coef (bool, optional): If True, returns the coefficients of the underlying linear model (default is False).
        random_state (int or None, optional): Random seed (default is None).

    Returns:
        X (np.ndarray): Input samples of shape (n_samples, n_features).
        y (np.ndarray): Output values of shape (n_samples,) or (n_samples, n_targets).
        coef (np.ndarray, optional): Coefficients of the underlying linear model of shape (n_features,) or (n_features, n_targets). Only returned if coef=True.
    """
    # Set random state
    rng = np.random.RandomState(random_state)

    # Generate random design matrix X
    if effective_rank is None:
        # Generate data of full rank
        X = rng.normal(size=(n_samples, n_features))
    else:
        # Generate data of approximate rank `effective_rank`
        if effective_rank > n_features:
            raise ValueError("effective_rank must be less than n_features")

        # Create covariance matrix with singular values decreasing exponentially
        singular_values = np.zeros(n_features)
        singular_values[:effective_rank] = np.exp(
            -np.arange(effective_rank) / effective_rank * tail_strength
        )
        singular_values[effective_rank:] = singular_values[effective_rank - 1] / 100

        # Create random covariance matrix
        U, _, _ = linalg.svd(
            rng.normal(size=(n_features, n_features)), full_matrices=False
        )
        X = rng.normal(size=(n_samples, 1)) @ np.ones((1, n_features))
        X = np.dot(X, np.dot(U, np.diag(np.sqrt(singular_values))))

    # Generate true coefficients
    if n_informative > n_features:
        n_informative = n_features

    ground_truth = np.zeros((n_features, n_targets))
    ground_truth[:n_informative, :] = rng.normal(size=(n_informative, n_targets))

    # Build output
    y = np.dot(X, ground_truth) + bias

    # Add noise
    if noise > 0.0:
        y += rng.normal(scale=noise, size=y.shape)

    # Shuffle
    if shuffle:
        indices = np.arange(n_samples)
        rng.shuffle(indices)
        X = X[indices]
        y = y[indices]

    if n_targets == 1:
        y = y.ravel()

    if coef:
        return X, y, ground_truth
    else:
        return X, y


def make_classification(
    n_samples=100,
    n_features=20,
    n_informative=2,
    n_redundant=2,
    n_repeated=0,
    n_classes=2,
    n_clusters_per_class=2,
    weights=None,
    flip_y=0.01,
    class_sep=1.0,
    hypercube=True,
    shift=0.0,
    scale=1.0,
    shuffle=True,
    random_state=None,
):
    """Generates a random n-class classification problem.

    Args:
        n_samples (int, optional): Number of samples (default is 100).
        n_features (int, optional): Total number of features (default is 20).
        n_informative (int, optional): Number of informative features (default is 2).
        n_redundant (int, optional): Number of redundant features (default is 2).
        n_repeated (int, optional): Number of duplicated features (default is 0).
        n_classes (int, optional): Number of classes (default is 2).
        n_clusters_per_class (int, optional): Number of clusters per class (default is 2).
        weights (array-like, optional): Proportions of samples assigned to each class (default is None).
        flip_y (float, optional): Fraction of samples whose class is randomly exchanged (default is 0.01).
        class_sep (float, optional): Factor multiplying the hypercube size (default is 1.0).
        hypercube (bool, optional): If True, clusters are placed on the vertices of a hypercube (default is True).
        shift (float, optional): Shift features by the specified value (default is 0.0).
        scale (float, optional): Multiply features by the specified value (default is 1.0).
        shuffle (bool, optional): Shuffle the samples and features (default is True).
        random_state (int or None, optional): Random seed (default is None).

    Returns:
        X (np.ndarray): Generated samples of shape (n_samples, n_features).
        y (np.ndarray): Integer labels for class membership of each sample of shape (n_samples,).
    """
    # Set random state
    rng = np.random.RandomState(random_state)

    # Calculate actual number of features
    n_useless = n_features - n_informative - n_redundant - n_repeated
    if n_useless < 0:
        raise ValueError(
            "n_features must be greater or equal to n_informative + n_redundant + n_repeated"
        )

    # Normalize weights
    if weights is not None:
        weights = np.asarray(weights)
        if weights.shape[0] != n_classes:
            raise ValueError("weights must be of length n_classes")
        weights_sum = np.sum(weights)
        if weights_sum <= 0:
            raise ValueError("weights must sum to a positive value")
        weights = weights / weights_sum
    else:
        weights = np.ones(n_classes) / n_classes

    # Calculate samples per class
    n_samples_per_class = np.random.multinomial(n_samples, weights)

    # Initialize data matrices
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)

    # --- New: Generate a class center for each class ---
    class_centers = rng.randn(n_classes, n_informative)
    if hypercube:
        class_centers = np.sign(class_centers)
    class_centers *= class_sep

    # Define a scale for cluster offsets (small relative to class_sep)
    offset_scale = 0.1 * class_sep

    start = 0
    for i in range(n_classes):
        n_samples_i = n_samples_per_class[i]
        if n_samples_i <= 0:
            continue
        end = start + n_samples_i
        y[start:end] = i

        # For each class, create cluster centers as offsets from the class center
        centroids = (
            class_centers[i]
            + rng.randn(n_clusters_per_class, n_informative) * offset_scale
        )

        # Get samples for each cluster
        n_samples_per_cluster = np.random.multinomial(
            n_samples_i, [1 / n_clusters_per_class] * n_clusters_per_class
        )

        cluster_start = 0
        for j, n_cluster_samples in enumerate(n_samples_per_cluster):
            if n_cluster_samples <= 0:
                continue
            cluster_end = cluster_start + n_cluster_samples
            X_cluster = rng.randn(n_cluster_samples, n_informative)
            X_cluster += centroids[j]
            X[start + cluster_start : start + cluster_end, :n_informative] = X_cluster
            cluster_start = cluster_end

        start = end

    # Add redundant features (linear combinations of informative ones)
    if n_redundant > 0:
        B = rng.randn(n_informative, n_redundant)
        X[:, n_informative : n_informative + n_redundant] = np.dot(
            X[:, :n_informative], B
        )

    # Add repeated features (copies of some of the first n_informative+n_redundant columns)
    if n_repeated > 0:
        indices = rng.choice(n_informative + n_redundant, n_repeated, replace=True)
        X[:, n_informative + n_redundant : n_informative + n_redundant + n_repeated] = (
            X[:, indices]
        )

    # Add useless features (noise)
    if n_useless > 0:
        X[:, -n_useless:] = rng.randn(n_samples, n_useless)

    # Apply shift and scale
    X = X * scale + shift

    # Flip labels (ensure changed labels)
    if flip_y > 0.0:
        flip_mask = rng.rand(n_samples) < flip_y
        if n_classes == 2:
            y[flip_mask] = 1 - y[flip_mask]
        else:
            random_labels = rng.randint(0, n_classes, size=np.sum(flip_mask))
            same = random_labels == y[flip_mask]
            random_labels[same] = (y[flip_mask][same] + 1) % n_classes
            y[flip_mask] = random_labels

    # Shuffle samples and features
    if shuffle:
        indices = np.arange(n_samples)
        rng.shuffle(indices)
        X = X[indices]
        y = y[indices]

        feature_indices = np.arange(n_features)
        rng.shuffle(feature_indices)
        X = X[:, feature_indices]

    return X, y


def make_blobs(
    n_samples=100,
    n_features=2,
    centers=None,
    cluster_std=1.0,
    center_box=(-10.0, 10.0),
    shuffle=True,
    random_state=None,
):
    """Generates isotropic Gaussian blobs for clustering.

    Args:
        n_samples (int or array-like, optional): Total number of samples if int, or number of samples per cluster if array-like (default is 100).
        n_features (int, optional): Number of features (default is 2).
        centers (int or array-like, optional): Number of centers to generate, or fixed center locations. If None, 3 centers are generated (default is None).
        cluster_std (float or array-like, optional): Standard deviation of the clusters (default is 1.0).
        center_box (tuple of float, optional): Bounding box for each cluster center when centers are generated at random (default is (-10.0, 10.0)).
        shuffle (bool, optional): Whether to shuffle the samples (default is True).
        random_state (int or None, optional): Random seed (default is None).

    Returns:
        X (np.ndarray): Generated samples of shape (n_samples, n_features).
        y (np.ndarray): Integer labels for cluster membership of each sample of shape (n_samples,).
        centers (np.ndarray): Centers of each cluster of shape (n_centers, n_features).
    """
    # Set random state
    rng = np.random.RandomState(random_state)

    # Handle n_samples
    if isinstance(n_samples, (list, tuple)):
        n_samples_per_center = n_samples
        n_centers = len(n_samples_per_center)
        n_samples = sum(n_samples_per_center)
        if centers is None:
            centers = rng.uniform(
                center_box[0], center_box[1], size=(n_centers, n_features)
            )
        else:
            centers = np.asarray(centers)
            if centers.shape[0] != n_centers:
                raise ValueError("centers must have shape (n_centers, n_features)")
    else:
        if centers is None:
            n_centers = 3
            centers = rng.uniform(
                center_box[0], center_box[1], size=(n_centers, n_features)
            )
        elif isinstance(centers, int):
            n_centers = centers
            centers = rng.uniform(
                center_box[0], center_box[1], size=(n_centers, n_features)
            )
        else:
            centers = np.asarray(centers)
            n_centers = centers.shape[0]
        n_samples_per_center = [n_samples // n_centers] * n_centers
        remainder = n_samples % n_centers
        for i in range(remainder):
            n_samples_per_center[i] += 1

    # Handle cluster_std
    if np.isscalar(cluster_std):
        cluster_std = np.ones(n_centers) * cluster_std
    else:
        cluster_std = np.asarray(cluster_std)

    # Get n_features from centers
    n_features = centers.shape[1]

    # Initialize data matrices
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)

    # Build data
    start = 0
    for i, (n, std) in enumerate(zip(n_samples_per_center, cluster_std)):
        end = start + n
        X[start:end] = centers[i] + rng.normal(scale=std, size=(n, n_features))
        y[start:end] = i
        start = end

    # Shuffle
    if shuffle:
        indices = np.arange(n_samples)
        rng.shuffle(indices)
        X = X[indices]
        y = y[indices]

    return X, y, centers


def make_time_series(
    n_samples=100,
    n_timestamps=50,
    n_features=1,
    trend="linear",
    seasonality="sine",
    seasonality_period=None,
    noise=0.1,
    random_state=None,
):
    """Generates synthetic time series data.

    Args:
        n_samples (int, optional): Number of time series samples (default is 100).
        n_timestamps (int, optional): Number of timestamps per sample (default is 50).
        n_features (int, optional): Number of features per timestamp (default is 1).
        trend (str, optional): Type of trend ('linear', 'quadratic', or None) (default is 'linear').
        seasonality (str, optional): Type of seasonality ('sine', 'cosine', or None) (default is 'sine').
        seasonality_period (int, optional): Period of the seasonality (default is None, which uses the length of the time series/2).
        noise (float, optional): Standard deviation of Gaussian noise (default is 0.1).
        random_state (int or None, optional): Random seed (default is None).

    Returns:
        X (np.ndarray): Time series data of shape (n_samples, n_timestamps, n_features).
    """
    # Verify trend and seasonality
    if trend not in ["linear", "quadratic", None]:
        raise ValueError("trend must be 'linear', 'quadratic', or None")
    if seasonality not in ["sine", "cosine", None]:
        raise ValueError("seasonality must be 'sine', 'cosine', or None")
    if seasonality_period is not None and seasonality_period <= 0:
        raise ValueError("seasonality_period must be a positive integer")

    if seasonality_period is None:
        seasonality_period = n_timestamps // 2

    rng = np.random.RandomState(random_state)

    # Initialize time series data
    X = np.zeros((n_samples, n_timestamps, n_features))

    # Generate time points
    t = np.linspace(0, 1, n_timestamps)

    for i in range(n_samples):
        for j in range(n_features):
            # Add trend
            if trend == "linear":
                series = t
            elif trend == "quadratic":
                series = t**2
            else:
                series = np.zeros_like(t)

            # Add seasonality
            if seasonality == "sine":
                series += np.sin(
                    2 * np.pi * np.arange(n_timestamps) / seasonality_period
                ) / np.max(
                    np.abs(
                        np.sin(2 * np.pi * np.arange(n_timestamps) / seasonality_period)
                    )
                )
            elif seasonality == "cosine":
                series += np.cos(
                    2 * np.pi * np.arange(n_timestamps) / seasonality_period
                ) / np.max(
                    np.abs(
                        np.cos(2 * np.pi * np.arange(n_timestamps) / seasonality_period)
                    )
                )

            # Add noise
            series += rng.normal(scale=noise, size=t.shape)

            X[i, :, j] = series

    return X
