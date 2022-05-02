#!/usr/bin/python3

"""brep2ifc - convert BREP geometry into an IFC building

This example script illustrates how to implement the homemaker-addon
functionality without any blender dependencies.

Usage:
    brep2ifc.py mygeometry.brep mybuilding.ifc

"""
import sys, os, datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from topologic import Topology, Vertex, CellComplex, TopologyUtility
from molior import Molior

print("Start", datetime.datetime.now())
brep_file = open(sys.argv[1], "r")
topology = Topology.ByString(brep_file.read())
print("BREP imported", datetime.datetime.now())

origin = Vertex.ByCoordinates(0.0, 0.0, 0.0)
# topology_scaled = TopologyUtility.Scale(topology, origin, 0.3048, 0.3048, 0.3048)
# print("BREP scale from feet to metres", datetime.datetime.now())
topology_scaled = TopologyUtility.Scale(topology, origin, 1.0, 1.0, 1.0)

faces_ptr = []
topology_scaled.Faces(faces_ptr)
print(str(len(faces_ptr)), "faces", datetime.datetime.now())

cc = CellComplex.ByFaces(faces_ptr, 0.0001)
print("CellComplex created", datetime.datetime.now())

# Give every Cell and Face an index number
cc.IndexTopology()
# Copy styles from Faces to the CellComplex
# cc.ApplyDictionary(faces_ptr)
# Assign Cell usages from widgets
cc.AllocateCells([])
# Generate a cirulation Graph
circulation = cc.Adjacency()
circulation.Circulation(cc)
print("Circulation Graph generated", datetime.datetime.now())

# Traces are 2D paths that define walls, extrusions and rooms
traces, normals, elevations = cc.GetTraces()
hulls = cc.GetHulls()
print("Traces calculated", datetime.datetime.now())

molior_object = Molior(
    circulation=circulation,
    traces=traces,
    name="brep2ifc building",
    elevations=elevations,
    hulls=hulls,
    normals=normals,
    cellcomplex=cc,
)
molior_object.execute()
print("IFC model created", datetime.datetime.now())

molior_object.file.write(sys.argv[2])
