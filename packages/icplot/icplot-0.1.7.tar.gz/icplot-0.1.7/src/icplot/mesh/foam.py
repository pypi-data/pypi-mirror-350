"""
Meshing utilities for use in openfoam
"""

import shutil
import subprocess
import os
from pathlib import Path
from dataclasses import dataclass

from .mesh import Mesh, Block, Edge, Patch


@dataclass(frozen=True)
class FoamFile:

    version: str = "2.0"
    format: str = "ascii"
    arch: str = "LSB;label=32;scalar=64"
    foam_class: str = "dictionary"
    location: str = "system"
    object: str = "blockMeshDict"


def _get_foam_header(spec: FoamFile) -> str:

    output = "FoamFile\n{"
    output += f"\tversion\t{spec.version};\n"
    output += f"\tformat\t{spec.format};\n"
    output += f'\tarch\t"{spec.arch}";\n'
    output += f"\tclass\t{spec.foam_class};\n"
    output += f'\tlocation\t"{spec.location}";\n'
    output += f"\tobject\t{spec.object};\n"
    output += "}\n\n"
    return output


def has_openfoam() -> bool:
    return bool(shutil.which("openfoam")) and bool(shutil.which("blockMesh"))


def _mesh_blocks(blocks: tuple[Block, ...]) -> str:

    output = "blocks\n(\n"
    for b in blocks:
        verts = " ".join(str(v) for v in b.vertices)
        output += f"\thex ({verts})\n"

        counts = " ".join(str(c) for c in b.cell_counts)
        output += f"\t({counts})\n"

        grades = " ".join(str(g) for g in b.grading_ratios)
        output += f"\t{b.grading} ({grades})\n"
    output += ");\n\n"
    return output


def _mesh_edges(edges: tuple[Edge, ...]) -> str:

    if not edges:
        return ""

    output = "edges\n(\n"
    for e in edges:
        if e.type == "line":
            output += f"\tline {e.vert0} {e.vert1}\n"
        else:
            interps = ""
            for p in e.interp_points:
                interps += f"({p.x} {p.y} {p.z}) "
            output += f"\t {e.type} {e.vert0} {e.vert1} {interps}\n"
    output += ");\n\n"
    return output


def _mesh_boundaries(patches: tuple[Patch, ...]) -> str:

    if not patches:
        return ""

    output = "boundary\n(\n"
    for patch in patches:
        output += f"\t{patch.name}\n"
        output += "\t{\n"
        output += f"\t\ttype {patch.type};\n"
        output += "\t\tfaces\n\t\t(\n"
        for f in patch.faces:
            faces = " ".join(str(idx) for idx in f)
            output += f"\t\t\t({faces})\n"
        output += "\t\t);\n"
        output += "\t}\n"
    output += ");\n\n"
    return output


def mesh_to_foam(mesh: Mesh, spec: FoamFile = FoamFile()) -> str:
    """
    Given a mesh, write it in openfoam blockMesh format
    """

    output = _get_foam_header(spec)

    output += f"scale\t{mesh.scale};\n"

    output += "vertices\n(\n"
    for idx, v in enumerate(mesh.vertices):
        output += f"\t( {v.x} {v.y} {v.z} ) // # {idx} \n"
    output += ");\n\n"

    output += _mesh_edges(mesh.edges)

    output += _mesh_blocks(mesh.blocks)

    output += _mesh_boundaries(mesh.patches)

    return output


def generate_mesh(mesh: Mesh, case_dir: Path):

    if not has_openfoam():
        raise RuntimeError("Openfoam not found, can't generate mesh")

    system_dir = case_dir / "system"
    os.makedirs(system_dir, exist_ok=True)

    mesh_str = mesh_to_foam(mesh)
    mesh_file = system_dir / "blockMeshDict"
    with open(mesh_file, "w", encoding="utf-8") as f:
        f.write(mesh_str)

    control_dict = system_dir / "controlDict"
    if not control_dict.exists():
        shutil.copy(Path(__file__).parent / "controlDict", control_dict)

    cmd = f"blockMesh -case {case_dir}"
    subprocess.run(cmd, cwd=case_dir, shell=True, check=True)

    cmd = f"blockMesh -case {case_dir} -write-vtk"
    subprocess.run(cmd, cwd=case_dir, shell=True, check=True)
