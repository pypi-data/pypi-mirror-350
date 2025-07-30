import math
import numpy as np

def in_region(a, p1, p2, include_end=True):
    if include_end:
        return (p1 >= a >= p2) or (p2 >= a >= p1)
    else:
        return (p1 > a > p2) or (p2 > a > p1)

def equal_rect(c, area):
    """
    a + b = c/2
    a * b = area
    a >= b
    return a , b
    """

    A = -1
    B = c/2
    C = -area

    sqdelta = math.sqrt(B * B - 4 * A * C)

    x1 =(-B + sqdelta) / (2 * A)
    x2 =(-B - sqdelta) / (2 * A)
    return x2, x1

def rodrigues_rotate(axis_point, axis_vector, angle, points=None):
    """
    根据罗德里格公式将points(n,3)绕轴axis旋转angle
    """
    axis_point = np.asarray(axis_point)
    axis_vector = np.asarray(axis_vector)
    c = np.cos(angle)
    s = np.sin(angle)
    d = 1 - c
    x, y, z = axis_vector
    rotate_j = np.asarray([
                        [c + x**2 * d, x * y * d - z * s, x * z * d + y * s],
                        [y * x * d + z * s, c + y**2 * d, y * z * d - x * s],
                        [z * x * d - y * s, z * y * d + x * s, c + z**2 * d]
                    ])
    r = rotate_j
    t = - axis_point @ rotate_j.T + axis_point

    if points is None:
        return r, t
    else:
        return points @ r.T + t

def rodrigues_rotation_between_vectors(a, b, points=None):
    """
    根据罗德里格公式计算从向量a到b的旋转矩阵R
    用法:
    points: (n,3)
    旋转后为 points @ R.T
    """
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    v = np.cross(a, b)
    c = np.dot(a, b)
    if np.isclose(c, -1.0):  # 处理反向情况
        R = -np.eye(3)
    else:
        k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + k + (k @ k) * (1 / (1 + c))
    if points is None:
        return R
    else:
        return points @ R.T

def svd_homogeneous(terms):
    """
    比如求 ax**2 + bxy + cy + d = 0的最优系数
    传入terms = [x**2, xy, y, 1]
    返回最优a,b,c,d
    """
    A = np.column_stack(terms)
    U, S, Vh = np.linalg.svd(A)
    coefficients = Vh[-1, :] 
    return coefficients

def svd_non_homogeneous(terms, z):
    """
    比如求 z = ax**2 + bxy + cy + d 的最优系数
    传入terms = [x**2, xy, y, 1] 与 z
    返回最优a,b,c,d
    """
    A = np.column_stack(terms)
    return np.linalg.lstsq(A, z, rcond=None)[0]
