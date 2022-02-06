"""Overloads domain-specific methods onto topologic.Face"""

from functools import lru_cache
import topologic
from topologic import Vertex, Edge, Face, FaceUtility, CellUtility
import topologist.ugraph as ugraph


def ByVertices(vertices):
    """Create a Face from an ordered set of Vertices"""
    edges_ptr = []
    for i in range(len(vertices) - 1):
        v1 = vertices[i]
        v2 = vertices[i + 1]
        e1 = Edge.ByStartVertexEndVertex(v1, v2)
        edges_ptr.append(e1)
    # connect the last vertex to the first one
    v1 = vertices[len(vertices) - 1]
    v2 = vertices[0]
    e1 = Edge.ByStartVertexEndVertex(v1, v2)
    edges_ptr.append(e1)
    return Face.ByEdges(edges_ptr)


setattr(topologic.Face, "ByVertices", ByVertices)


@lru_cache(maxsize=256)
def CellsOrdered(self, host_topology):
    """Front Cell and back Cell, can be None"""
    centroid = FaceUtility.InternalVertex(self, 0.001).Coordinates()
    normal = self.Normal()
    vertex_front = Vertex.ByCoordinates(
        centroid[0] + (normal[0] / 10),
        centroid[1] + (normal[1] / 10),
        centroid[2] + (normal[2] / 10),
    )
    vertex_back = Vertex.ByCoordinates(
        centroid[0] - (normal[0] / 10),
        centroid[1] - (normal[1] / 10),
        centroid[2] - (normal[2] / 10),
    )

    results = [None, None]
    if host_topology:
        cells_ptr = self.Cells_Cached(host_topology)
        for cell in cells_ptr:
            if CellUtility.Contains(cell, vertex_front, 0.001) == 0:
                results[0] = cell
            elif CellUtility.Contains(cell, vertex_back, 0.001) == 0:
                results[1] = cell
    return results


def VerticesPerimeter(self, vertices_ptr):
    """Vertices, tracing the outer perimeter"""
    # FIXME does return self.ExternalBoundary().Vertices(None, vertices_ptr) do the same thing?
    wires_ptr = []
    self.Wires(None, wires_ptr)
    wires_ptr[0].Vertices(None, vertices_ptr)
    return vertices_ptr


def BadNormal(self, cellcomplex):
    """Faces on outside of CellComplex are orientated correctly, but 'outside'
    Faces inside the CellComplex have random orientation. Tag them with 'badnormal'
    if Face doesn't face 'out'"""
    if not self.IsWorld(cellcomplex):
        cells = self.CellsOrdered(cellcomplex)
        if cells[0] == None or cells[1] == None:
            self.Set("badnormal", True)
            return True
        if cells[1].IsOutside() and not cells[0].IsOutside():
            self.Set("badnormal", True)
            return True
    return False


def IsVertical(self):
    normal_stl = FaceUtility.NormalAtParameters(self, 0.5, 0.5)
    if abs(normal_stl[2]) < 0.0001:
        return True
    return False


def IsHorizontal(self):
    normal_stl = FaceUtility.NormalAtParameters(self, 0.5, 0.5)
    if abs(normal_stl[2]) > 0.9999:
        return True
    return False


def IsUpward(self):
    normal = self.Normal()
    if normal[2] > 0.0:
        return True
    return False


def AxisOuter(self):
    """2D bottom edge of a vertical face, for external walls, anti-clockwise in plan"""
    edges_ptr = []
    self.EdgesBottom(edges_ptr)
    if len(edges_ptr) > 0:
        unordered = ugraph.graph()
        for edge in edges_ptr:
            start_coor = edge.StartVertex().CoorAsString()
            end_coor = edge.EndVertex().CoorAsString()
            unordered.add_edge(
                {
                    start_coor: [
                        end_coor,
                        {
                            "start_vertex": edge.StartVertex(),
                            "end_vertex": edge.EndVertex(),
                        },
                    ]
                }
            )
        ordered = unordered.find_chains()[0]
        ordered_edges = ordered.edges()
        first_edge = ordered_edges[0][0]
        last_edge = ordered_edges[-1][0]
        if self.Get("badnormal"):
            return [
                ordered.graph[first_edge][1]["end_vertex"],
                ordered.graph[last_edge][1]["start_vertex"],
            ]
        else:
            return [
                ordered.graph[first_edge][1]["start_vertex"],
                ordered.graph[last_edge][1]["end_vertex"],
            ]


# FIXME doesn't appear to be in use
def AxisOuterTop(self):
    """2D top edge of a vertical face, for external walls, anti-clockwise in plan"""
    edges_ptr = []
    self.EdgesTop(edges_ptr)
    if len(edges_ptr) > 0:
        unordered = ugraph.graph()
        for edge in edges_ptr:
            start_coor = edge.StartVertex().CoorAsString()
            end_coor = edge.EndVertex().CoorAsString()
            unordered.add_edge(
                {
                    start_coor: [
                        end_coor,
                        {
                            "start_vertex": edge.StartVertex(),
                            "end_vertex": edge.EndVertex(),
                        },
                    ]
                }
            )
        ordered = unordered.find_chains()[0]
        ordered_edges = ordered.edges()
        first_edge = ordered_edges[0][0]
        last_edge = ordered_edges[-1][0]
        if self.Get("badnormal"):
            return [
                ordered.graph[last_edge][1]["start_vertex"],
                ordered.graph[first_edge][1]["end_vertex"],
            ]
        else:
            return [
                ordered.graph[last_edge][1]["end_vertex"],
                ordered.graph[first_edge][1]["start_vertex"],
            ]


@lru_cache(maxsize=256)
def IsInternal(self, host_topology):
    """Face between two indoor cells"""
    cells_ptr = self.Cells_Cached(host_topology)
    if len(cells_ptr) == 2:
        for cell in cells_ptr:
            if cell.IsOutside():
                return False
        return True
    return False


@lru_cache(maxsize=256)
def IsExternal(self, host_topology):
    """Face between indoor cell and outdoor cell (or world)"""
    cells_ptr = self.Cells_Cached(host_topology)
    if len(cells_ptr) == 2:
        if cells_ptr[0].IsOutside() and not cells_ptr[1].IsOutside():
            return True
        if cells_ptr[1].IsOutside() and not cells_ptr[0].IsOutside():
            return True
    elif len(cells_ptr) == 1:
        if not cells_ptr[0].IsOutside():
            return True
    return False


@lru_cache(maxsize=256)
def IsWorld(self, host_topology):
    """Face on outside of mesh"""
    cells_ptr = self.Cells_Cached(host_topology)
    if len(cells_ptr) == 1:
        return True
    return False


@lru_cache(maxsize=256)
def IsOpen(self, host_topology):
    """Face on outdoor cell on outside of mesh"""
    cells_ptr = self.Cells_Cached(host_topology)
    if len(cells_ptr) == 1:
        for cell in cells_ptr:
            if cell.IsOutside():
                return True
    return False


# FIXME doesn't appear to be in use
def FaceAbove(self, host_topology):
    """Does this Face have a vertical Face attached to a horizontal top Edge?"""
    edges_ptr = []
    self.EdgesTop(edges_ptr)
    for edge in edges_ptr:
        faces_ptr = edge.Faces_Cached(host_topology)
        for face in faces_ptr:
            if face.IsVertical() and not face.IsSame(self):
                return face
    return None


def FacesBelow(self, host_topology):
    """Does this Face have Faces attached below a horizontal bottom Edge?"""
    edges_ptr = []
    self.EdgesBottom(edges_ptr)
    result = []
    for edge in edges_ptr:
        faces_below = edge.FacesBelow(host_topology)
        if faces_below:
            result.extend(faces_below)
    return result


def CellsBelow(self, host_topology):
    """Does this Face have Cells attached below a horizontal bottom Edge?"""
    edges_ptr = []
    self.EdgesBottom(edges_ptr)
    result = []
    for edge in edges_ptr:
        cells_below = edge.CellsBelow(host_topology)
        if cells_below:
            result.extend(cells_below)
    return result


# FIXME doesn't appear to be in use
def HorizontalFacesSideways(self, host_topology):
    """Which horizontal faces are attached to the bottom Edges of this Face?"""
    edges_ptr = []
    self.EdgesBottom(edges_ptr)
    result_faces_ptr = []
    for edge in edges_ptr:
        faces_ptr = edge.Faces_Cached(host_topology)
        for face in faces_ptr:
            if face.IsHorizontal() and not face.IsSame(self):
                result_faces_ptr.append(face)
    return result_faces_ptr


def Normal(self):
    """Normal for this Face, but flipped if tagged with 'badnormal'"""
    normal_stl = FaceUtility.NormalAtParameters(self, 0.5, 0.5)
    if self.Get("badnormal"):
        return [-normal_stl[0], -normal_stl[1], -normal_stl[2]]
    else:
        return [normal_stl[0], normal_stl[1], normal_stl[2]]


def TopLevelConditions(self, host_topology):
    """Assuming this is a vertical external wall, how do the top edges continue?"""
    # FIXME treats condition where above is an open wall same as eave
    result = []
    edges_ptr = []
    self.EdgesTop(edges_ptr)
    for edge in edges_ptr:
        faces_ptr = edge.FacesExternal(host_topology)
        for (
            face
        ) in faces_ptr:  # there should only be one external face (not including self)
            if face.IsSame(self):
                continue
            # top face tilts backward (roof) if normal faces up, forward (soffit) if faces down
            normal = face.Normal()
            condition = "top"
            if abs(normal[2]) < 0.0001:
                condition += "-vertical"
            elif normal[2] > 0.0:
                condition += "-backward"
            else:
                condition += "-forward"
            # top face can be above or below top edge
            if abs(normal[2]) > 0.9999:
                condition += "-level"
            elif face.Centroid().Z() > edge.Centroid().Z():
                condition += "-up"
            else:
                condition += "-down"
            result.append([edge, condition])
    return result


def BottomLevelConditions(self, host_topology):
    """Assuming this is a vertical external wall, how do the bottom edges continue?"""
    # FIXME treats condition where below is an open wall same as footing
    result = []
    edges_ptr = []
    self.EdgesBottom(edges_ptr)
    for edge in edges_ptr:
        faces_ptr = edge.FacesExternal(host_topology)
        for (
            face
        ) in faces_ptr:  # there should only be one external face (not including self)
            if face.IsSame(self):
                continue
            # bottom face tilts forward (roof) if normal faces up, backward (soffit) if faces down
            normal = face.Normal()
            condition = "bottom"
            if abs(normal[2]) < 0.0001:
                condition += "-vertical"
            elif normal[2] > 0.0:
                condition += "-forward"
            else:
                condition += "-backward"
            # bottom face can be above or below bottom edge
            if abs(normal[2]) > 0.9999:
                condition += "-level"
            elif face.Centroid().Z() > edge.Centroid().Z():
                condition += "-up"
            else:
                condition += "-down"
            result.append([edge, condition])
    return result


setattr(topologic.Face, "CellsOrdered", CellsOrdered)
setattr(topologic.Face, "VerticesPerimeter", VerticesPerimeter)
setattr(topologic.Face, "BadNormal", BadNormal)
setattr(topologic.Face, "IsVertical", IsVertical)
setattr(topologic.Face, "IsHorizontal", IsHorizontal)
setattr(topologic.Face, "IsUpward", IsUpward)
setattr(topologic.Face, "AxisOuter", AxisOuter)
setattr(topologic.Face, "AxisOuterTop", AxisOuterTop)
setattr(topologic.Face, "IsInternal", IsInternal)
setattr(topologic.Face, "IsExternal", IsExternal)
setattr(topologic.Face, "IsWorld", IsWorld)
setattr(topologic.Face, "IsOpen", IsOpen)
setattr(topologic.Face, "FaceAbove", FaceAbove)
setattr(topologic.Face, "FacesBelow", FacesBelow)
setattr(topologic.Face, "CellsBelow", CellsBelow)
setattr(topologic.Face, "HorizontalFacesSideways", HorizontalFacesSideways)
setattr(topologic.Face, "Normal", Normal)
setattr(topologic.Face, "TopLevelConditions", TopLevelConditions)
setattr(topologic.Face, "BottomLevelConditions", BottomLevelConditions)
