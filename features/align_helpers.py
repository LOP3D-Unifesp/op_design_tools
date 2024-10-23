import bpy
import math
from mathutils import Vector

# Função para garantir que estamos no modo objeto
def ensure_object_mode():
    if bpy.context.object is not None and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

# Função para garantir que o objeto está selecionado e ativo
def ensure_object_selected():
    obj = bpy.context.view_layer.objects.active
    if obj is None:
        raise ValueError("Nenhum objeto selecionado. Selecione um objeto antes de continuar.")
    return obj

# Função para centralizar a origem do objeto no centro da geometria
def set_geometry_origin_to_center():
    ensure_object_mode()
    obj = ensure_object_selected()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    print(f"Centro da geometria ajustado para o centro da malha do objeto {obj.name}")

# Função para mover o objeto para a origem mundial (0, 0, 0)
def move_object_to_origin():
    ensure_object_mode()
    obj = ensure_object_selected()
    obj.location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=True)
    print(f"Objeto {obj.name} movido para a origem (0, 0, 0)")

# Função para alinhar o modelo em relação aos eixos predefinidos
def align_model_to_axes():
    ensure_object_mode()
    obj = ensure_object_selected()

    # Tentar alinhar a maior dimensão do objeto com o eixo Y
    dimensions = obj.dimensions
    if dimensions.x > dimensions.y and dimensions.x > dimensions.z:
        obj.rotation_euler = (0, 0, math.radians(90))
    elif dimensions.z > dimensions.y and dimensions.z > dimensions.x:
        obj.rotation_euler = (math.radians(90), 0, 0)
    else:
        obj.rotation_euler = (0, 0, 0)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    print(f"Rotação do objeto {obj.name} alinhada corretamente")

# Função para padronizar a orientação da mão
def standardize_hand_orientation():
    ensure_object_mode()
    obj = ensure_object_selected()

    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    z_values = [corner.z for corner in bbox_corners]
    max_z = max(z_values)
    min_z = min(z_values)

    if abs(max_z) < abs(min_z):
        obj.rotation_euler.x += math.radians(180)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        print(f"A orientação do objeto {obj.name} foi padronizada.")

# # Função para reposicionar o objeto e aplicar uma rotação padrão
# def set_object_final_position():
#     ensure_object_mode()
#     obj = ensure_object_selected()

#     obj.location = (0, 0, 0)

#     obj.rotation_euler = (0, 0, 0)
#     bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

#     bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
#     print(f"Objeto {obj.name} movido e rotacionado para uma posição uniforme, origem definida na origem mundial")

def set_object_final_position():
    ensure_object_mode()
    obj = ensure_object_selected()

    # Define a posição do objeto para (0, 0, 0)
    obj.location = (0, 0, 0)

    # Define a rotação em 0 para começar
    obj.rotation_euler = (0, 0, 0)

    # Aplica a rotação final: 90 graus no eixo X
    obj.rotation_euler[0] = 1.5708  # 90 graus em radianos

    # Aplica as transformações (posição e rotação)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # Define a origem do objeto no centro do cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    print(f"Objeto {obj.name} movido, rotacionado em 90° no eixo X e origem definida na origem mundial")


# Função para focar a visão no objeto (como Numpad .)
def focus_view_on_object():
    obj = ensure_object_selected()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {
                        'area': area,
                        'region': region,
                        'edit_object': bpy.context.edit_object,
                        'selected_objects': [obj],
                    }
                    with bpy.context.temp_override(**override):
                        bpy.ops.view3d.view_selected(use_all_regions=False)
                        print(f"Visão focada no objeto {obj.name}")
                    return

# Função para definir a visão frontal (como Numpad 1)
def set_view_to_front():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {
                        'area': area,
                        'region': region,
                    }
                    with bpy.context.temp_override(**override):
                        bpy.ops.view3d.view_axis(type='FRONT')
                        print("Visão ajustada para Frontal")
                    return
