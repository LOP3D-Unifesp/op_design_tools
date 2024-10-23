import bpy
from .operators.align import OBJECT_OT_AlignObject
from .operators.setup import OBJECT_OT_PrepareWorkspace
from .panels.ui_panels import VIEW3D_PT_op_inicializacao
from .operators.import_mesh import IMPORT_MESH_OT_stl

bl_info = {
    "name": "O&P Design Tools",
    "blender": (2, 90, 0),
    "category": "Object",
}

# Registrar e desregistrar classes
opdesign_classes = [
    OBJECT_OT_AlignObject,
    OBJECT_OT_PrepareWorkspace,
    VIEW3D_PT_op_inicializacao,
    IMPORT_MESH_OT_stl,
]

def register():

    # Registrar todas as classes
    for cls in opdesign_classes:
        bpy.utils.register_class(cls)

def unregister():
    # Desregistrar todas as classes
    for cls in opdesign_classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
