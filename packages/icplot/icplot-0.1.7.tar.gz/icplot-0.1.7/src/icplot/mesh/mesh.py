"""
Module for describing mesh elements. Goes for simplicity and low dependencies
over performance. Consider something else for high performance meshing.
"""

from __future__ import annotations
from dataclasses import dataclass

import numpy as np

from icplot.geometry import Point, Vector, Cuboid, Cylinder


@dataclass(frozen=True)
class Vertex:
    """
    A mesh vertext
    """

    x: float
    y: float
    z: float = 0.0
    id: int = -1

    @staticmethod
    def from_point(p: Point, id: int = -1) -> Vertex:
        return Vertex(p.x, p.y, p.z, id)

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    def get_distance(self, p: Point) -> float:
        return float(np.linalg.norm(p.as_array() - self.as_array()))


@dataclass(frozen=True)
class Edge:
    """
    A mesh edge - consists of two verts
    """

    vert0: int
    vert1: int
    type: str = "line"
    interp_points: tuple[Point, ...] = ()


@dataclass(frozen=True)
class Block:
    """
    A hex mesh element - used in openfoam meshing
    """

    vertices: tuple[int, ...]
    cell_counts: tuple[int, ...] = (1, 1, 1)
    grading: str = "simpleGrading"
    grading_ratios: tuple[int, ...] = (1, 1, 1)

    def get_top_edges(self) -> tuple:
        return (
            (self.vertices[0], self.vertices[1]),
            (self.vertices[1], self.vertices[2]),
            (self.vertices[2], self.vertices[3]),
            (self.vertices[3], self.vertices[0]),
        )

    def get_bottom_edges(self) -> tuple:
        return (
            (self.vertices[4], self.vertices[5]),
            (self.vertices[5], self.vertices[6]),
            (self.vertices[6], self.vertices[7]),
            (self.vertices[7], self.vertices[4]),
        )

    def get_side_edges(self) -> tuple:
        return (
            (self.vertices[0], self.vertices[4]),
            (self.vertices[1], self.vertices[5]),
            (self.vertices[2], self.vertices[6]),
            (self.vertices[3], self.vertices[7]),
        )

    def get_edges(self) -> tuple:
        return self.get_bottom_edges() + self.get_top_edges() + self.get_side_edges()


@dataclass(frozen=True)
class Patch:
    """
    A collection of mesh faces - used for openfoam boundaries
    """

    type: str
    name: str
    faces: tuple[tuple[int, ...], ...]


def is_between(v0: Vertex, v1: Vertex, p: Point, tol: float = 1.0e-4) -> bool:

    dv0v1 = np.linalg.norm(v1.as_array() - v0.as_array())
    dv0p = np.linalg.norm(v0.as_array() - p.as_array())
    dv1p = np.linalg.norm(v1.as_array() - p.as_array())
    return np.abs(dv0p + dv1p - dv0v1) < tol


def line_distance(v0: Vertex, v1: Vertex, p: Point) -> float:

    pv0 = p.as_array() - v0.as_array()
    v1v0 = v1.as_array() - v0.as_array()
    side0 = np.dot(pv0, v1v0)
    if side0 < 0.0:
        return float(np.linalg.norm(pv0))
    pv1 = p.as_array() - v1.as_array()
    side1 = np.dot(pv1, v0.as_array() - v1.as_array())
    if side1 < 0.0:
        return float(np.linalg.norm(pv1))
    length = np.linalg.norm(v1v0)
    proj = (side1 * v0.as_array() + side0 * v1.as_array()) / (length * length)
    return float(np.linalg.norm(p.as_array() - proj))


@dataclass(frozen=True)
class Mesh:
    """
    A mesh tailored for use in openfoam
    """

    vertices: tuple[Vertex, ...]
    blocks: tuple[Block, ...]
    edges: tuple[Edge, ...] = ()
    patches: tuple[Patch, ...] = ()
    scale: float = 1.0

    def select_edge(self, p: Point) -> tuple[int, int]:

        for b in self.blocks:
            for e in b.get_edges():
                if is_between(self.vertices[e[0]], self.vertices[e[1]], p):
                    return (e[0], e[1])
        raise RuntimeError("No edge found at selection point")

    def get_closest_edge(self, p: Point) -> tuple[int, int]:

        min_dist = -1.0
        closest_edges: tuple[int, int] = (-1, -1)
        for b in self.blocks:
            for e in b.get_edges():
                dist = line_distance(self.vertices[e[0]], self.vertices[e[1]], p)
                if min_dist == -1.0:
                    min_dist = dist
                    closest_edges = (e[0], e[1])
                    continue
                if dist < min_dist:
                    min_dist = dist
                    closest_edges = (e[0], e[1])
        return closest_edges


def from_cuboid(cuboid: Cuboid, elements_per_dim: int = 5) -> Mesh:

    verts = tuple(Vertex.from_point(p) for p in cuboid.points)

    cell_counts = (elements_per_dim, elements_per_dim, elements_per_dim)
    blocks = (Block(tuple(range(len(verts))), cell_counts),)
    return Mesh(verts, blocks)


def find_closest_vert(verts: list[Vertex], point: Point) -> int:

    if not verts:
        raise RuntimeError("Can't find nearest vert in empty list")

    min_id = -1
    min_distance = 0.0
    for idx, v in enumerate(verts):

        distance = v.get_distance(point)

        if idx == 0:
            min_id = idx
            min_distance = distance
            continue

        if distance < min_distance:
            min_id = idx
            min_distance = distance

    return min_id


def from_cuboids(
    cuboids: list[Cuboid], elements_per_dim: int = 5, merge_tolerance: float = 1.0e-4
) -> Mesh:

    verts: list = []
    block_vert_ids: list = []
    for cuboid in cuboids:
        vert_ids = []
        for p in cuboid.points:

            if not verts:
                verts.append(Vertex.from_point(p, 0))
                vert_ids.append(0)
                continue

            nearest_id = find_closest_vert(verts, p)
            if verts[nearest_id].get_distance(p) <= merge_tolerance:
                vert_ids.append(nearest_id)
            else:
                end_id = len(verts)
                verts.append(Vertex.from_point(p, end_id))
                vert_ids.append(end_id)
        block_vert_ids.append(vert_ids)

    cell_counts = (elements_per_dim, elements_per_dim, elements_per_dim)
    blocks = tuple(Block(tuple(b), cell_counts) for b in block_vert_ids)
    return Mesh(tuple(verts), blocks)


def from_cylinder(cylinder: Cylinder, boundary_frac: float = 0.66) -> Mesh:

    depth = (cylinder.diameter - boundary_frac * cylinder.diameter) / 2.0
    cuboids = [
        Cuboid(
            Point(0.0, 0.0, depth / 2.0),
            width=cylinder.diameter,
            height=cylinder.length,
            depth=depth,
            top_width_scale=boundary_frac,
        ),
        Cuboid(
            Point(0.0, 0.0, cylinder.diameter + depth / 2.0),
            width=cylinder.diameter,
            height=cylinder.length,
            depth=depth,
            normal=Vector(0.0, 0.0, -1.0),
            top_width_scale=boundary_frac,
        ),
        Cuboid(
            Point(-cylinder.diameter / 2.0, 0.0, cylinder.diameter / 2.0 + depth / 2.0),
            width=cylinder.diameter,
            height=cylinder.length,
            depth=depth,
            normal=Vector(1.0, 0.0, 0.0),
            top_width_scale=boundary_frac,
        ),
        Cuboid(
            Point(cylinder.diameter / 2.0, 0.0, cylinder.diameter / 2.0 + depth / 2.0),
            width=cylinder.diameter,
            height=cylinder.length,
            depth=depth,
            normal=Vector(-1.0, 0.0, 0.0),
            top_width_scale=boundary_frac,
        ),
        Cuboid(
            Point(0.0, 0.0, cylinder.diameter * boundary_frac / 2.0 + depth),
            width=cylinder.diameter * boundary_frac,
            height=cylinder.length,
            depth=boundary_frac * cylinder.diameter,
        ),
    ]

    mesh = from_cuboids(cuboids)

    top_front_edge = mesh.get_closest_edge(
        Point(0.0, -cylinder.length / 2.0, cylinder.diameter + depth / 2.0)
    )
    top_front_arc = Point(
        0.0, -cylinder.length / 2.0, cylinder.diameter + depth / 2.0 + 0.15
    )

    edges = (Edge(top_front_edge[0], top_front_edge[1], "arc", (top_front_arc,)),)

    return Mesh(mesh.vertices, mesh.blocks, edges=edges)
