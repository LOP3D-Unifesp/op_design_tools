import bpy
import os
import shutil
import tempfile

class OBJECT_OT_PrepareWorkspace(bpy.types.Operator):
    bl_idname = "object.prepare_workspace"
    bl_label = "Preparar Ambiente"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Obter o caminho do arquivo do addon
        addon_directory = os.path.dirname(__file__)
        template_path = os.path.join(addon_directory, "..", "assets", "template.blend")

        # Criar um arquivo temporário com prefixo "op_unsaved_"
        temp_file = tempfile.NamedTemporaryFile(prefix="op_unsaved_", delete=False, suffix=".blend")
        temp_template_path = temp_file.name  # Caminho do arquivo temporário

        # Copiar o template para o arquivo temporário
        shutil.copyfile(template_path, temp_template_path)

        # Carregar o arquivo temporário no Blender
        bpy.ops.wm.open_mainfile(filepath=temp_template_path)

        # Usar um timer para aplicar as configurações após a cena ser carregada
        bpy.app.timers.register(self.apply_view_settings)

        return {'FINISHED'}

    def apply_view_settings(self):
        # Esperar até que o contexto esteja pronto
        try:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    space_data = area.spaces.active
                    region_3d = space_data.region_3d
                    
                    # Ativar visão ortográfica
                    region_3d.view_perspective = 'ORTHO'

                    # Oclusão de faces traseiras (Backface Culling)
                    space_data.shading.show_backface_culling = True

                    # Escala da grade
                    space_data.overlay.grid_scale = 0.001

                    # Configuração da resolução de visualização do modelo (shade smooth)
                    for obj in bpy.context.view_layer.objects:
                        if obj.type == 'MESH':
                            # Aplicar sombreamento suave
                            bpy.ops.object.shade_smooth()

            # Mensagem de sucesso
            self.report({'INFO'}, "Ambiente configurado com sucesso!")
        except AttributeError:
            # Retorna None para continuar o timer até que o contexto esteja pronto
            return 0.1

        # Retornar None para encerrar o timer
        return None

# Registrar o operador no Blender
def register():
    bpy.utils.register_class(OBJECT_OT_PrepareWorkspace)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_PrepareWorkspace)

if __name__ == "__main__":
    register()
