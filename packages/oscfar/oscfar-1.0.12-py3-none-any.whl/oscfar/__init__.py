import numpy as np

# Package to do OS-CFAR + Useful filters
__version__ = "1.0.12"

from . import cfar
from . import filters
from . import utils
from . import gaussian_fit
from . import cluster

# OS-CFAR versions
os_cfar = cfar.os_cfar_1d
vwindow_os_cfar = cfar.variable_window_os_cfar_indices

# Filters
baseline_filter = filters.remove_baseline_peaks
lowpass_filter = filters.lowpass_filter
highpass_filter = filters.highpass_filter

median_smoothing = filters.median_filter
mean_smoothing = filters.moving_average_filter

group_peaks = filters.find_representative_peaks
force_min_dist = filters.enforce_min_distance
check_snr = filters.verify_peaks_snr
force_max_extent = filters.filter_peaks_by_extent_1d

# Utilities
peaks = utils.Peaks
waterfall_axes = utils.WaterFallAxes
waterfall_grid = utils.WaterFallGrid
npz_reader = utils.NpzReader
npz_writer = utils.NpzWriter


# Gaussian functions
multi_gaussian = gaussian_fit.sum_of_gaussians
multi_scattered_gaussian = gaussian_fit.sum_of_scattered_gaussians
grid_search_gaussian = gaussian_fit.find_best_multi_gaussian_fit

# Other utilities
best_params = {
    "guard_cells": 1,
    "train_cells": 8,
    "rank_k": 0.75,
    "threshold_factor": 0.9,
    "averaging": 2,
    "min_snr": 2,
    "baseline": 0.15,
}


def do_os_cfar(
    data: np.array,
    guard_cells,
    train_cells,
    rank_k,
    threshold_factor,
    averaging,
    min_dist,
    min_snr,
    baseline,
):
    """
    Performs OS-CFAR detection on a 2D data array (e.g., spectrogram) by summing
    along the frequency axis to create a 1D time series. Applies filtering,
    peak refinement, and baseline removal.

    Args:
        data (np.ndarray): 2D array of input data (frequency vs. time).
        guard_cells (int): Number of guard cells on each side of the CUT.
        train_cells (int): Number of training cells on each side of the CUT.
        rank_k (float): Rank (as a fraction of total training cells) for OS.
        threshold_factor (float): Scaling factor for the threshold.
        averaging (int): Window size for moving average smoothing.
        min_dist (int): Minimum distance between peaks (in samples).
        min_snr (float): Minimum SNR for peak verification.
        baseline (float): Factor for removing baseline peaks.

    Returns:
        utils.Peaks: An object containing the refined peak indices and the
                     threshold array from OS-CFAR.
    """

    ts = np.sum(data, 0)
    stdev = np.std(data, 0)
    mts = np.mean(data, 0)

    filtered = mean_smoothing(ts, averaging)
    res = os_cfar(
        filtered,
        guard_cells,
        train_cells,
        int(rank_k * 2 * train_cells),
        threshold_factor,
    )

    pk = res[0]
    pk = force_min_dist(list(pk), ts, min_dist)
    pk = check_snr(ts, list(pk), min_dist, min_snr)
    pk = group_peaks(ts, list(pk), min_dist)
    pk = baseline_filter(mts, pk, stdev, baseline)

    return peaks((pk, res[1]))
