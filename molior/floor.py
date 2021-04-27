import os
import sys
import ifcopenshell.api

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from molior.baseclass import BaseClass
from molior.geometry_2d import matrix_align

run = ifcopenshell.api.run


class Floor(BaseClass):
    """A floor filling a room or space"""

    def __init__(self, args={}):
        super().__init__(args)
        self.floor = 0.02
        self.id = ""
        self.ifc = "IFCSLAB"
        self.inner = 0.08
        self.path = []
        self.type = "molior-floor"
        for arg in args:
            self.__dict__[arg] = args[arg]
        # FIXME implement not_if_stair_below

    def Ifc(self, ifc, context):
        """Generate some ifc"""
        entity = run("root.create_entity", ifc, ifc_class="IfcSlab", name="Floor")
        ifc.assign_storey_byindex(entity, self.level)
        shape = ifc.createIfcShapeRepresentation(
            context,
            "Body",
            "SweptSolid",
            [
                ifc.createExtrudedAreaSolid(
                    [self.corner_in(index) for index in range(len(self.path))],
                    self.floor,
                )
            ],
        )
        run("geometry.assign_representation", ifc, product=entity, representation=shape)
        run(
            "geometry.edit_object_placement",
            ifc,
            product=entity,
            matrix=matrix_align([0.0, 0.0, self.elevation], [1.0, 0.0, 0.0]),
        )
