import numpy as np
import pytest

from nupgis.ops import distance, point_to_line_distance


def test_distance() -> None:
    x = np.array([1, 2])
    y = np.array([3, 4])

    dist = distance(x=x, y=y)
    assert isinstance(dist, float)

    with pytest.raises(ValueError):
        x = np.array([1, 2, 3])
        distance(x=x, y=y)


def test_point_to_line_distance() -> None:
    x = np.array([1, 2])
    y = np.array([3, 4])
    p = np.array([5, 6])

    dist = point_to_line_distance(point=p, start=x, end=y)
    assert isinstance(dist, float)

    dist = point_to_line_distance(point=p, start=x, end=x)
    assert isinstance(dist, float)
    assert dist == distance(x=x, y=p)

    with pytest.raises(ValueError):
        p = np.array([1, 2, 3])
        point_to_line_distance(point=p, start=x, end=y)
