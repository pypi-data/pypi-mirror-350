import numpy as np


def angle_between(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
    """Calculate the angle at p2 between vectors p1->p2 and p2->p3 in radians

    Parameters
    ----------
    p1 : np.ndarray
        First point
    p2 : np.ndarray
        Pivot point
    p3 : np.ndarray
        Last point

    Returns
    -------
    float
        Angle of p1-p2-p3
    """

    a = p1 - p2
    b = p3 - p2
    dot_product = a.dot(b)
    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    if mag_a == 0 or mag_b == 0:
        return 0

    cos_angle = dot_product / (mag_a * mag_b)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to avoid numerical error

    return np.acos(cos_angle)


def simplify_polygon(
    points: list[np.ndarray], angle_threshold_degrees: float = 5.0, lookahead: int = 10
) -> list[np.ndarray]:
    """Lang simplification with look-ahead modification.

    Parameters
    ----------
    points : list[np.ndarray]
        List of (x, y) tuples forming a polygon or polyline
    angle_threshold_degrees : float, optional
        Angular threshold in degrees for removing points, by default 5.0
    lookahead : int, optional
        Max number of points to look ahead for skipping, by default 5

    Returns
    -------
    list[np.ndarray]
        Simplified list of points
    """

    if len(points) < 3:
        return points

    angle_threshold = np.radians(angle_threshold_degrees)
    simplified = [points[0]]
    i = 0

    while i < len(points) - 2:
        max_j = min(i + lookahead, len(points) - 1)
        j = i + 1
        best_j = j

        while j < max_j:
            angle = angle_between(points[i], points[j], points[j + 1])
            if abs(np.pi - angle) <= angle_threshold or angle <= angle_threshold:
                best_j = j + 1  # Can skip point j
                j += 1
            else:
                break

        simplified.append(points[best_j])
        i = best_j

    # Ensure last point is included
    if not np.all(np.equal(simplified[-1], points[-1])):
        simplified.append(points[-1])

    return simplified
