bl_info = {
    "name": "Westwood3D Tools",
    "author": "Huw Pascoe",
    "version": (1, 0),
    "blender": (2, 6, 3),
    "location": "Import, Export, Material Panel",
    "description": "Enables content authoring for C&C Renegade",
    "warning": "This is a preview and should not be used for projects",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

if "bpy" in locals():
    import imp
    imp.reload(w3d_material)
    imp.reload(w3d_struct)
    imp.reload(mat_reduce)
    imp.reload(w3d_import)
else:
    from . import w3d_material, w3d_struct, mat_reduce, w3d_import

import bpy

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Material.westwood3d = bpy.props.PointerProperty(type=w3d_material.Westwood3DMaterial)
    bpy.types.INFO_MT_file_import.append(w3d_import.menu_func_import)
    
def unregister():
    bpy.types.INFO_MT_file_import.remove(w3d_import.menu_func_import)
    del bpy.types.Material.westwood3d
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
