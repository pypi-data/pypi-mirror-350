from iccore.test_utils import get_test_output_dir

from icplot.geometry import Point, Cylinder, Cuboid
from icplot.mesh import foam, vtk, from_cylinder, from_cuboid


def test_closest_edge():

    cuboid = Cuboid()

    mesh = from_cuboid(cuboid)

    closest_edge = mesh.get_closest_edge(Point(0.0, -0.5, -0.5))

    assert closest_edge[0] == 0
    assert closest_edge[1] == 1


def test_mesh():

    output_dir = get_test_output_dir()

    cylinder = Cylinder(loc=Point(0.0, 0.0, 0.0), length=2.0, diameter=1.0)

    mesh = from_cylinder(cylinder)
    vtk.write_mesh(mesh, output_dir / "cylinder.vtk")
    # return

    foam_str = foam.mesh_to_foam(mesh)

    assert foam_str

    if not foam.has_openfoam():
        return

    foam.generate_mesh(mesh, output_dir)
