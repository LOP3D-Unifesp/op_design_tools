import bpy
import os
import platform

class IMPORT_MESH_OT_stl(bpy.types.Operator):
    bl_idname = "import_mesh.stl_operator"
    bl_label = "Importar STL"
    bl_description = "Importa um arquivo STL para a cena"

    def execute(self, context):
        # Verificar o sistema operacional
        if platform.system() == "Windows":
            # Windows: Obter o caminho da pasta Documentos
            documents_dir = os.path.join(os.getenv('USERPROFILE'), 'Documents')
        elif platform.system() == "Linux":
            # Linux: Usar o caminho padrão ~/Documents
            documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
        else:
            # Em sistemas desconhecidos (como macOS), usa o home como fallback
            documents_dir = os.path.expanduser("~")
        
        # Chama o operador nativo do Blender para importar STL, configurando o diretório inicial
        bpy.ops.import_mesh.stl('INVOKE_DEFAULT', filepath=documents_dir)
        return {'FINISHED'}

# Registrar o operador
def register():
    bpy.utils.register_class(IMPORT_MESH_OT_stl)

def unregister():
    bpy.utils.unregister_class(IMPORT_MESH_OT_stl)
