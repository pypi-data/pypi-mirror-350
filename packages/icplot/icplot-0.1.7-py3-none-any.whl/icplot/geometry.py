"""
Module for primitive geometries. This is used to keep dependencies simple,
consider a real geometry library like cgal for more complex or performance
dependent work.
"""

from __future__ import annotations
from dataclasses import dataclass

import numpy as np
from scipy.spatial.transform import Rotation


@dataclass(frozen=True)
class Vector:
    """
    A 3d spatial vector
    """

    x: float
    y: float = 0.0
    z: float = 0.0

    def scale(self, factor: float) -> Vector:
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])


@dataclass(frozen=True)
class Point:
    """
    A location in 3d space
    """

    x: float
    y: float = 0.0
    z: float = 0.0

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    def translate(self, v: Vector) -> Point:
        return Point(self.x + v.x, self.y + v.y, self.z + v.z)

    @staticmethod
    def from_array(arr: np.ndarray) -> Point:
        return Point(arr[0], arr[1], arr[2])


@dataclass(frozen=True)
class Shape:
    """
    A shape in 3d space, defaults to having a normal to Z
    """

    loc: Point = Point(0.0, 0.0, 0.0)
    normal: Vector = Vector(0.0, 0.0, 1.0)


def get_rotation_matrix(vec0, vec1):
    """get rotation matrix between two vectors using scipy"""
    vec0 = np.reshape(vec0, (1, -1))
    vec1 = np.reshape(vec1, (1, -1))
    r = Rotation.align_vectors(vec0, vec1)
    return r[0].as_matrix()


def get_normal(p0, p1, p2):
    direction = np.cross(p1 - p0, p2 - p0)
    return direction / np.linalg.norm(direction)


_GLOBAL_Z = np.array([0.0, 0.0, 1.0])


@dataclass(frozen=True)
class Quad(Shape):
    """
    A regular quadrilateral in 3d space, defaults to be normal to Z
    """

    width: float = 1.0
    height: float = 1.0

    @property
    def points(self) -> list[Point]:

        points = [
            self.loc.translate(Vector(-self.width / 2.0, -self.height / 2.0)),
            self.loc.translate(Vector(self.width / 2.0, -self.height / 2.0)),
            self.loc.translate(Vector(self.width / 2.0, self.height / 2.0)),
            self.loc.translate(Vector(-self.width / 2.0, self.height / 2.0)),
        ]

        rot = get_rotation_matrix(_GLOBAL_Z, self.normal.as_array())
        rotated_points = [
            Point.from_array(
                rot.dot(p.as_array() - self.loc.as_array()) + self.loc.as_array()
            )
            for p in points
        ]

        plane_normal = get_normal(
            rotated_points[0].as_array(),
            rotated_points[1].as_array(),
            rotated_points[3].as_array(),
        )

        if np.dot(plane_normal, self.normal.as_array()) < 0:
            rotated_points.reverse()
        return rotated_points

    def translate(self, v: Vector) -> Quad:
        return Quad(self.loc.translate(v), self.normal, self.width, self.height)


@dataclass(frozen=True)
class Cuboid(Shape):
    """
    A regular cuboid
    """

    width: float = 1.0
    height: float = 1.0
    depth: float = 1.0
    top_width_scale: float = 1.0

    def translate(self, v: Vector) -> Cuboid:
        return Cuboid(
            self.loc.translate(v), self.normal, self.width, self.height, self.depth
        )

    @property
    def points(self) -> list[Point]:

        base = Quad(
            self.loc.translate(Vector(0.0, 0.0, -self.depth / 2.0)),
            self.normal,
            self.width,
            self.height,
        )

        top = Quad(
            self.loc.translate(Vector(0.0, 0.0, -self.depth / 2.0)),
            self.normal,
            self.width * self.top_width_scale,
            self.height,
        )
        top = top.translate(self.normal.scale(self.depth))
        return base.points + top.points


@dataclass(frozen=True)
class Cylinder(Shape):
    """
    A cylinder
    """

    diameter: float = 1.0
    length: float = 1.0

    @property
    def start(self) -> Point:
        return self.loc

    @property
    def end(self) -> Point:
        return self.loc.translate(self.normal.scale(self.length))


@dataclass(frozen=True)
class Revolution(Shape):
    """
    A revolved profile sitting on the plane given by the loc
    and normal and revolved about the normal.
    """

    diameter: float = 1.0
    length: float = 1.0
    profile: str = "arc"


@dataclass(frozen=True)
class CuboidGrid:
    """
    A irregular grid composed of cuboids. Can be useful for
    generating topological meshes like OpenFoam's blockMesh.
    """

    x_locs: list[float]
    y_locs: list[float]
    z_locs: list[float]

    @property
    def cuboids(self) -> list[Cuboid]:
        ret = []

        for kdx, z in enumerate(self.z_locs[:-1]):
            for jdx, y in enumerate(self.y_locs[:-1]):
                for idx, x in enumerate(self.x_locs[:-1]):
                    width = self.x_locs[idx + 1] - x
                    height = self.y_locs[jdx + 1] - y
                    depth = self.z_locs[kdx + 1] - z
                    ret.append(
                        Cuboid(Point(x, y, z), width=width, height=height, depth=depth)
                    )
        return ret
