"""Overloads domain-specific methods onto topologic.Topology"""

from functools import lru_cache
import topologic
from topologic import StringAttribute, Vertex
from topologist.helpers import el


@lru_cache(maxsize=256)
def Cells_Cached(self, host_topology):
    cells_ptr = []
    self.Cells(host_topology, cells_ptr)
    return cells_ptr


@lru_cache(maxsize=256)
def Faces_Cached(self, host_topology):
    faces_ptr = []
    self.Faces(host_topology, faces_ptr)
    return faces_ptr


def FacesVertical(self, faces_ptr):
    elements_ptr = []
    self.Faces(None, elements_ptr)
    for face in elements_ptr:
        if face.IsVertical():
            faces_ptr.append(face)


def FacesHorizontal(self, faces_ptr):
    elements_ptr = []
    self.Faces(None, elements_ptr)
    for face in elements_ptr:
        if face.IsHorizontal():
            faces_ptr.append(face)


def FacesInclined(self, faces_ptr):
    if self.__class__ == Vertex:
        # FIXME Topologic segfaults if self is a Vertex
        return
    elements_ptr = []
    self.Faces(None, elements_ptr)
    for face in elements_ptr:
        if not face.IsHorizontal() and not face.IsVertical():
            faces_ptr.append(face)


def FacesExternal(self, host_topology):
    """searches host not sub-topologies"""
    faces_ptr = []
    elements_ptr = self.Faces_Cached(host_topology)
    for face in elements_ptr:
        if face.IsExternal(host_topology):
            faces_ptr.append(face)
    return faces_ptr


@lru_cache(maxsize=256)
def Elevation(self):
    lowest = 9999999.9
    vertices_ptr = []
    self.Vertices(None, vertices_ptr)
    for vertex in vertices_ptr:
        if vertex.Z() < lowest:
            lowest = vertex.Z()
    return el(lowest)


@lru_cache(maxsize=256)
def Height(self):
    highest = -9999999.9
    vertices_ptr = []
    self.Vertices(None, vertices_ptr)
    for vertex in vertices_ptr:
        if vertex.Z() > highest:
            highest = vertex.Z()
    return el(highest - self.Elevation())


def Mesh(self):
    """A list of node coordinates and a list of faces"""
    vertices_ptr = []
    self.Vertices(None, vertices_ptr)
    vertices = [vertex.Coordinates() for vertex in vertices_ptr]

    faces_ptr = []
    self.Faces(None, faces_ptr)
    faces = []
    for face in faces_ptr:
        wire_vertices_ptr = []
        face.ExternalBoundary().Vertices(None, wire_vertices_ptr)
        faces.append([self.VertexId(vertex) for vertex in wire_vertices_ptr])
    return vertices, faces


def EdgesTop(self, result_edges_ptr):
    """A list of horizontal edges at the highest level of this face"""
    edges_ptr = []
    self.Edges(None, edges_ptr)
    level = el(self.Elevation() + self.Height())
    for edge in edges_ptr:
        vertex_start = edge.StartVertex()
        vertex_end = edge.EndVertex()
        if el(vertex_start.Z()) == level and el(vertex_end.Z()) == level:
            result_edges_ptr.append(edge)


def EdgesBottom(self, result_edges_ptr):
    """A list of horizontal edges at the lowest level of this face"""
    edges_ptr = []
    self.Edges(None, edges_ptr)
    level = self.Elevation()
    for edge in edges_ptr:
        vertex_start = edge.StartVertex()
        vertex_end = edge.EndVertex()
        if el(vertex_start.Z()) == level and el(vertex_end.Z()) == level:
            result_edges_ptr.append(edge)


def EdgesCrop(self, result_edges_ptr):
    """Which edges are not vertical or top/bottom?"""
    edges_ptr = []
    self.Edges(None, edges_ptr)
    bottom = self.Elevation()
    top = el(self.Elevation() + self.Height())
    for edge in edges_ptr:
        vertex_start = edge.StartVertex()
        vertex_end = edge.EndVertex()
        if el(vertex_start.Z()) == top and el(vertex_end.Z()) == top:
            continue
        elif el(vertex_start.Z()) == bottom and el(vertex_end.Z()) == bottom:
            continue
        elif edge.IsVertical():
            continue
        result_edges_ptr.append(edge)


def Set(self, key, value):
    """Simple string value dictionary access"""
    dictionary = self.GetDictionary()
    if dictionary.ContainsKey(str(key)):
        dictionary.Remove(str(key))
    dictionary.Add(str(str(key)), StringAttribute(str(value)))
    self.SetDictionary(dictionary)


def Get(self, key):
    """Simple string value dictionary access"""
    dictionary = self.GetDictionary()
    if dictionary.ContainsKey(str(key)):
        value = dictionary.ValueAtKey(str(key))
        return str(value.StringValue())
    return None


def DumpDictionary(self):
    dictionary = self.GetDictionary()
    keys = dictionary.Keys()
    result = {}
    for key in keys:
        value = self.Get(str(key))
        result[str(key)] = value
    return result


def GraphVertex(self, graph):
    index = self.Get("index")
    myclass = type(self).__name__
    if not index == None:
        vertices_ptr = []
        graph.Vertices(vertices_ptr)
        for vertex in vertices_ptr:
            if vertex.Get("index") == index and vertex.Get("class") == myclass:
                return vertex


@lru_cache(maxsize=256)
def VertexId(self, vertex):
    i = 0
    vertices_ptr = []
    self.Vertices(None, vertices_ptr)
    for v in vertices_ptr:
        if v.IsSame(vertex):
            return i
        i += 1


setattr(topologic.Topology, "Cells_Cached", Cells_Cached)
setattr(topologic.Topology, "Faces_Cached", Faces_Cached)
setattr(topologic.Topology, "FacesVertical", FacesVertical)
setattr(topologic.Topology, "FacesHorizontal", FacesHorizontal)
setattr(topologic.Topology, "FacesInclined", FacesInclined)
setattr(topologic.Topology, "FacesExternal", FacesExternal)
setattr(topologic.Topology, "Elevation", Elevation)
setattr(topologic.Topology, "Height", Height)
setattr(topologic.Topology, "Mesh", Mesh)
setattr(topologic.Topology, "EdgesTop", EdgesTop)
setattr(topologic.Topology, "EdgesBottom", EdgesBottom)
setattr(topologic.Topology, "EdgesCrop", EdgesCrop)
setattr(topologic.Topology, "Set", Set)
setattr(topologic.Topology, "Get", Get)
setattr(topologic.Topology, "DumpDictionary", DumpDictionary)
setattr(topologic.Topology, "GraphVertex", GraphVertex)
setattr(topologic.Topology, "VertexId", VertexId)
