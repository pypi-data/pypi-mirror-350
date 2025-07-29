import numpy as np


def distance(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) != len(y):
        raise ValueError("Points must have the same dimension")
    return float(np.linalg.norm(x - y))


def point_to_line_distance(point: np.ndarray, start: np.ndarray, end: np.ndarray) -> float:
    if np.array_equal(start, end):
        return distance(x=point, y=start)

    if len(point) != 2 or len(start) != 2 or len(end) != 2:
        raise ValueError("All points must be 2D")

    x = end - start
    x = np.append(x, 0.0)
    y = start - point
    y = np.append(y, 0.0)
    area = np.linalg.norm(np.cross(x, y))

    return float(np.abs(area) / float(np.linalg.norm(end - start)))
