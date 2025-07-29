"""A function to return the DRNN imputer.

More details on the Doubly Robust Nearest Neighbor (DRNN) method can be found in Section 2.2.2 of the following paper:
    Dwivedi, R., Tian, K., Tomkins, S., Klasnja, P., Murphy, S., & Shah, D. (2022).
    Doubly robust nearest neighbors in factor models. arXiv preprint arXiv:2211.14297.
"""

from .nnimputer import NearestNeighborImputer
from typing import Optional


def dr_nn(
    distance_threshold_row: Optional[float] = None,
    distance_threshold_col: Optional[float] = None,
    is_percentile: bool = True,
) -> NearestNeighborImputer:
    """Create a doubly robust nearest neighbor imputer.

    If distance_threshold_row and distance_threshold_col are not provided, they must be set by calling fit on the imputer.


    Args:
        distance_threshold_row (float): [Optional] Distance threshold for row-row nearest neighbors.
        distance_threshold_col (float): [Optional] Distance threshold for column-column nearest neighbors.
        is_percentile (bool): [Optional] Whether to use percentile-based distance threshold. Defaults to True.

    Returns:
        NearestNeighborImputer: A doubly robust nearest neighbor imputer.

    """
    from .estimation_methods import DREstimator
    from .data_types import Scalar

    estimator = DREstimator(is_percentile=is_percentile)
    data_type = Scalar()
    # note that the default value of distance_threshold is np.inf -> distance threshold is unused for DRNN
    if distance_threshold_row is None or distance_threshold_col is None:
        distance_threshold = None
    else:
        distance_threshold = (distance_threshold_row, distance_threshold_col)
    return NearestNeighborImputer(estimator, data_type, distance_threshold)
