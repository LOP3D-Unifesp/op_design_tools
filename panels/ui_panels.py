import bpy
import bmesh

# Classe base para a sidebar
class Sidebar:
    bl_category = "O&P Design"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

# Painel de Inicialização
class VIEW3D_PT_op_inicializacao(Sidebar, bpy.types.Panel):
    bl_label = "Inicialização"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("object.prepare_workspace", text="Preparar Ambiente", icon='SCENE_DATA')
        col.operator("import_mesh.stl_operator", text="Importar STL", icon='IMPORT')
        # Adicionar o botão de Alinhar aqui
        col.operator("object.align_object", text="Alinhar Modelo", icon='MOD_MIRROR')

# Painel de Análise
class VIEW3D_PT_print3d_analyze(Sidebar, bpy.types.Panel):
    bl_label = "Análise"

    _type_to_icon = {
        bmesh.types.BMVert: "VERTEXSEL",
        bmesh.types.BMEdge: "EDGESEL",
        bmesh.types.BMFace: "FACESEL",
    }

    def draw_report(self, context):
        # Importar o módulo report aqui para evitar circularidade
        from ..operators import report
        layout = self.layout
        info = report.info()

        if info:
            is_edit = context.edit_object is not None

            row = layout.row()
            row.label(text="Resultado")
            row.operator("wm.print3d_report_clear", text="", icon="X")

            box = layout.box()
            col = box.column()

            for i, (text, data) in enumerate(info):
                if is_edit and data and data[1]:
                    bm_type, _bm_array = data
                    col.operator("mesh.print3d_select_report", text=text, icon=self._type_to_icon[bm_type],).index = i
                else:
                    col.label(text=text)

    def draw(self, context):
        layout = self.layout

        # Secção do O&P Design
        col = layout.column(align=True)
        col.operator("object.align_object", text="Alinhar Modelo", icon='MOD_MIRROR')

        # Integração da análise de malha do addon
        print_3d = context.scene.print_3d

        layout.label(text="Estatísticas")
        row = layout.row(align=True)
        row.operator("mesh.print3d_info_volume", text="Volume")
        row.operator("mesh.print3d_info_area", text="Área")

        layout.label(text="Verificações")
        col = layout.column(align=True)
        col.operator("mesh.print3d_check_solid", text="Sólido")
        col.operator("mesh.print3d_check_intersect", text="Interseções")
        row = col.row(align=True)
        row.operator("mesh.print3d_check_degenerate", text="Degenerado")
        row.prop(print_3d, "threshold_zero", text="")
        row = col.row(align=True)
        row.operator("mesh.print3d_check_distort", text="Distorcido")
        row.prop(print_3d, "angle_distort", text="")
        row = col.row(align(True))
        row.operator("mesh.print3d_check_thick", text="Espessura")
        row.prop(print_3d, "thickness_min", text="")
        row = col.row(align(True))
        row.operator("mesh.print3d_check_sharp", text="Aresta Afiada")
        row.prop(print_3d, "angle_sharp", text="")
        row = col.row(align(True))
        row.operator("mesh.print3d_check_overhang", text="Overhang")
        row.prop(print_3d, "angle_overhang", text="")
        layout.operator("mesh.print3d_check_all", text="Verificar Tudo")

        self.draw_report(context)  # Exibir o relatório de análise de malha


# Registrar os painéis
classes = [
    VIEW3D_PT_op_inicializacao,
    VIEW3D_PT_print3d_analyze,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
