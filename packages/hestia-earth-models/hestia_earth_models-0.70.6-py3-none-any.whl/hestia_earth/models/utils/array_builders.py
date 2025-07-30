"""
Based on code by Cool Farm Tool:
https://gitlab.com/MethodsCFT/coolfarm-soc/-/blob/main/src/cfasoc/builders.py
"""
import hashlib
from numpy import cumsum, dot, full, linalg, hstack, random, mean, vstack
from numpy.typing import NDArray, DTypeLike
from typing import Union

from .stats import calc_z_critical, truncnorm_rvs


def repeat_single(shape: tuple, value: float, dtype: DTypeLike = None) -> NDArray:
    """
    Repeat a single value to form an array of a defined shape.

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    value : float
        Value to be repeated.
    dtype : DTypeLike, optional
        The desired data-type for the array.

    Returns
    -------
    NDArray
        Array with repeated value.
    """
    return full(shape=shape, fill_value=value, dtype=dtype)


def repeat_array_as_columns(n_iterations: int, arr: NDArray) -> NDArray:
    """
    Repeat a numpy array horizontally as columns.

    Parameters
    ----------
    n_iterations : int
        Number of times the columns should be repeated.
    arr : NDArray
        Array to repeat.

    Returns
    -------
    NDArray
        Repeated array.
    """
    return hstack([arr for _ in range(n_iterations)])


def repeat_array_as_rows(n_iterations: int, arr: NDArray) -> NDArray:
    """
    Repeat a numpy array vertically as rows.

    Parameters
    ----------
    n_iterations : int
        Number of times the rows should be repeated.
    arr : NDArray
        Array to repeat.

    Returns
    -------
    NDArray
        Repeated array.
    """
    return vstack([arr for _ in range(n_iterations)])


def repeat_1d_array_as_columns(n_columns: int, column: NDArray) -> NDArray:
    """
    Repeat a column (NDArray) to form an array of a defined shape

    Parameters
    ----------
    n_columns : int
        How many times the column (NDArray) should be repeated.
    column : NDArray
        The column (NDArray) to be repeated.

    Returns
    -------
    NDArray
        Repeated array.
    """
    return vstack([column for _ in range(n_columns)]).transpose()


def discrete_uniform_1d(
    shape: tuple, low: float, high: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a discrete uniform distribution and produce an array of a specified shape.
    All rows in a specified column will have the same sample value, but each column will be different (1 dimensional
    variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    low : float
        Lower bound of the discrete uniform distribution to be sampled.
    high : float
        Upper bound of the discrete uniform distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 1 dimensional variability.
    """
    n_rows, n_columns = shape
    rng = random.default_rng(seed)
    return repeat_array_as_rows(
        n_rows,
        rng.uniform(low=low, high=high, size=n_columns)
    )


def discrete_uniform_2d(
    shape: tuple, low: float, high: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a discrete uniform distribution and produce an array of a specified shape.
    All rows and columns contain different sample values (2 dimensional variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    low : float
        Lower bound of the discrete uniform distribution to be sampled.
    high : float
        Upper bound of the discrete uniform distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 2 dimensional variability.
    """
    rng = random.default_rng(seed)
    return rng.uniform(low=low, high=high, size=shape)


def triangular_1d(
    shape: tuple, low: float, high: float, mode: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a triangular distribution and produce an array of a specified shape.
    All rows in a specified column will have the same sample value, but each column will be different (1 dimensional
    variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    low : float
        Lower bound of the triangular distribution to be sampled.
    high : float
        Upper bound of the triangular distribution to be sampled.
    mode : float
        Mode of the triangular distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 1 dimensional variability.
    """
    n_rows, n_columns = shape
    rng = random.default_rng(seed)
    return repeat_array_as_rows(
        n_rows,
        rng.triangular(left=low, mode=mode, right=high, size=n_columns)
    )


def triangular_2d(
    shape: tuple, low: float, high: float, mode: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a triangular distribution and produce an array of a specified shape.
    All rows and columns contain different sample values (2 dimensional variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    low : float
        Lower bound of the triangular distribution to be sampled.
    high : float
        Upper bound of the triangular distribution to be sampled.
    mode : float
        Mode of the triangular distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 2 dimensional variability.
    """
    rng = random.default_rng(seed)
    return rng.triangular(left=low, mode=mode, right=high, size=shape)


def normal_1d(
    shape: tuple, mu: float, sigma: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a normal distribution and produce an array of a specified shape.
    All rows in a specified column will have the same sample value, but each column will be different (1 dimensional
    variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    mu : float
        Mean of the normal distribution to be sampled.
    sigma : float
        Standard deviation of the normal distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 1 dimensional variability.
    """
    n_rows, n_columns = shape
    rng = random.default_rng(seed)
    return repeat_array_as_rows(
        n_rows,
        rng.normal(loc=mu, scale=sigma, size=n_columns)
    )


def normal_2d(
    shape: tuple, mu: float, sigma: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a normal distribution and produce an array of a specified shape.
    All rows and columns contain different sample values (2 dimensional variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    mu : float
        Mean of the normal distribution to be sampled.
    sigma : float
        Standard deviation of the normal distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 2 dimensional variability.
    """
    rng = random.default_rng(seed)
    return rng.normal(loc=mu, scale=sigma, size=shape)


def truncated_normal_1d(
    shape: tuple, mu: float, sigma: float, low: float, high: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a truncated normal distribution and produce an array of a specified shape.
    All rows in a specified column will have the same sample value, but each column will be different (1 dimensional
    variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    mu : float
        Mean of the normal distribution to be sampled.
    sigma : float
        Standard deviation of the normal distribution to be sampled.
    low : float
        Lower bound of the normal distribution to be sampled.
    high : float
        Upper bound of the normal distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 1 dimensional variability.
    """
    n_rows, n_columns = shape
    return repeat_array_as_rows(
        n_rows,
        truncnorm_rvs(a=low, b=high, loc=mu, scale=sigma, shape=n_columns, seed=seed)
    )


def truncated_normal_2d(
    shape: tuple, mu: float, sigma: float, low: float, high: float, seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Sample from a truncated normal distribution and produce an array of a specified shape.
    All rows and columns contain different sample values (2 dimensional variability).

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    mu : float
        Mean of the normal distribution to be sampled.
    sigma : float
        Standard deviation of the normal distribution to be sampled.
    low : float
        Lower bound of the normal distribution to be sampled.
    high : float
        Upper bound of the normal distribution to be sampled.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 2 dimensional variability.
    """
    return truncnorm_rvs(a=low, b=high, loc=mu, scale=sigma, shape=shape, seed=seed)


def plus_minus_uncertainty_to_normal_1d(
    shape: tuple,
    value: float,
    uncertainty: float,
    confidence_interval: float = 95,
    seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Return a normally distributed sample given a value and uncertainty expressed as +/- a percentage.

    All rows in a specified column will have the same sample value, but each column will be different (1 dimensional
    variability).

    This function has been written to serve Table 5.5b on Page 5.32, Tier 2 Steady State Method for Mineral Soils,
    Chapter 5 Cropland, 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories. Table 5.5b
    notes:

        "Uncertainty is assumed to be ±75% for the N content estimates and ±50% for the lignin content estimates,
        expressed as a 95% confidence intervals."

    This function also serves Table 11.2 on Page 11.19, Tier 2 Steady State Method for Mineral Soils, Chapter 11 N2O
    Emissions from Managed Soils, and CO2 Emissions from Lime and Urea Application, 2019 Refinement to the 2006 IPCC
    Guidelines for National Greenhouse Gas Inventories.

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    value : float
        Reported value.
    uncertainty : float
        Uncertainty expressed as +/- a percentage.
    confidence_interval : float
        Confidence interval the uncertainty represents.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 1 dimensional variability.
    """
    n_rows, n_columns = shape
    n_sds = calc_z_critical(confidence_interval)
    sigma = (value * (uncertainty / 100)) / n_sds
    return repeat_array_as_rows(
        n_rows,
        normal_1d(shape=(1, n_columns), mu=value, sigma=sigma, seed=seed)
    )


def plus_minus_uncertainty_to_normal_2d(
    shape: tuple,
    value: float,
    uncertainty: float,
    confidence_interval: float = 95,
    seed: Union[int, random.Generator, None] = None
) -> NDArray:
    """
    Return a normally distributed sample given a value and uncertainty expressed as +/- a percentage.

    All rows and columns contain different sample values (2 dimensional variability).

    This function has been written to serve Table 5.5b on Page 5.32, Tier 2 Steady State Method for Mineral Soils,
    Chapter 5 Cropland, 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories. Table 5.5b
    notes:

        "Uncertainty is assumed to be ±75% for the N content estimates and ±50% for the lignin content estimates,
        expressed as a 95% confidence intervals."

    This function also serves Table 11.2 on Page 11.19, Tier 2 Steady State Method for Mineral Soils, Chapter 11 N2O
    Emissions from Managed Soils, and CO2 Emissions from Lime and Urea Application, 2019 Refinement to the 2006 IPCC
    Guidelines for National Greenhouse Gas Inventories.

    Parameters
    ----------
    shape : tuple
        Shape (rows, columns).
    value : float
        Reported value.
    uncertainty : float
        Uncertainty expressed as +/- a percentage.
    confidence_interval : float
        Confidence interval the uncertainty represents.
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        Array of samples with 2 dimensional variability.
    """
    n_sds = calc_z_critical(confidence_interval)
    sigma = (value * (uncertainty / 100)) / n_sds
    return normal_2d(shape=shape, mu=value, sigma=sigma, seed=seed)


def grouped_avg(arr: NDArray, n: int = 12) -> NDArray:
    """ Row-wise averaging of numpy arrays. For example:
    1   2   3
    4   5   6
    7   8   9
    10  11  12
    13  14  15
    16  17  18

    if n = 6, becomes:
    8.5 9.5 10.5

    because:
    (1 + 4 + 7 + 10 + 13 + 16) / 6 = 8.5
    (2 + 5 + 8 + 11 + 14 + 17) / 6 = 9.5
    etc.

    if n = 2, becomes:
    2.5  3.5  4.5
    8.5  9.5  10.5
    14.5 15.5 16.5

    because:
    (in column 0) (1 + 4) / 2 = 2.5, (7 + 10) / 2 = 8.5, (13 + 16) / 2 = 14.5
    (in column 1) (2 + 5) / 2 = 3.5, (8 + 11) / 2 = 9.5, (14 + 17) / 2 = 15.5

    Source: https://stackoverflow.com/questions/30379311/fast-way-to-take-average-of-every-n-rows-in-a-npy-array

    Parameters
    ----------
    arr : NDArray
        Input array.
    n : int, optional
        Number of rows to average. Defaults to 12.

    Returns
    -------
    NDArray
        Output array
    """
    result = cumsum(arr, 0)[n-1::n] / float(n)
    result[1:] = result[1:] - result[:-1]
    return result


def avg_run_in_columnwise(arr: NDArray, n: int):
    """
    Reduce the first `n` elements of each column in an array by averaging them, while leaving the rest of the array
    modified.

    Parameters
    ----------
    arr : NDArray
        Input array.
    n : int
        The number of run-in elements to average.

    Returns
    -------
    NDArray
        The new array where the first element in each column is an average of the run in elements.
    """
    run_in: NDArray = mean(arr[:n], 0)
    return vstack([run_in, arr[n:]])


def avg_run_in_rowwise(arr: NDArray, n: int):
    """
    Reduce the first `n` elements of each row in an array by averaging them, while leaving the rest of the array
    modified.

    Parameters
    ----------
    arr : NDArray
        Input array.
    n : int
        The number of run-in elements to average.

    Returns
    -------
    NDArray
        The new array where the first element in each row is an average of the run in elements.
    """
    return avg_run_in_columnwise(arr.transpose(), n).transpose()


def gen_seed(node: dict, *args: tuple[str]) -> int:
    """
    Generate a seed based on a node's `@id` and optional args so that rng is the same each time the model is re-run.
    """
    node_id = node.get("@id", "")
    seed_str = "".join([node_id] + [str(arg) for arg in args])
    hashed = hashlib.shake_128(seed_str.encode(), usedforsecurity=False).hexdigest(4)
    return abs(int(hashed, 16))


def correlated_normal_2d(
    n_iterations: int,
    means: NDArray,
    sds: NDArray,
    correlation_matrix: NDArray,
    seed: Union[int, random.Generator, None] = None,
) -> NDArray:
    """
    Generate correlated random samples from a multivariate normal distribution with specified means, standard
    deviations, and a correlation matrix. Each row represents a different variable (e.g., different years), and each
    column represents a different iteration (sample).

    Parameters
    ----------
    n_iterations : int
        The number of samples (iterations) to generate for each variable.
    means : NDArray
        An array of mean values for each variable (row).
    sds : NDArray
        An array of standard deviations for each variable (row).
    correlation_matrix : NDArray
        A positive-definite matrix representing the correlations between the variables (rows).
    seed : int | Generator | None, optional
        A seed to initialize the BitGenerator. If passed a Generator, it will be returned unaltered. If `None`, then
        fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    NDArray
        A 2D array of shape (len(means), n_iterations), where each row corresponds to a different variable and each
        column corresponds to a sample iteration. The values in each row are correlated according to the provided
        correlation matrix.
    """
    # Generate independent random samples for each year
    shape = (len(means), n_iterations)
    independent_samples = normal_2d(shape, 0, 1, seed=seed)

    # Apply Cholesky decomposition to the correlation matrix
    cholesky_decomp = linalg.cholesky(correlation_matrix)

    # Apply Cholesky transformation to introduce correlation across years (rows) for each sample
    correlated_samples = dot(cholesky_decomp, independent_samples)

    # Scale by standard deviations and shift by means
    scaled_samples = (
        correlated_samples
        * repeat_1d_array_as_columns(n_iterations, sds)
        + repeat_1d_array_as_columns(n_iterations, means)
    )

    return scaled_samples
