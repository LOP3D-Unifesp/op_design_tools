import bpy
from ..features.align_helpers import (
    set_geometry_origin_to_center,
    move_object_to_origin,
    align_model_to_axes,
    standardize_hand_orientation,
    set_object_final_position,
    focus_view_on_object,
    set_view_to_front
)

class OBJECT_OT_AlignObject(bpy.types.Operator):
    bl_idname = "object.align_object"
    bl_label = "Alinhar Modelo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            set_geometry_origin_to_center()
            move_object_to_origin()
            align_model_to_axes()
            standardize_hand_orientation()
            set_object_final_position()
            focus_view_on_object()
            set_view_to_front()
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
