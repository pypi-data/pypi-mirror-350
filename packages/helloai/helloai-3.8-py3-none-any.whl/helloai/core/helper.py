import math
import numpy as np

__all__ = ["distance", "angle3p"]


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    c = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return c


# P1-P2-P2의 각도를 시계방향으로


def angle3p(p1, p2, p3):
    ang = math.degrees(
        math.atan2(p3[1] - p2[1], p3[0] - p2[0])
        - math.atan2(p1[1] - p2[1], p1[0] - p2[0])
    )
    return ang + 360 if ang < 0 else ang


# def angle3p(p1, p2, p3):
#     a = np.array(p1)
#     b = np.array(p2)
#     c = np.array(p3)

#     ba = a - b
#     bc = c - b

#     cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
#     angle = np.arccos(cosine_angle)

#     return np.degrees(angle)
