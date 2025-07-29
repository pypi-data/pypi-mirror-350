from typing import Sequence

import numpy as np

from nupgis.ops import point_to_line_distance
from nupgis.validation import validate_2d_points


def simplify_polygon(points: Sequence[np.ndarray], epsilon: float) -> Sequence[np.ndarray]:
    validate_2d_points(points=points)

    if len(points) < 4:
        return points

    start = points[0]
    end = points[-1]
    reduced: list[np.ndarray] = []
    max_dist = 0.0
    index = 0

    for i, point in enumerate(points[1:-1]):
        cur_dist = point_to_line_distance(point=point, start=start, end=end)

        if np.greater(cur_dist, max_dist):
            max_dist = cur_dist
            index = i

    if max_dist > epsilon:
        reduced.extend(simplify_polygon(points=points[: index + 1], epsilon=epsilon)[:-1])
        reduced.extend(simplify_polygon(points=points[index:], epsilon=epsilon)[1:])

        return reduced

    reduced = [start, end]

    return reduced
