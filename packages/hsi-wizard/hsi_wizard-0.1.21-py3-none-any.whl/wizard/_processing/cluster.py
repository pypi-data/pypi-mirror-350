"""
_processing/cluster.py
========================

.. module:: cluster
:platform: Unix
:synopsis: Initialization of the exploration package for hsi-wizard.

Module Overview
---------------

This module initializes the cluster functions of the hsi-wizard package.

Functions
---------

.. autofunction:: quit_low_change_in_clusters
.. autofunction:: discard_clusters


Credits
-------
The Isodata code was inspired by:
- Repository: pyRadar
- Author/Organization: PyRadar
- Original repository: https://github.com/PyRadar/pyradar/

"""
import numpy as np
from scipy.cluster.vq import vq
from typing import Tuple
from typing import Optional
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from scipy.signal import convolve2d


def quit_low_change_in_clusters(centers: np.ndarray, last_centers: np.ndarray, theta_o: float) -> bool:
    """
    Stop algorithm by low change in the clusters values between each iteration.

    :param centers: Cluster centers
    :param last_centers: Last cluster centers
    :param theta_o: threshold change in the clusters between each iter
    :return: True if it should stop, otherwise False.
    """
    qt = False
    if centers.shape == last_centers.shape:
        thresholds = np.abs((centers - last_centers) / (last_centers + 1))

        if np.all(thresholds <= theta_o):  # percent of change in [0:1]
            qt = True

    return qt


def discard_clusters(img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Discard clusters with fewer than theta_m.

    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param theta_m: threshold value for min number in each cluster
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    k_ = centers.shape[0]
    to_delete = np.array([])
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        total_per_cluster = indices.size
        if total_per_cluster <= theta_m:
            to_delete = np.append(to_delete, cluster)

    if to_delete.size:
        to_delete = np.array(to_delete, dtype=int)
        new_centers = np.delete(centers, to_delete, axis=0)
        new_clusters_list = np.delete(clusters_list, to_delete)
    else:
        new_centers = centers
        new_clusters_list = clusters_list

    # new_centers, new_clusters_list = sort_arrays_by_first(new_centers, new_clusters_list)
    assert new_centers.shape[0] == new_clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"

    return new_centers, new_clusters_list, k_


def update_clusters(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Update clusters.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    k_ = centers.shape[0]
    new_centers = np.zeros((k_, img_flat.shape[1]))
    new_clusters_list = np.array([])

    if centers.shape[0] != clusters_list.size:
        raise ValueError(
            "ERROR: update_clusters() centers and clusters_list size are different"
        )

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        # get whole cluster
        cluster_values = img_flat[indices, :]
        new_cluster = cluster_values.mean(axis=0)
        new_centers[cluster, :] = new_cluster
        new_clusters_list = np.append(new_clusters_list, cluster)

    new_centers, new_clusters_list = sort_arrays_by_first(new_centers, new_clusters_list)

    if new_centers.shape[0] != new_clusters_list.size:
        raise ValueError(
            "ERROR: update_clusters() centers and clusters_list size are different after sorting"
        )

    return new_centers, new_clusters_list, k_


def initial_clusters(img_flat: np.ndarray, k_: int, method: str = "linspace") -> np.ndarray | None:
    """
    Define initial clusters centers as startup.

    By default, the method is "linspace". Other method available is "random".

    :param img_flat: Flatten image
    :param k_:
    :param method: Method for initially defining cluster centers
    :return: Initial cluster centers
    """
    methods_available = ["linspace", "random"]
    v = img_flat.shape[1]
    assert method in methods_available, f"ERROR: method {method} is not valid."
    if method == "linspace":
        maximum, minimum = img_flat.max(axis=0), img_flat.min(axis=0)
        centers = np.array([np.linspace(minimum[i], maximum[i], k_) for i in range(v)]).T
    elif method == "random":
        start, end = 0, img_flat.shape[0]
        indices = np.random.randint(start, end, k_)
        centers = img_flat[indices]
    else:
        return None

    return centers


def sort_arrays_by_first(centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sort the array 'centers' and with the indices of the sorted centers order the array 'clusters_list'.

    Example: centers=[22, 33, 0, 11] and cluster_list=[7,6,5,4]
    returns  (array([ 0, 11, 22, 33]), array([5, 4, 7, 6]))

    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple of the sorted centers and the sorted cluster list
    """
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: sort_arrays_by_first centers and clusters_list size are not equal"

    indices = np.argsort(centers[:, 0])

    sorted_centers = centers[indices, :]
    sorted_clusters_list = clusters_list[indices]

    return sorted_centers, sorted_clusters_list


def split_clusters(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, theta_s: float, theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Split clusters to form new clusters.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param theta_s: threshold value for standard deviation (for split)
    :param theta_m: threshold value for min number in each cluster
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    assert centers.shape[0] == clusters_list.size, "ERROR: split() centers and clusters_list size are different"

    delta = 10
    k_ = centers.shape[0]
    count_per_cluster = np.zeros(k_)
    stddev = np.array([])

    avg_dists_to_clusters, k_ = compute_avg_distance(img_flat, img_class_flat, centers, clusters_list)
    d, k_ = compute_overall_distance(img_class_flat, avg_dists_to_clusters, clusters_list)

    # compute all the standard deviation of the clusters
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        count_per_cluster[cluster] = indices.size
        value = ((img_flat[indices] - centers[cluster]) ** 2).sum()
        value /= count_per_cluster[cluster]
        value = np.sqrt(value)
        stddev = np.append(stddev, value)

    cluster = stddev.argmax()
    max_stddev = stddev[cluster]
    max_clusters_list = int(clusters_list.max())

    if max_stddev > theta_s:
        if avg_dists_to_clusters[cluster] >= d:
            if count_per_cluster[cluster] > (2.0 * theta_m):
                old_cluster = centers[cluster, :]

                new_cluster_1 = old_cluster + delta
                new_cluster_1 = new_cluster_1.reshape(1, -1)
                new_cluster_2 = old_cluster - delta
                new_cluster_2 = new_cluster_2.reshape(1, -1)

                centers = np.delete(centers, cluster, axis=0)
                clusters_list = np.delete(clusters_list, cluster)

                centers = np.concatenate((centers, new_cluster_1), axis=0)
                centers = np.concatenate((centers, new_cluster_2), axis=0)
                clusters_list = np.append(clusters_list, max_clusters_list + 1)
                clusters_list = np.append(clusters_list, max_clusters_list + 2)

                centers, clusters_list = sort_arrays_by_first(centers, clusters_list)

                assert centers.shape[0] == clusters_list.size, \
                    "ERROR: split() centers and clusters_list size are different"

    return centers, clusters_list, k_


def compute_avg_distance(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Computes all the average distances to the center in each cluster.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple containing the average distances as well as the value for k_
    """
    k_ = centers.shape[0]
    avg_dists_to_clusters = np.zeros(k_)

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]

        cluster_points = img_flat[indices]
        avg_dists_to_clusters[cluster] = np.mean(np.linalg.norm(cluster_points - centers[cluster], axis=1))

    return avg_dists_to_clusters, k_


def compute_overall_distance(img_class_flat: np.ndarray, avg_dists_to_clusters: np.ndarray, clusters_list: np.ndarray) -> Tuple[float, int]:
    """
    Computes the overall distance of the samples from their respective cluster centers.

    :param img_class_flat: Classes of the flatten image
    :param avg_dists_to_clusters: Average distances
    :param clusters_list: List of clusters
    :return: Tuple containing the overall distances as well the value for k_
    """
    k_ = avg_dists_to_clusters.size
    total_count = 0
    total_dist = 0

    for cluster in range(k_):
        nbr_points = len(np.where(img_class_flat == clusters_list[cluster])[0])
        total_dist += avg_dists_to_clusters[cluster] * nbr_points
        total_count += nbr_points

    d = total_dist / total_count

    return d, k_


def merge_clusters(img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, p: int, theta_c: int, k_: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Merge by pair of clusters in 'below_threshold' to form new clusters.

    Todo: adaptation for 3d images
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param p: max number of pairs of clusters which can be merged
    :param theta_c: threshold value for pairwise distances (for merge)
    :param k_:
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    pair_dists = compute_pairwise_distances(centers)

    first_p_elements = pair_dists[:p]
    below_threshold = [(c1, c2) for d, (c1, c2) in first_p_elements if d < theta_c]

    if below_threshold:
        k_ = centers.size
        count_per_cluster = np.zeros(k_)
        to_add = np.array([])  # new clusters to add
        to_delete = np.array([])  # clusters to delete

        for cluster in range(k_):
            result = np.where(img_class_flat == clusters_list[cluster])
            indices = result[0]
            count_per_cluster[cluster] = indices.size

        for c1, c2 in below_threshold:
            c1_count = float(count_per_cluster[c1]) + 1
            c2_count = float(count_per_cluster[c2])
            factor = 1.0 / (c1_count + c2_count)
            weight_c1 = c1_count * centers[c1]
            weight_c2 = c2_count * centers[c2]

            value = round(factor * (weight_c1 + weight_c2))

            to_add = np.append(to_add, value)
            to_delete = np.append(to_delete, [c1, c2])

        # delete old clusters and their indices from the available array
        centers = np.delete(centers, to_delete)
        clusters_list = np.delete(clusters_list, to_delete)

        # generate new indices for the new clusters
        # starting from the max index 'to_add.size' times
        start = int(clusters_list.max())
        end = to_add.size + start

        centers = np.append(centers, to_add)
        clusters_list = np.append(clusters_list, range(start, end))

        centers, clusters_list = sort_arrays_by_first(centers, clusters_list)

    return centers, clusters_list, k_


def compute_pairwise_distances(centers: np.ndarray) -> list:
    """
    Compute the pairwise distances 'pair_dists', between every two clusters centers and returns them sorted.

    Todo: adaptation for 3d images
    :param centers: Cluster centers
    :return: a list with tuples, where every tuple has in its first coord the distance between to clusters, and in the
    second coord has a tuple, with the numbers of the clusters measured
    """
    pair_dists = []

    for i in range(centers.shape[0]):
        for j in range(i):
            # Compute the Euclidean distance using np.linalg.norm
            d = np.linalg.norm(centers[i] - centers[j])
            pair_dists.append((d, (i, j)))

    # Sort by the computed distance (the first element in the tuple)
    return sorted(pair_dists, key=lambda x: x[0])


def isodata(dc, k: int = 10, it: int = 10, p: int = 2, theta_m: int = 10,
            theta_s: float = 0.1, theta_c: int = 2, theta_o: float = 0.05,
            k_: Optional[int] = None) -> np.ndarray:
    """
    Classifies an image stored in a DataCube using the ISODATA clustering algorithm.

    :param dc: DataCube containing the image data.
    :param k: Initial number of clusters.
    :param it: Maximum number of iterations.
    :param p: Maximum number of cluster pairs allowed to merge.
    :param theta_m: Minimum number of pixels required per cluster.
    :param theta_s: Standard deviation threshold for cluster splitting.
    :param theta_c: Distance threshold for cluster merging.
    :param theta_o: Minimum change in cluster centers to continue iterating.
    :return: A 2D numpy array with the classified image.
    """
    img = np.transpose(dc.cube, (1, 2, 0))  # Rearrange cube dimensions to (H, W, Channels)

    if k_ is None:
        k_ = k

    x, y, _ = img.shape
    img_flat = img.reshape(-1, img.shape[2])  # Flatten spatial dimensions
    clusters_list = np.arange(k_)
    centers = initial_clusters(img_flat, k_, "linspace")

    for i in range(it):
        last_centers = centers.copy()

        # Assign samples to the nearest cluster center
        img_class_flat, _ = vq(img_flat, centers)

        # Discard underpopulated clusters
        centers, clusters_list, k_ = discard_clusters(img_class_flat, centers, clusters_list, theta_m)

        # Update cluster centers
        centers, clusters_list, k_ = update_clusters(img_flat, img_class_flat, centers, clusters_list)

        # Handle excessive or insufficient clusters
        if k_ <= (k / 2.0):  # Too few clusters -> Split clusters
            centers, clusters_list, k_ = split_clusters(img_flat, img_class_flat, centers, clusters_list, theta_s, theta_m)
        elif k_ > (k * 2.0):  # Too many clusters -> Merge clusters
            centers, clusters_list, k_ = merge_clusters(img_class_flat, centers, clusters_list, p, theta_c, k_)

        # Terminate early if cluster changes are minimal
        if quit_low_change_in_clusters(centers, last_centers, theta_o):
            break

    return img_class_flat.reshape(x, y)


def generate_gaussian_kernel(size=3, sigma=1.0):
    """Generates a Gaussian-like kernel dynamically."""
    ax = np.linspace(-(size // 2), size // 2, size)
    gauss = np.exp(-0.5 * (ax / sigma) ** 2)
    kernel = np.outer(gauss, gauss)
    return kernel / kernel.sum()


def optimal_clusters(pixels, max_clusters=5, threshold=0.1) -> int:
    """
    Determine the optimal number of KMeans clusters based on minimum centroid distances.

    The function iteratively fits KMeans clustering with increasing values of k (from 2 up to `max_clusters`)
    and evaluates the minimum distance between any two cluster centers. Clustering stops when this distance
    falls below the specified `threshold`, indicating the clusters are getting too close together.

    :param pixels: np.ndarray
        A 1D NumPy array representing the data to be clustered.
    :param max_clusters: int, optional (default=5)
        The maximum number of clusters to evaluate.
    :param threshold: float, optional (default=0.1)
        The minimum allowable distance between cluster centroids.
        Clustering stops when the closest centroids are within this threshold.

    :return: int
        The optimal number of clusters based on the centroid distance threshold.
    """
    best_k = 2
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_
        dists = pairwise_distances(centers)
        np.fill_diagonal(dists, np.inf)  # Ignore self-distances
        closest_dist = np.min(dists)
        if closest_dist > threshold:
            best_k = k
        else:
            break
    return best_k


def segment_cube(dc, n_clusters=5, threshold=.1, mrf_iterations=5, kernel_size=12, sigma=1.0):
    """
    Segments a data cube using both spectral clustering (KMeans) and spatial smoothing (MRF-based regularization).

    :param dc: wizard.DataCube
        3D array where each voxel has a spectrum (v, x, y)
    :param n_clusters: int
        Number of clusters for segmentation
    :param mrf_iterations: int
        Number of iterations for spatial regularization
    :param kernel_size: int
        Size of the Gaussian smoothing kernel
    :param sigma: float
        Standard deviation for Gaussian kernel

    :return: segmented
    :rtype: np.ndarray
        2D array with cluster labels
    """
    v, x, y = dc.shape

    # Reshape cube for clustering
    pixels = dc.cube.reshape(v, -1).T

    # Determine optimal number of clusters
    optimal_k = optimal_clusters(pixels, max_clusters=n_clusters, threshold=threshold)
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    labels = labels.reshape(x, y)

    # Generate dynamic Gaussian kernel
    kernel = generate_gaussian_kernel(size=kernel_size, sigma=sigma)

    # Apply Markov Random Field-based spatial regularization
    for _ in range(mrf_iterations):
        smoothed_labels = np.zeros_like(labels, dtype=np.float64)
        for cluster in range(optimal_k):
            binary_mask = (labels == cluster).astype(np.float64)
            smoothed_mask = convolve2d(binary_mask, kernel, mode='same', boundary='symm')
            smoothed_labels += cluster * smoothed_mask
        labels = np.round(smoothed_labels).astype(np.int32)

    return labels
