"""
全部考虑在纸张上的情况，原点在左上角。
"""

import numbers
from typing import Iterable, Literal, Tuple

import cv2
import numpy as np

AngleUnit = Literal["degree", "rad"]


def _to_int_array(data) -> np.ndarray:
    try:
        return np.array(data, dtype=np.int32)
    except ValueError as e:
        raise e


class Transform:
    @staticmethod
    def rotate(points: np.ndarray, M: np.ndarray) -> np.ndarray:
        return M.dot(np.hstack([points, np.ones((len(points), 1))]).T).T

    @staticmethod
    def shear(points: np.ndarray, M: np.ndarray) -> np.ndarray:
        # TODO: 待优化 https://blog.csdn.net/yjl9122/article/details/70853475
        return cv2.perspectiveTransform(np.array(points).reshape(-1, 1, 2), M)

    @staticmethod
    def scale(data: np.ndarray, scale_factor: np.ndarray | float) -> np.ndarray:
        return data * scale_factor

    @staticmethod
    def shift(points: np.ndarray, offset: np.ndarray | float) -> np.ndarray:
        return points + offset

    @staticmethod
    def get_scale_and_offset(dst_size, src_size):
        """不形变，且相对位置不变的情况下，图形从 src_size 背景到 dst_size 背景需要进行的缩放和平移"""
        dst_h, dst_w = dst_size[:2]
        src_h, src_w = src_size[:2]
        if dst_h / src_h > dst_w / src_w:
            scale = dst_h / src_h
            offset = np.array([(src_w * scale - dst_w) / 2, 0])
        else:
            scale = dst_w / src_w
            offset = np.array([0, (src_h * scale - dst_h) / 2])
        return scale, offset


class ShapeArrayMeta(type):
    def __instancecheck__(self, instance):
        if isinstance(instance, np.ndarray):
            try:
                _to_int_array(instance)
                return True
            except Exception:
                return False
        return False


class Shape(np.ndarray, metaclass=ShapeArrayMeta):
    pass


class PointArrayMeta(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Shape) and instance.shape == (2,)


class Point(np.ndarray, metaclass=PointArrayMeta):
    def __new__(cls, data):
        data = _to_int_array(data)
        if not isinstance(data, Point):
            raise ValueError()
        return data.view(cls)

    @classmethod
    def from_polar_coordinates(cls, theta: float, rho: float) -> "Point":
        return cls([rho * np.cos(theta), rho * np.sin(theta)])

    @staticmethod
    def get_theta(p: "Point", unit: AngleUnit = "rad") -> float:
        rad = np.arctan2(p[1], p[0])
        if unit == "degree":
            return np.rad2deg(rad)
        return rad

    @staticmethod
    def get_rho(p: "Point") -> float:
        return np.sqrt(p[0] ** 2 + p[1] ** 2)

    @staticmethod
    def to_polar_coordinates(p: "Point", angle_unit: AngleUnit = "rad") -> Tuple[float, float]:
        return Point.get_theta(p, angle_unit), Point.get_rho(p)

    @staticmethod
    def get_symmetric(p: "Point", reference: "Point | Line") -> "Point":
        if isinstance(reference, Point):
            return Point(2 * reference - p)
        else:
            raise NotImplementedError()


class BoxArrayMeta(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Shape) and instance.shape == (4,)


class Box(np.ndarray, metaclass=BoxArrayMeta):
    def __new__(cls, data):
        """
        永远是左上右下的顺序
        """
        data = _to_int_array(data)

        if isinstance(data, Quadril) or isinstance(data, Line):
            data = np.array(
                [
                    min(data[:, 0]),
                    min(data[:, 1]),
                    max(data[:, 0]),
                    max(data[:, 1]),
                ],
            ).reshape(4)
        elif isinstance(data, Box):
            data = Box(Line(data))
        else:
            raise ValueError()
        return data.view(cls)

    @staticmethod
    def is_in(inner: "Box", outer: "Box") -> bool:
        x1, y1, x2, y2 = inner
        X1, Y1, X2, Y2 = outer
        return X1 < (x1 + x2) / 2 < X2 and Y1 < (y1 + y2) / 2 < Y2

    @staticmethod
    def is_intersect(a: "Box", b: "Box") -> bool:
        return not (a[0] >= b[2] or b[0] >= a[2] or a[1] >= b[3] or b[1] >= a[3])

    @staticmethod
    def is_vertical_intersect(a: "Box", b: "Box") -> bool:
        if a[0] <= b[0] < a[2] or a[0] < b[2] <= a[2] or b[0] <= a[0] < b[2] or b[0] < a[2] <= b[2]:
            return True
        return False

    @staticmethod
    def get_center(box: "Box") -> Point:
        l, t, r, b = box
        return Point([(r + l) / 2, (b + t) / 2])

    @staticmethod
    def get_bounding_box(boxes: Iterable["Box"]) -> "Box":
        boxes = np.array(boxes)
        return Box(
            [
                min(boxes[:, 0]),
                min(boxes[:, 1]),
                max(boxes[:, 2]),
                max(boxes[:, 3]),
            ]
        )


class LineArrayMeta(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Shape) and instance.shape == (2, 2)


class Line(np.ndarray, metaclass=LineArrayMeta):
    def __new__(cls, data):
        data = _to_int_array(data)

        if isinstance(data, Box):
            data = data.reshape(2, 2)
        elif isinstance(data, Quadril):
            data = Line(Box(data))
        elif not isinstance(data, Line):
            raise ValueError()
        return data.view(cls)

    @staticmethod
    def get_length(line: "Line") -> float:
        return Point.get_rho(Point(line[1] - line[0]))

    @staticmethod
    def get_direction(line: "Line", angle_unit: AngleUnit = "rad") -> float:
        return Point.get_theta(Point(line[1] - line[0]), angle_unit)

    @staticmethod
    def get_mid(line: "Line") -> Point:
        return Point((line[1] - line[0]) / 2)

    @staticmethod
    def split(line: "Line", num: int) -> Iterable["Point"]:
        p0, p1 = line.astype(float)
        offset = ((p1 - p0) / num).astype(float)
        points = np.full((num + 1, 2), p0)
        if offset[0] > 1:
            points[:, 0] = np.arange(p0[0], p1[0] + 1, offset[0])[: len(points[:, 0])]
        if offset[1] > 1:
            points[:, 1] = np.arange(p0[1], p1[1] + 1, offset[1])[: len(points[:, 1])]
        return points

    @staticmethod
    def is_valid(line: "Line") -> bool:
        return Line.get_length(line) != 0

    @staticmethod
    def is_horizontal(line: "Line") -> bool:
        p0, p1 = line
        return Line.is_valid(line) and p0[1] == p1[1]

    @staticmethod
    def is_vertical(line: "Line") -> bool:
        p0, p1 = line
        return Line.is_valid(line) and p0[0] == p1[0]


class TriangleArrayMeta(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Shape) and instance.shape == (3, 2)


class Triangle(np.ndarray, metaclass=TriangleArrayMeta):
    def __new__(cls, data):
        data = _to_int_array(data)

        if len(data) == 6 and all([isinstance(x, numbers.Number) for x in data]):
            data = data.reshape(3, 2)
        elif not isinstance(data, Triangle):
            raise ValueError()
        return data.view(cls)

    @staticmethod
    def is_clockwise(tri: "Triangle") -> bool:
        p0, p1, p2 = tri
        return ((p1[1] - p0[1]) * (p2[0] - p1[0])) < ((p1[0] - p0[0]) * (p2[1] - p1[1]))

    @staticmethod
    def get_angles(tri: "Triangle") -> Tuple[float, float, float]:
        p0, p1, p2 = tri
        a = Point.get_rho(p1 - p0)
        b = Point.get_rho(p2 - p1)
        c = Point.get_rho(p0 - p2)
        a2, b2, c2 = a**2, b**2, c**2
        alpha = np.arccos((b2 + c2 - a2) / (2 * b * c))
        betta = np.arccos((a2 + c2 - b2) / (2 * a * c))
        gamma = np.arccos((a2 + b2 - c2) / (2 * a * b))
        return alpha, betta, gamma

    @staticmethod
    def to_cirle(tri: "Triangle") -> "Circle":
        p1, p2, p3 = tri
        x, y, z = p1[0] + p1[1] * 1j, p2[0] + p2[1] * 1j, p3[0] + p3[1] * 1j
        w = z - x
        w /= y - x
        c = (x - y) * (w - abs(w) ** 2) / 2j / w.imag - x
        return Circle(Point([-c.real, -c.imag]), abs(c + x))

    @staticmethod
    def is_valid(tri: "Triangle") -> bool:
        angles = Triangle.get_angles(tri)
        return all([x != 0 for x in angles])


class QuadrilArrayMeta(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Shape) and instance.shape == (4, 2)


class Quadril(np.ndarray, metaclass=QuadrilArrayMeta):
    def __new__(cls, data):
        data = _to_int_array(data)

        if len(data) == 8 and all([isinstance(x, numbers.Number) for x in data]):
            data = data.reshape(4, 2)
        elif isinstance(data, Box):
            l, t, r, b = data
            data = Quadril([l, t, r, t, l, b, r, b])
        elif isinstance(data, Line):
            data = Quadril(Box(data))
        elif not isinstance(data, Quadril):
            raise ValueError()
        return data.view(cls)

    @staticmethod
    def is_box(quadril: "Quadril") -> bool:
        if (
            quadril[0][0] == quadril[2][0]
            and quadril[0][1] == quadril[1][1]
            and quadril[1][0] == quadril[3][0]
            and quadril[2][1] == quadril[3][1]
        ):
            l, t, r, b = Box(quadril)
            if l != r and t != b:
                return True
        return False


class PolygonArrayMeta(type):
    def __instancecheck__(self, instance):
        return (
            isinstance(instance, Shape)
            and len(instance.shape) == 2
            and instance.shape[0] >= 5
            and instance.shape[1] == 2
        )


class Polygon(np.ndarray, metaclass=PolygonArrayMeta):
    def __new__(cls, data):
        try:
            data = np.array(data)
        except ValueError as e:
            raise e

        if not isinstance(data, Polygon):
            raise ValueError()

        return data.view(cls)

    @staticmethod
    def to_ellipse_polynomial(polygon: "Polygon") -> np.ndarray:
        """任意椭圆: A x^2 + B xy + C y^2 + Dx + Ey + F = 0 where F is always -1"""
        if len(np.unique(polygon)) < 5:
            raise RuntimeError("Not enough points or duplicated points")

        xx, yy = polygon[:, 0], polygon[:, 1]
        x, y = xx[:, np.newaxis], yy[:, np.newaxis]

        J = np.hstack((x * x, x * y, y * y, x, y))
        InvJTJ = np.linalg.inv(np.dot(J.T, J))
        ABC = np.dot(InvJTJ, np.dot(J.T, np.ones_like(x)))
        abcdef = np.append(ABC, -1)
        return abcdef

    @staticmethod
    def to_ellipse(polygon: "Polygon") -> "Ellipse":
        abcdef = Polygon.to_ellipse_polynomial(polygon)
        a, b, c, d, e, f = abcdef

        Amat = np.array(
            [
                [a, b / 2.0, d / 2.0],
                [b / 2.0, c, e / 2.0],
                [d / 2.0, e / 2.0, f],
            ]
        )

        # See B.Bartoni:
        # Preprint SMU-HEP-10-14 Multi-dimensional Ellipsoidal Fitting
        # equation 20 for the following method for finding the center
        A2Inv = np.linalg.inv(Amat[0:2, 0:2])  # inverse matrix
        ofs = abcdef[3:5] / 2.0
        center = -np.dot(A2Inv, ofs)

        # Center the ellipse at the origin
        Tofs = np.eye(3)  # identity matrix
        Tofs[2, 0:2] = center
        R = np.dot(Tofs, np.dot(Amat, Tofs.T))
        R2 = R[0:2, 0:2]
        s1 = -R[2, 2]
        RS = R2 / s1
        e_value, e_vector = np.linalg.eig(RS)  # calculate eigenvalues and eigenvectors
        # rotation_M = np.linalg.inv(e_vector)

        axes = np.sqrt(1.0 / np.abs(e_value))
        degree = np.degrees(np.arctan2(e_vector[1, 0], e_vector[0, 0]))
        return Ellipse(center, (axes[0], axes[1]), degree)

    @staticmethod
    def is_convex_polygon(polygon: "Polygon") -> bool:
        raise NotImplementedError()


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius


class Ellipse:
    def __init__(
        self,
        center: Point,
        axes: Tuple[float, float],
        degree: float,
    ) -> None:
        self.center = center
        self.axes = np.array(axes, dtype=np.int32)
        self.degree = degree

    def get_circumscribed_box(self) -> Box:
        a, b = self.axes if self.axes[0] > self.axes[1] else self.axes[::-1]
        theta = np.deg2rad(self.degree)
        sin_theta, cos_theta = np.sin(theta), np.cos(theta)
        A = a**2 * sin_theta**2 + b**2 * cos_theta**2
        B = 2 * (a**2 - b**2) * sin_theta * cos_theta
        C = a**2 * cos_theta**2 + b**2 * sin_theta**2
        F = -(a**2) * b**2
        y = np.sqrt(4 * A * F / (B**2 - 4 * A * C))
        y1, y2 = -np.abs(y), np.abs(y)
        x = np.sqrt(4 * C * F / (B**2 - 4 * C * A))
        x1, x2 = -np.abs(x), np.abs(x)
        return Box(np.array([[x1, y1], [x2, y2]], dtype=float) + self.center)

    def get_points(
        self, points_num: int = 6, arc_start: int = 0, arc_end: int = 0
    ) -> Iterable["Point"]:
        if points_num < 1:
            raise ValueError("sides_num should bigger than 1")
        return np.array(
            cv2.ellipse2Poly(
                (self.center[0], self.center[1]),
                (int(self.axes[0]), int(self.axes[1])),
                int(self.degree),
                delta=int(self.degree / points_num),
                arcStart=arc_start,
                arcEnd=arc_end,
            )
        )

    def get_eccentricity(self) -> float:
        a, b = self.axes if self.axes[0] > self.axes[1] else self.axes[::-1]
        return np.sqrt(1 - b**2 / a**2)

    def get_perimeter(self) -> int:
        a, b = self.axes if self.axes[0] > self.axes[1] else self.axes[::-1]
        return int(2 * np.pi * b + 4 * (a - b))


if __name__ == "__main__":
    p = np.array([2, 3])
    assert isinstance(p, Point)

    box = np.array([1, 2, 3, 4])
    assert isinstance(box, Box)

    line = np.array([[1, 1], [2, 2]])
    assert isinstance(line, Line)

    tri = np.array([[2, 3], [3, 4], [3, 2]])
    assert isinstance(tri, Triangle)

    quad = np.array([[2, 3], [3, 4], [3, 2], [1, 1]])
    assert isinstance(quad, Quadril)

    poly = np.array([[2, 3], [3, 4], [3, 2], [1, 1], [5, 3]])
    assert isinstance(poly, Polygon)

    print("line to box:", Box(line))  # 矩形对角线
    print("line to quadril:", Quadril(line))  # 线条外接矩形的四个顶
    print("box to quadril:", Quadril(box))  # 矩形的四个顶点
    print("quadril to box:", Box(quad))  # 任意四边形的外接矩形
    print("quadril to line:", Line(quad))  # 任意四边形的外接矩形的对角线
    print("box to line:", Line(box))  # 矩形的对角线
