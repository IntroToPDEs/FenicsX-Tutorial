import gmsh
gmsh.initialize()

# The next step is to create the membrane and start the computations by the GMSH CAD kernel, to generate the relevant underlying data structures. The first arguments of `addDisk` are the x, y and z coordinate of the center of the circle, while the two last arguments are the x-radius and y-radius.

domain = gmsh.model.occ.addRectangle(-1, -1, 0, 2, 2)
gmsh.model.occ.synchronize()

# After that, we make the membrane a physical surface, such that it is recognized by `gmsh` when generating the mesh. As a surface is a two-dimensional entity, we add `2` as the first argument, the entity tag of the membrane as the second argument, and the physical tag as the last argument. In a later demo, we will get into when this tag matters.

gdim = 2
gmsh.model.addPhysicalGroup(gdim, [domain], 1)

# Finally, we generate the two-dimensional mesh. We set a uniform mesh size by modifying the GMSH options.

gmsh.option.setNumber("Mesh.CharacteristicLengthMin",0.05)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax",0.05)
gmsh.model.mesh.generate(gdim)


from dolfinx.io import gmshio
from mpi4py import MPI

gmsh_model_rank = 0
mesh_comm = MPI.COMM_WORLD
domain, cell_markers, facet_markers = gmshio.model_to_mesh(gmsh.model, mesh_comm, gmsh_model_rank, gdim=gdim)

from dolfinx import fem
import ufl
p = 1
Ue = ufl.FiniteElement("CG", domain.ufl_cell(), p)
V = fem.FunctionSpace(domain, Ue)

from dolfinx.plot import create_vtk_mesh
import pyvista
pyvista.start_xvfb()

# Extract topology from mesh and create pyvista mesh
topology, cell_types, x = create_vtk_mesh(V)
grid = pyvista.UnstructuredGrid(topology, cell_types, x)
grid.plot(show_edges=True)
# Visualizzation in Paraview
import dolfinx.io
with dolfinx.io.XDMFFile(MPI.COMM_WORLD, "mesh.xdmf", "w") as xdmf:
    xdmf.write_mesh(domain)

