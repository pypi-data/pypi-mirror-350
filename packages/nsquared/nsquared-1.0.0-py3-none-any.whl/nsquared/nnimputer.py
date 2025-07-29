"""Base class for all nearest neighbors algorithms."""

import numpy.typing as npt
from abc import ABC, abstractmethod
from typing import Any, Union, Tuple
from hyperopt import Trials


class DataType(ABC):
    """Abstract class for data types. Examples include scalars and distributions."""

    @abstractmethod
    def distance(self, obj1: Any, obj2: Any) -> float:
        """Calculate the distance between two objects.

        Args:
            obj1 (Any): Object 1
            obj2 (Any): Object 2

        """
        pass

    @abstractmethod
    def average(self, object_list: npt.NDArray[Any]) -> Any:
        """Calculate the average of a list of objects.

        Args:
            object_list (npt.NDArray[Any]): List of objects

        """
        pass


class EstimationMethod(ABC):
    """Abstract class for estimation methods.
    Examples include row-row, col-col, two-sided, and doubly-robust.
    """

    def __init__(self, is_percentile: bool = True):
        """Initialize the estimation method.

        Args:
            is_percentile (bool): Whether to use percentile-based threshold. Defaults to True.

        """
        self.is_percentile = is_percentile

    @abstractmethod
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
            **kwargs (Any): Additional arguments for the imputer

        Returns:
            npt.NDArray: Imputed value

        """
        pass

    @abstractmethod
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
        pass

    def impute_all(
        self,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        distance_threshold: Union[float, Tuple[float, float]],
        data_type: DataType,
    ) -> npt.NDArray:
        """Impute all missing values in the data array.
        Note that this is not an abstract method, but a default implementation.
        This method can be overridden by subclasses if needed.

        Args:
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            distance_threshold (float): Distance threshold for nearest neighbors
            data_type (DataType): Data type to use (e.g. scalars, distributions)

        Returns:
            npt.NDArray: Imputed value

        """
        # by default, just call impute for each missing value
        n_rows, n_cols = data_array.shape
        imputed_data = data_array.copy()
        for i in range(n_rows):
            for j in range(n_cols):
                imputed_data[i, j] = self.impute(
                    i,
                    j,
                    data_array,
                    mask_array,
                    distance_threshold,
                    data_type,
                )
        return imputed_data


class NearestNeighborImputer:
    """Nearest neighbor composed of different kinds of methods."""

    def __init__(
        self,
        estimation_method: EstimationMethod,
        data_type: DataType,
        distance_threshold: Union[float, Tuple[float, float], None] = None,
    ):
        """Initialize the imputer.

        Args:
            estimation_method (EstimationMethod): Estimation method to use (e.g. row-row, col-col, two-sided, doubly-robust)
            data_type (DataType): Data type to use (e.g. scalars, distributions)
            distance_threshold (Optional[float], Optional[Tuple[float, float]] optional): Distance threshold(s) to use. Defaults to None.

        """
        self.estimation_method = estimation_method
        self.data_type = data_type
        self.distance_threshold = distance_threshold

    def __str__(self):
        return f"NearestNeighborImputer(estimation_method={self.estimation_method}, data_type={self.data_type})"

    def impute(
        self,
        row: int,
        column: int,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        **kwargs: Any,
    ) -> npt.NDArray:
        """Impute the missing value at the given row and column.

        Args:
            row (int): Row index
            column (int): Column index
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            **kwargs (Any): Additional keyword arguments

        Raises:
            ValueError: If distance threshold is not set

        Returns:
            npt.NDArray: Imputed value

        """
        if self.distance_threshold is None:
            raise ValueError(
                "Distance threshold is not set. Call a FitMethod on this imputer or manually set it."
            )
        return self.estimation_method.impute(
            row,
            column,
            data_array,
            mask_array,
            self.distance_threshold,
            self.data_type,
            **kwargs,
        )

    def impute_all(
        self,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
    ) -> npt.NDArray:
        """Impute all missing values in the data array.

        Args:
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            distance_threshold (float): Distance threshold for nearest neighbors

        Returns:
            npt.NDArray: Imputed value

        """
        if self.distance_threshold is None:
            raise ValueError(
                "Distance threshold is not set. Call a FitMethod on this imputer or manually set it."
            )
        return self.estimation_method.impute_all(
            data_array, mask_array, self.distance_threshold, self.data_type
        )


class FitMethod(ABC):
    """Abstract class for fitting methods.
    Examples include cross validation methods.
    """

    @abstractmethod
    def fit(
        self,
        data_array: npt.NDArray,
        mask_array: npt.NDArray,
        imputer: NearestNeighborImputer,
        ret_trials: bool = False,
    ) -> Union[
        float,
        Tuple[float, float],
        Tuple[float, Trials],
        Tuple[Tuple[float, float], Trials],
    ]:
        """Find the best distance threshold for the given data.

        Args:
            data_array (npt.NDArray): Data matrix
            mask_array (npt.NDArray): Mask matrix
            imputer (NearestNeighborImputer): Imputer object
            ret_trials (bool): Whether to return metadata about the hyperparameter search. Defaults to False.

        Returns:
            float | Tuple[float, float]: Best distance threshold(s)

        """
        pass
