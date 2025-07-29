from typing import Sequence

import numpy as np


def validate_2d_points(points: Sequence[np.ndarray]) -> None:
    if not isinstance(points, Sequence):
        raise TypeError("Points must be a valid indexable `Sequence`")

    if len(points) < 1:
        raise ValueError("Points cannot be empty")

    for point in points:
        if not isinstance(point, np.ndarray):
            raise ValueError("Every point must be a numpy array")

        if point.ndim != 1 or len(point.shape) > 1 or point.shape[0] != 2:
            raise ValueError("Every point must be 2d")

        for x in point:
            if np.isnan(x) or np.isinf(x):
                raise ValueError("Points cannot contain null or invalid values")
