# from numpy._core.numerictypes import float
from .nnimputer import EstimationMethod, DataType
import numpy.typing as npt
import numpy as np
from typing import Union, Tuple, Any
import logging
import warnings
from typing import Optional
from .data_types import Scalar
from tqdm import tqdm

logger = logging.getLogger(__name__)


class RowRowEstimator(EstimationMethod):
    """Estimate the missing value using row-row nearest neighbors."""

    def __init__(self, is_percentile: bool = True):
        """Initialize the row-row estimator.

        Args:
            is_percentile (bool): Whether to use percentile-based threshold. Defaults to True.

        """
        super().__init__(is_percentile)
        self.row_distances = dict()

    def __str__(self):
        return "RowRowEstimator"

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
        allow_self_neighbor: bool = False,
        **kwargs: Any,
    ) -> npt.NDArray:
        """Impute the missing value at the given row and column.

        Args:
            row (int): Row index
            column (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            distance_threshold (float): Distance threshold for nearest neighbors
            data_type (DataType): Data type to use (e.g. scalars, distributions)
            allow_self_neighbor (bool): Whether to allow self-neighbor. Defaults to False.
            **kwargs (Any): Additional keyword arguments

        Returns:
            npt.NDArray: Imputed value

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # Calculate distances between rows
            self._calculate_distances(row, column, data_array, mask_array, data_type)
            all_dists = np.copy(self.row_distances[row])
            # Exclude the target column
            if not allow_self_neighbor:
                all_dists[:, column] = np.nan
            row_dists = np.nanmean(all_dists, axis=1)
            if self.is_percentile:
                # NOTE: we assume eta_row and eta_col are in [0, 1] in this case
                quantile_row_dists = row_dists[
                    ~np.isnan(row_dists) & (row_dists != np.inf)
                ]
                if quantile_row_dists.size == 0:
                    # No valid distances, return np.nan
                    eta_row = np.nan
                else:
                    eta_row = np.quantile(quantile_row_dists, distance_threshold)
            else:
                eta_row = distance_threshold

            # Find the nearest neighbors indexes
            nearest_neighbors = np.where(row_dists <= eta_row)[0]
            # Apply mask_array to data_array
            masked_data_array = np.copy(data_array)
            masked_data_array[mask_array == 0] = np.nan

        # NOTE: this code block will never be called since the target row
        # is always a nearest neighbor
        if len(nearest_neighbors) == 0:
            # return np.array(np.nan)
            # NOTE: implement the base case described by Eq. 11 in
            # "Counterfactual Inference for Sequential Experiments".
            if mask_array[row, column]:
                # return the observed outcome
                return data_array[row, column]
            else:
                # return the average of all observed outcomes corresponding
                # to treatment 1 at time t.
                return data_type.average(masked_data_array[:, column])

        # Calculate the average of the nearest neighbors
        nearest_neighbors_data = masked_data_array[nearest_neighbors, column]
        return data_type.average(nearest_neighbors_data)

    def _calculate_distances(
        self,
        row: int,
        col: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
    ) -> None:
        """Sets the distances for the imputer.
        Sets the distances as a class attribute, so returns nothing.

        Args:
            row (int): Row index
            col (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            data_type (DataType): Data type to use (e.g. scalars, distributions)

        """
        data_shape = data_array.shape
        n_rows = data_shape[0]
        n_cols = data_shape[1]

        if row in self.row_distances:
            return

        # Calculate distances between rows
        row_dists = np.zeros((n_rows, n_cols))
        # Scalar optimization with vectorized operations instead of loops
        if isinstance(data_type, Scalar):
            # Determine overlap columns for any pairwise rows
            overlap_columns_mask = np.logical_and(
                np.tile(mask_array[row], (n_rows, 1)), mask_array
            )
            row_big_matrix = np.tile(data_array[row], (n_rows, 1))
            row_dists = np.power(data_array - row_big_matrix, 2).astype(np.float64)
            # We need the row dists as a float matrix to use np.nanmean
            row_dists[~overlap_columns_mask] = np.nan
            self.row_distances[row] = row_dists
            return

        for i in range(n_rows):
            # Get columns observed in both row i and row
            overlap_columns = np.logical_and(mask_array[row], mask_array[i])

            if not np.any(overlap_columns):
                row_dists[i, :] = np.nan
                continue

            # Calculate distance between rows
            for j in range(n_cols):
                if not overlap_columns[j]:  # Skip missing values and the target column
                    row_dists[i, j] = np.nan
                else:
                    row_dists[i, j] = data_type.distance(
                        data_array[row, j], data_array[i, j]
                    )
        self.row_distances[row] = row_dists


class ColColEstimator(EstimationMethod):
    """Estimate the missing value using column-column nearest neighbors."""

    def __init__(self, is_percentile: bool = True):
        """Initialize the column-column estimator.

        Args:
            is_percentile (bool): Whether to use percentile-based threshold. Defaults to True.

        """
        self.estimator = RowRowEstimator(is_percentile=is_percentile)
        # use the same logic as RowRowEstimator but transposed
        # save the distances

    def __str__(self):
        return "ColColEstimator"

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
        allow_self_neighbor: bool = False,
        **kwargs: Any,
    ) -> npt.NDArray:
        """Impute the missing value at the given row and column.

        Args:
            row (int): Row index
            column (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            distance_threshold (float): Distance threshold for nearest neighbors
            data_type (DataType): Data type to use (e.g. scalars, distributions)
            allow_self_neighbor (bool): Whether to allow self-neighbor. Defaults to False.
            **kwargs (Any): Additional keyword arguments

        Returns:
            npt.NDArray: Imputed value

        """
        data_transposed = np.swapaxes(data_array, 0, 1)
        mask_transposed = np.swapaxes(mask_array, 0, 1)

        return self.estimator.impute(
            column,
            row,
            data_transposed,
            mask_transposed,
            distance_threshold,
            data_type,
            allow_self_neighbor,
        )

    def _calculate_distances(
        self,
        row: int,
        col: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
    ) -> None:
        """Sets the distances for the imputer.
        Sets the distances as a class attribute, so returns nothing.

        Args:
            row (int): Row index
            col (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            data_type (DataType): Data type to use (e.g. scalars, distributions)

        """
        # We use the RowRow Estimator to calculate the distances
        pass


class DREstimator(EstimationMethod):
    """Estimate the missing entry using doubly robust nearest neighbors."""

    def __init__(self, is_percentile: bool = True):
        """Initialize the doubly robust estimator.

        Args:
            is_percentile (bool): Whether to use percentile-based threshold. Defaults to True.

        """
        super().__init__(is_percentile)
        self.row_distances = dict()
        self.col_distances = dict()

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
        allow_self_neighbor: bool = False,
        **kwargs: Any,
    ) -> npt.NDArray:
        """Impute the missing value at the given row and column using doubly robust method.

        Args:
        ----
            row (int): Row index
            column (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            distance_threshold (float or Tuple[float, float]): Distance threshold for nearest neighbors
            or a tuple of (row_threshold, col_threshold) for row and column respectively.
            data_type (DataType): Data type to use (e.g. scalars, distributions)
            allow_self_neighbor (bool): Whether to allow self-neighbor. Defaults to False.
            **kwargs (Any): Additional keyword arguments

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self._calculate_distances(row, column, data_array, mask_array, data_type)
            all_dists = np.copy(self.row_distances[row])
            # Exclude the target column
            if not allow_self_neighbor:
                all_dists[:, column] = np.nan
            row_dists = np.nanmean(all_dists, axis=1)
            if not mask_array[row, column] and not allow_self_neighbor:
                row_dists[row] = np.inf  # Exclude the target row
            # Exclude the target row
            all_dists = np.copy(self.col_distances[column])
            if not allow_self_neighbor:
                all_dists[row, :] = np.nan
            col_dists = np.nanmean(all_dists, axis=0)
            if not mask_array[row, column] and not allow_self_neighbor:
                col_dists[column] = np.inf  # Exclude the target col

        if isinstance(distance_threshold, tuple):
            eta_row = distance_threshold[0]
            eta_col = distance_threshold[1]
        else:
            eta_row = distance_threshold
            eta_col = distance_threshold
        if self.is_percentile:
            # NOTE: we assume eta_row and eta_col are in [0, 1] in this case
            quantile_row_dists = row_dists[~np.isnan(row_dists) & (row_dists != np.inf)]
            quantile_col_dists = col_dists[~np.isnan(col_dists) & (col_dists != np.inf)]
            if quantile_row_dists.size == 0:
                # No valid distances, return np.nan
                eta_row = np.nan
            else:
                eta_row = np.quantile(quantile_row_dists, eta_row)
            if quantile_col_dists.size == 0:
                # No valid distances, return np.nan
                eta_col = np.nan
            else:
                eta_col = np.quantile(quantile_col_dists, eta_col)

        # Find the row nearest neighbors indexes
        row_nearest_neighbors = np.nonzero(row_dists <= eta_row)[0]

        # Find the col nearest neighbors indexes
        col_nearest_neighbors = np.nonzero(col_dists <= eta_col)[0]

        # neighbors can only be used if they are observed
        row_nearest_neighbors = row_nearest_neighbors[
            mask_array[row_nearest_neighbors, column] == 1
        ]
        col_nearest_neighbors = col_nearest_neighbors[
            mask_array[row, col_nearest_neighbors] == 1
        ]

        # Use doubly robust nearest neighbors to combine row and col
        y_itprime = data_array[row, col_nearest_neighbors]
        y_jt = data_array[row_nearest_neighbors, column]

        if len(y_itprime) == 0 and len(y_jt) == 0:
            return np.array(np.nan)

        # get intersecting entries
        j_inds, tprime_inds = np.meshgrid(
            row_nearest_neighbors, col_nearest_neighbors, indexing="ij"
        )

        y_jtprime = data_array[j_inds, tprime_inds]
        mask_jtprime = mask_array[j_inds, tprime_inds]

        # nonzero gets all indices of the mask that are 1
        intersec_inds = np.nonzero(mask_jtprime == 1)

        y_itprime_inter = y_itprime[
            intersec_inds[1]
        ]  # this is a array of column values for all intersecting triplets
        y_jt_inter = y_jt[
            intersec_inds[0]
        ]  # this is a array of row values for all intersecting triplets
        # note: defaults to rownn if no intersection -> should default to ts-nn instead?
        if len(y_itprime_inter) == 0 or len(y_jt_inter) == 0:
            return np.array(
                data_type.average(y_jt)
                if len(y_jt) > 0
                else data_type.average(y_itprime)
            )
        sum_y = y_itprime_inter + y_jt_inter - y_jtprime[intersec_inds]
        avg = data_type.average(sum_y)
        return avg

    def _calculate_distances(
        self,
        row: int,
        col: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
    ) -> None:
        """Sets the distances for the imputer.
        Sets the distances as a class attribute, so returns nothing.

        Args:
            row (int): Row index
            col (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            data_type (DataType): Data type to use (e.g. scalars, distributions)

        """
        data_shape = data_array.shape
        n_rows = data_shape[0]
        n_cols = data_shape[1]

        if row not in self.row_distances:
            # Calculate distances between rows
            row_dists = np.zeros((n_rows, n_cols))

            # Scalar optimization with vectorized operations instead of loops
            if isinstance(data_type, Scalar):
                # Determine overlap columns for any pairwise rows
                overlap_columns_mask = np.logical_and(
                    np.tile(mask_array[row], (n_rows, 1)), mask_array
                )
                row_big_matrix = np.tile(data_array[row], (n_rows, 1))
                row_dists = np.power(data_array - row_big_matrix, 2).astype(np.float64)
                # We need the row dists as a float matrix to use np.nanmean
                row_dists[~overlap_columns_mask] = np.nan
            else:
                for i in range(n_rows):
                    # Get columns observed in both row i and row
                    overlap_columns = np.logical_and(mask_array[row], mask_array[i])

                    if not np.any(overlap_columns):
                        row_dists[i, :] = np.nan
                        continue

                    # Calculate distance between rows
                    for j in range(n_cols):
                        if not overlap_columns[
                            j
                        ]:  # Skip missing values and the target column
                            row_dists[i, j] = np.nan
                        else:
                            row_dists[i, j] = data_type.distance(
                                data_array[row, j], data_array[i, j]
                            )
            self.row_distances[row] = row_dists
            # self.row_distances[row][row] = np.inf  # Exclude the row itself

        if col not in self.col_distances:
            # Calculate distances between columns
            col_dists = np.zeros((n_rows, n_cols))

            # Scalar optimization with vectorized operations instead of loops
            if isinstance(data_type, Scalar):
                # Determine overlap columns for any pairwise rows
                overlap_columns_mask = np.logical_and(
                    np.tile(mask_array[:, col].reshape(-1, 1), (1, n_cols)), mask_array
                )
                row_big_matrix = np.tile(data_array[:, col].reshape(-1, 1), (1, n_cols))
                col_dists = np.power(data_array - row_big_matrix, 2).astype(np.float64)
                # We need the col dists as a float matrix to use np.nanmean
                col_dists[~overlap_columns_mask] = np.nan

            else:
                for j in range(n_cols):
                    # Get rows observed in both row i and row
                    overlap_columns = np.logical_and(
                        mask_array[:, col], mask_array[:, j]
                    )

                    if not np.any(overlap_columns):
                        col_dists[:, j] = np.nan
                        continue

                    # Calculate distance between columns
                    for i in range(n_rows):
                        if not overlap_columns[
                            i
                        ]:  # Skip missing values and the target column
                            col_dists[i, j] = np.nan
                        else:
                            col_dists[i, j] = data_type.distance(
                                data_array[i, col], data_array[i, j]
                            )
            self.col_distances[col] = col_dists
            # self.col_distances[col][col] = np.inf


class TSEstimator(EstimationMethod):
    """Estimate the missing value using two-sided nearest neighbors.

    This method first finds the row and column neighborhoods (based on a
    distance computed over overlapping observed entries, excluding the target)
    and then imputes the missing entry by averaging the observed values
    over the cross-product of these neighborhoods.
    """

    def __init__(self, is_percentile: bool = True):
        """Initialize the two-sided estimator.

        Args:
            is_percentile (bool): Whether to use percentile-based threshold. Defaults to True.

        """
        super().__init__(is_percentile)
        self.estimator = DREstimator(is_percentile=is_percentile)

    def __str__(self):
        return "TSEstimator"

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
        allow_self_neighbor: bool = True,
        **kwargs: Any,
    ) -> npt.NDArray:
        r"""Impute the missing value at the given row and column using two-sided NN.

        Args:
            row (int): Target row index.
            column (int): Target column index.
            data_array (npt.NDArray): Data matrix.
            mask_array (npt.NDArray): Boolean mask matrix (True if observed).
            distance_threshold (float or Tuple[float, float]): Distance threshold(s) for row and column neighborhoods. This is our \vec eta = (\eta_row, \eta_col).
            data_type (DataType): Provides methods for computing distances and averaging.
            allow_self_neighbor (bool): Whether to allow self-neighbor. Defaults to False.
            **kwargs (Any): Additional keyword arguments

        Returns:
            npt.NDArray: Imputed value.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self._calculate_distances(row, column, data_array, mask_array, data_type)
            all_dists = np.copy(self.estimator.row_distances[row])
            # Exclude the target column
            if not allow_self_neighbor:
                all_dists[:, column] = np.nan
            row_dists = np.nanmean(all_dists, axis=1)
            if not mask_array[row, column] and not allow_self_neighbor:
                row_dists[row] = np.inf  # Exclude the target row
            # Exclude the target row
            all_dists = np.copy(self.estimator.col_distances[column])
            if not allow_self_neighbor:
                all_dists[row, :] = np.nan
            col_dists = np.nanmean(all_dists, axis=0)
            if not mask_array[row, column] and not allow_self_neighbor:
                col_dists[column] = np.inf  # Exclude the target col

        if isinstance(distance_threshold, tuple):
            eta_row, eta_col = distance_threshold
        else:
            eta_row = distance_threshold
            eta_col = distance_threshold
        if self.is_percentile:
            # NOTE: we assume eta_row and eta_col are in [0, 1] in this case
            quantile_row_dists = row_dists[~np.isnan(row_dists) & (row_dists != np.inf)]
            quantile_col_dists = col_dists[~np.isnan(col_dists) & (col_dists != np.inf)]
            if quantile_row_dists.size == 0:
                # No valid distances, return np.nan
                eta_row = np.nan
            else:
                eta_row = np.quantile(quantile_row_dists, eta_row)
            if quantile_col_dists.size == 0:
                # No valid distances, return np.nan
                eta_col = np.nan
            else:
                eta_col = np.quantile(quantile_col_dists, eta_col)

        # Establish the neighborhoods subject to the distance thresholds
        row_nearest_neighbors = np.where(row_dists <= eta_row)[0]
        # This is the set N_row(i, j) = {i' | d^2(i, i') <= eta_row^2}
        col_nearest_neighbors = np.where(col_dists <= eta_col)[0]
        # This is the set N_col(i, j) = {j' | d^2(j, j') <= eta_col^2}
        neighborhood_submatrix = data_array[
            np.ix_(row_nearest_neighbors, col_nearest_neighbors)
        ]
        # This is the submatrix of the cross-product of the row and column neighborhoods
        mask_array = mask_array.astype(bool)  # for efficient indexing
        neighborhood_mask = mask_array[
            np.ix_(row_nearest_neighbors, col_nearest_neighbors)
        ]
        # This is the mask of the cross-product of the row and column neighborhoods

        values_for_estimation = neighborhood_submatrix[neighborhood_mask.astype(bool)]
        if values_for_estimation.size == 0:
            if mask_array[row, column]:
                logger.log(
                    logging.WARNING,
                    f"Warning: No valid neighbors found for ({row}, {column}). Returning observed value.",
                )
                return data_array[row, column]
            else:
                logger.log(
                    logging.WARNING,
                    f"Warning: No valid neighbors found for ({row}, {column}). Returning np.nan.",
                )
                return np.array(np.nan)
        else:
            theta_hat = data_type.average(values_for_estimation)
            return theta_hat

    def _calculate_distances(
        self,
        row: int,
        col: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
    ) -> None:
        """Sets the distances for the imputer.
        Sets the distances as a class attribute, so returns nothing.

        Args:
            row (int): Row index
            col (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            data_type (DataType): Data type to use (e.g. scalars, distributions)

        """
        self.estimator._calculate_distances(row, col, data_array, mask_array, data_type)
        # We use the DREstimator class to calculate the distances
        # because it is the same as the two-sided estimator


class StarNNEstimator(EstimationMethod):
    """Estimate the missing value using Star NN."""

    def __init__(
        self,
        delta: float = 1,
        noise_variance: Optional[
            float
        ] = None,  # this is a the new variable specific to this!
        convergence_threshold: float = 1e-4,
        max_iterations: int = 10,
    ):
        """Initialize the Star NN estimator."""
        # sanity checks:
        if delta < 0 or delta > 1:
            raise ValueError("Delta must be between 0 and 1.")
        if convergence_threshold < 0:
            raise ValueError("Convergence threshold must be non-negative.")
        if max_iterations <= 0:
            raise ValueError("Max iterations must be positive.")
        if noise_variance is not None and noise_variance < 0:
            raise ValueError("Noise variance must be non-negative.")
        self.row_distances = np.array([])
        self.noise_variance = noise_variance
        self.convergence_threshold = convergence_threshold
        self.max_iterations = max_iterations
        self.delta = delta
        self.estimated_signal_matrix = None  # these 2 are used to cache full matrix result since impute is 1 (r,c) at a time
        self.delta_value_for_signal_matrix = None

    def __str__(self):
        return "StarNNEstimator"

    def _impute_single_value_helper(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
        vectorize: bool = True,
    ) -> npt.NDArray:
        """Imputes one specific value using the Star NN method."""
        n_rows, n_cols = data_array.shape
        delta = self.delta / np.sqrt(n_rows)
        logger.info("delta: %s" % delta)  # TODO switch to logger.log
        logger.info(
            "noise_variance: %s" % self.noise_variance
        )  # TODO switch to logger.log
        if self.noise_variance is None:
            noise_variance = np.var(data_array[mask_array == 1]) / 2
            self.noise_variance = noise_variance
        else:
            noise_variance = self.noise_variance

        observed_rows = np.where(mask_array[:, column] == 1)[0]
        n_observed = len(observed_rows)
        if n_observed == 0:
            return np.array(np.nan)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # Calculate distances between rows
            if not self.row_distances.size:
                self._calculate_distances(
                    row, column, data_array, mask_array, data_type
                )
            row_distances = self.row_distances

        d = row_distances[row, observed_rows]
        d = np.where(observed_rows == row, 0, d - 2 * noise_variance)
        row_dist_min = min(0, np.min(d))
        d = np.where(observed_rows == row, 0, d - row_dist_min)

        mean_distance = np.mean(d)
        dist_diff = d - mean_distance
        # print (noise_variance)
        if noise_variance != 0:
            weights = (1 / n_observed) - dist_diff / (
                8 * noise_variance * np.log(1 / delta)
            )
        else:
            weights = (1 / n_observed) - dist_diff / (8 * np.log(1 / delta))
        sorted_weights = np.sort(weights)[::-1]
        if vectorize:  # datatype-independent optimization!
            cumsum_weights = np.cumsum(sorted_weights)
            threshold = (cumsum_weights - 1) / np.arange(1, n_observed + 1)
            masker = sorted_weights > threshold
            u = threshold[masker][-1] if masker.any() else 0
            weights = np.maximum(0, weights - u)
        else:
            weight_sum = 0
            u = 0
            for k in range(n_observed):
                weight_sum += sorted_weights[k]
                u_new = (weight_sum - 1) / (k + 1)
                if k == n_observed - 1 or sorted_weights[k + 1] <= u_new:
                    u = u_new
                    break
            weights = np.maximum(0, weights - u)
            # print("weights for row %d, column %d: %s" % (row, column, weights))
        ret_val = np.sum(weights * data_array[observed_rows, column])
        return ret_val

    def _fit_full_matrix(
        self,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
    ) -> np.ndarray:
        n_rows, n_cols = data_array.shape
        imputed_data = np.zeros_like(data_array)
        for iter in range(self.max_iterations):
            logger.info("Iteration %d" % iter)  # TODO switch to logger.log
            for i in range(n_rows):
                for j in range(n_cols):
                    imputed_data[i, j] = self._impute_single_value_helper(
                        i, j, data_array, mask_array, data_type
                    )
            diff = imputed_data[mask_array == 1] - data_array[mask_array == 1]
            diff = diff[~np.isnan(diff)]  # Remove any NaN values
            if len(diff) > 0:
                new_variance_estimate = np.var(diff)
                if self.noise_variance is None:
                    raise ValueError(
                        "Noise variance is not set, which should not happen."
                    )
                if (
                    abs(new_variance_estimate - self.noise_variance)
                    / self.noise_variance
                    < self.convergence_threshold
                ):
                    logger.info(
                        f"Converged after {iter + 1} iterations and final noise variance: {new_variance_estimate}"
                    )
                    self.noise_variance = new_variance_estimate
                    break
                self.noise_variance = new_variance_estimate
        self.estimated_signal_matrix = imputed_data
        return imputed_data

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],  # unused
        data_type: DataType,
        allow_self_neighbor: bool = False,
        **kwargs: Any,
    ) -> npt.NDArray:
        """Impute the missing value at the given row and column.

        Args:
            row (int): Row index of the missing value.
            column (int): Column index of the missing value.
            data_array (npt.NDArray): Data matrix containing observed and missing values.
            mask_array (npt.NDArray): Boolean mask matrix indicating observed values.
            distance_threshold (Union[float, Tuple[float, float]]): Distance threshold (unused in this method).
            data_type (DataType): Data type providing methods for distance calculation and averaging.
            allow_self_neighbor (bool): Whether to allow self-neighbor. Defaults to False. (unused in this method)
            **kwargs (Any): Additional keyword arguments.

        Returns:
            npt.NDArray: Imputed value for the specified row and column.

        """
        full_matrix = self.impute_all(
            data_array,
            mask_array,
            distance_threshold,
            data_type,
        )
        val_at_index = full_matrix[row, column]
        return val_at_index

    def impute_all(
        self,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
    ) -> npt.NDArray:
        """Impute all missing values in the data array.

        Args:
            data_array (npt.NDArray): Data matrix containing observed and missing values.
            mask_array (npt.NDArray): Boolean mask matrix indicating observed values.
            distance_threshold (Union[float, Tuple[float, float]]): Distance threshold for nearest neighbors.
            data_type (DataType): Data type providing methods for distance calculation and averaging.

        Returns:
            npt.NDArray: Imputed value for the specified row and column.

        """
        if self.estimated_signal_matrix is None:
            full_mat = self._fit_full_matrix(
                data_array,
                mask_array,
                data_type,
            )
            self.estimated_signal_matrix = full_mat  # cache it
        else:
            full_mat = self.estimated_signal_matrix

        return full_mat

    def _calculate_distances(
        self,
        row: int,
        col: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        data_type: DataType,
        vectorize: bool = True,
    ) -> None:
        """Computes distances, caches them. Vectorized version, tested for equivalence."""
        if vectorize and isinstance(data_type, Scalar):
            X = data_array
            M = mask_array.astype(float)
            X_masked = X * M

            # count of overlapping columns for each pair
            counts = M @ M.T

            # A[i,j] = Σₖ Mᵢₖ·Mⱼₖ·Xᵢₖ²
            A = (X_masked**2) @ M.T
            # C[i,j] = Σₖ Mᵢₖ·Mⱼₖ·Xᵢₖ·Xⱼₖ
            C = X_masked @ X_masked.T

            D = A + A.T - 2 * C
            # normalize, inf where no overlap
            with np.errstate(divide="ignore", invalid="ignore"):
                row_distances = D / counts
            row_distances[counts == 0] = np.inf
            np.fill_diagonal(row_distances, 0)
        else:
            n_rows, n_cols = data_array.shape
            row_distances = np.zeros((n_rows, n_rows))

            for i in tqdm(range(n_rows)):
                for j in range(i + 1, n_rows):
                    overlap_cols = np.logical_and(mask_array[i, :], mask_array[j, :])
                    if not np.any(overlap_cols):
                        row_distances[i, j] = np.inf
                        row_distances[j, i] = np.inf
                        continue
                    if isinstance(data_type, Scalar):
                        row_distances[i, j] = np.sum(
                            np.square(
                                data_array[i, overlap_cols]
                                - data_array[j, overlap_cols]
                            )
                        )
                    else:
                        for k in range(n_cols):
                            if not overlap_cols[k]:
                                continue
                            row_distances[i, j] += data_type.distance(
                                data_array[i, k], data_array[j, k]
                            )
                    row_distances[i, j] /= np.sum(overlap_cols)
                    row_distances[j, i] = row_distances[i, j]

        self.row_distances = row_distances
