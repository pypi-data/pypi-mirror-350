from pathlib import Path
import os
import logging

from .mesh import Mesh

_HAS_VTK = True
try:
    import vtk
except ImportError as e:
    logging.getLogger(__name__).warning(
        "Disabling VTK stupport. Failed to load with: %s", e
    )
    _HAS_VTK = False


def has_vtk() -> bool:
    return _HAS_VTK


def write_mesh(mesh: Mesh, path: Path):

    if not has_vtk():
        raise RuntimeError("VTK support failed to load")

    os.makedirs(path.parent, exist_ok=True)

    points = vtk.vtkPoints()
    for v in mesh.vertices:
        points.InsertNextPoint(v.x, v.y, v.z)

    grid = vtk.vtkUnstructuredGrid()
    grid.SetPoints(points)
    for block in mesh.blocks:
        cell = vtk.vtkHexahedron()
        for idx, v_id in enumerate(block.vertices):
            cell.GetPointIds().SetId(idx, v_id)
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetInputData(grid)
    writer.SetFileName(path)
    writer.SetFileTypeToASCII()
    writer.Write()
