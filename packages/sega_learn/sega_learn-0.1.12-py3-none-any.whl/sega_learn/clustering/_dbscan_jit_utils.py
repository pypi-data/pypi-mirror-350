import numpy as np
from numba import njit, prange

# The following lines are used to compile the numba functions into shared library
# from numba.pycc import CC
# cc = CC('compiled_dbscan_jit_utils')
# cc.verbose = True


@njit(parallel=True, fastmath=True)
def _identify_core_points(dist_matrix, eps, min_samples):
    """Identify core points based on the distance matrix, eps, and min_samples.

    Args:
        dist_matrix: Pairwise distance matrix.
        eps: Maximum distance for neighbors.
        min_samples: Minimum number of neighbors to be a core point.

    Returns:
        core_points: Boolean array indicating core points.
    """
    n_points = dist_matrix.shape[0]
    core_points = np.zeros(n_points, dtype=np.bool_)

    for i in prange(n_points):
        neighbors = 0
        for j in range(n_points):
            if dist_matrix[i, j] < eps:
                neighbors += 1
        if neighbors >= min_samples:
            core_points[i] = True

    return core_points


@njit(parallel=False, fastmath=True)
def _assign_clusters(dist_matrix, core_points, eps):
    """Assign cluster labels using depth-first search (DFS) starting from core points.

    Args:
        dist_matrix: Pairwise distance matrix.
        core_points: Boolean array indicating core points.
        eps: Maximum distance for neighbors.

    Returns:
        labels: Cluster labels for each data point.
    """
    n_points = dist_matrix.shape[0]
    labels = -1 * np.ones(n_points, dtype=np.int32)
    cluster_id = 0

    for i in range(n_points):
        if labels[i] == -1 and core_points[i]:
            labels[i] = cluster_id
            stack = [i]

            while stack:
                point = stack.pop()
                for j in range(n_points):
                    if dist_matrix[point, j] < eps and labels[j] == -1:
                        labels[j] = cluster_id
                        if core_points[j]:
                            stack.append(j)

            cluster_id += 1

    return labels


# if __name__ == "__main__":
#     cc.compile()
