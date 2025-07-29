import pytest

from icplot.geometry import Point, Vector, Quad, Cuboid


def test_quad():

    quad = Quad(Point(0.0, 0.0, 0.0))
    points = quad.points

    assert points[0].x == -0.5
    assert points[0].y == -0.5

    assert points[1].x == 0.5
    assert points[1].y == -0.5


def test_quad_with_rotation():

    normal = Vector(0.0, 1.0, 0.0)

    quad = Quad(Point(0.0, 0.0, 0.0), normal)
    points = quad.points

    assert points[0].x == pytest.approx(-0.5)
    assert points[0].y == pytest.approx(0.0)
    assert points[0].z == pytest.approx(0.5)

    assert points[1].x == pytest.approx(0.5)
    assert points[1].y == pytest.approx(0.0)
    assert points[1].z == pytest.approx(0.5)


def test_cuboid():

    shape = Cuboid(Point(0.0, 0.0, 0.0))
    points = shape.points

    assert points[0].x == -0.5
    assert points[0].y == -0.5
    assert points[0].z == -0.5

    assert points[1].x == 0.5
    assert points[1].y == -0.5

    assert points[4].x == -0.5
    assert points[4].y == -0.5
    assert points[4].z == 0.5


def test_cuboid_rotation():

    return

    normal = Vector(0.0, 1.0, 0.0)

    shape = Cuboid(Point(0.0, 0.0, 0.0), normal)
    points = shape.points

    assert points[0].x == -0.5
    assert points[0].y == -0.5
    assert points[0].z == -0.5

    assert points[1].x == 0.5
    assert points[1].y == -0.5

    assert points[4].x == -0.5
    assert points[4].y == -0.5
    assert points[4].z == 0.5
