import bpy
import bmesh
import os
from . import w3d_struct, mat_reduce

def gen_mats(materials):
    for mdata in materials:
        pdata = mdata['mpass']
        
        mat = bpy.data.materials.new('Material')
        mdata['BlenderMaterial'] = mat
        
        mat.use_nodes = True
        tree = mat.node_tree
        for n in tree.nodes:
            tree.nodes.remove(n)
        
        w3d = mat.westwood3d
        
        # basic info
        w3d.surface_type = str(mdata['surface'])
        w3d.sort_level = mdata['sort_level']
        
        # add passes
        w3d.mpass_count = len(pdata)
        while len(w3d.mpass) < w3d.mpass_count:
            w3d.mpass.add()
        
        name = ''
        texdone = False
        for p in range(len(pdata)):
            
            w3d.mpass[p].name = pdata[p]['vertex_material']['name']
            name += w3d.mpass[p].name + '-'
            
            vm = pdata[p]['vertex_material']['info']
            w3d.mpass[p].ambient = vm.Ambient
            w3d.mpass[p].diffuse = vm.Diffuse
            w3d.mpass[p].specular = vm.Specular
            w3d.mpass[p].emissive = vm.Emissive
            w3d.mpass[p].shininess = vm.Shininess
            w3d.mpass[p].opacity = vm.Opacity
            w3d.mpass[p].translucency = vm.Translucency
            w3d.mpass[p].mapping0 = str(vm.Mapping0)
            w3d.mpass[p].mapping1 = str(vm.Mapping1)
            
            sh = pdata[p]['shader']
            w3d.mpass[p].srcblend = str(sh['SrcBlend'])
            w3d.mpass[p].destblend = str(sh['DestBlend'])
            w3d.mpass[p].depthmask = sh['DepthMask']
            w3d.mpass[p].alphatest = sh['AlphaTest']
            
            
            textures = []
            s = 0
            for stage in pdata[p]['stages']:
                t = bpy.data.textures.new(stage['name'], 'IMAGE')
                t.image = bpy.data.images[stage['name']] if stage['name'] in bpy.data.images else None
                
                if s == 0:
                    w3d.mpass[p].stage0 = t.name
                else:
                    w3d.mpass[p].stage1 = t.name
                s += 1
                
        # set name
        if name != '':
            mat.name = name
        
        # Create basic node material
        nodegeo = tree.nodes.new('GEOMETRY')
        nodeout = tree.nodes.new('OUTPUT')
        
        if len(w3d.mpass) > 1:
            nodemix = tree.nodes.new('MIX_RGB')
            tree.links.new(nodegeo.outputs[6], nodemix.inputs[0])
            tree.links.new(nodemix.outputs[0], nodeout.inputs[0])
            r = 1
            for mpass in w3d.mpass:
                if mpass.stage0 in bpy.data.textures:
                    nodetex = tree.nodes.new('TEXTURE')
                    nodetex.texture = bpy.data.textures[mpass.stage0]
                    tree.links.new(nodegeo.outputs[4], nodetex.inputs[0])
                    tree.links.new(nodetex.outputs[1], nodemix.inputs[r])
                else:
                    nodeval = tree.nodes.new('VALUE')
                    nodeval.outputs[0].default_value = 1.0
                    tree.links.new(nodeval.outputs[0], nodemix.inputs[r])
                r += 1
                if r > 2:
                    break
        else:
            for mpass in w3d.mpass:
                if mpass.stage0 in bpy.data.textures:
                    nodetex = tree.nodes.new('TEXTURE')
                    nodetex.texture = bpy.data.textures[mpass.stage0]
                    tree.links.new(nodegeo.outputs[4], nodetex.inputs[0])
                    tree.links.new(nodetex.outputs[1], nodeout.inputs[0])
                    break

def gen_pivots(root, name, paths):
    
    exload = True
    hierarchy = root.get('hierarchy')
    if hierarchy is not None:
        info = hierarchy.get('hierarchy_header')
        if info.Name == name:
            exload = False
    
    if exload:
        hierarchy = None
        for path in paths:
            try:
                file = open(os.path.join(path, name + '.w3d'), 'rb')
                root = w3d_struct.node()
                root.children = w3d_struct.parse_nodes(file)
                hierarchy = root.get('hierarchy')
                if hierarchy is not None:
                    info = hierarchy.get('hierarchy_header')
                    if info.Name != name:
                        hierarchy = None
                    else:
                        break
                file.close()
            except:
                pass
    
    if hierarchy == None:
        raise Exception("Couldn't load hierarchy: " + name)
    
    pivots = []
    for p in hierarchy.get('pivots').pivots:
        ob = bpy.data.objects.new(p['Name'], None)
        if p['ParentIdx'] != 0xffffffff:
            ob.parent = pivots[p['ParentIdx']]
        
        ob.location = p['Translation']
        ob.rotation_mode = 'QUATERNION'
        r = p['Rotation']
        ob.rotation_quaternion = (r[3], r[0], r[1], r[2])
        ob.rotation_mode = 'XYZ'
        
        bpy.context.scene.objects.link(ob)
        pivots.append(ob)
    
    return pivots

def deform_mesh(mesh, mdata, pivots):
    inf = mdata.get('vertex_influences')
    if inf is None:
        return
    inf = inf.influences
    
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bpy.context.scene.update()
    for v in bm.verts:
        v.co = pivots[inf[v.index]].matrix_world * v.co
    bm.to_mesh(mesh)
    
def make_hierarchy(root, meshes, paths):
    hroot = root.get('hlod')
    info = hroot.get('hlod_header')
    for hlod in hroot.find('hlod_lod_array'):
        pivots = gen_pivots(root, info.HierarchyName, paths)
        for h in hlod.find('hlod_sub_object'):
            if h.Name in meshes:
                meshes[h.Name][0].parent = pivots[h.BoneIndex]
                deform_mesh(meshes[h.Name][0].data, meshes[h.Name][1], pivots)
    
def make_meshes(root):
    meshes = root.find('mesh')
    meshlist = {}
    for m in meshes:
        info = m.get('mesh_header3')
        verts = m.get('vertices').vertices
        faces = m.get('triangles').triangles
        
        tex = m.findRec('texture_name')
        mpass = m.findRec('material_pass')
        
        tids = m.getRec('texture_ids')
        if tids != None:
            tids = tids.ids
        
        # create mesh
        me = bpy.data.meshes.new(info.MeshName)
        
        # current bmesh's uv.new() doesn't work properly
        # have to create UVlayers with the old API
        for p in range(len(mpass)):
            uvs = mpass[p].findRec('stage_texcoords')
            for uv in range(len(uvs)):
                me.uv_textures.new('pass' + str(p + 1) + '.' + str(uv))
        bm = bmesh.new()
        bm.from_mesh(me)
        
        for v in verts:
            bm.verts.new(v)
        for f in faces:
            try:
                bm.faces.new([bm.verts[i] for i in f['Vindex']]).material_index = f['Mindex']
            except:
                print("duplicate faces encountered on:" + info.MeshName)
        
        # vertex color information
        for p in range(len(mpass)):
            dcg = mpass[p].get('dcg')
            if dcg is not None:
                alpha = False
                for c in dcg.dcg:
                    if c[3] < 255:
                        alpha = True
                        break
                
                layer = bm.loops.layers.color.new('pass' + str(p + 1))
                for v in range(len(bm.verts)):
                    for loop in bm.verts[v].link_loops:
                        col = dcg.dcg[v]
                        if alpha:
                            loop[layer].r = col[3] / 255
                            loop[layer].g = col[3] / 255
                            loop[layer].b = col[3] / 255
                        else:
                            loop[layer].r = col[0] / 255
                            loop[layer].g = col[1] / 255
                            loop[layer].b = col[2] / 255
        
        # Transfer UVs
        uvs = m.findRec('stage_texcoords')
        for uvi in range(len(uvs)):
            layer = bm.loops.layers.uv[uvi]
            for v in range(len(bm.verts)):
                for loop in bm.verts[v].link_loops:
                    loop[layer].uv = uvs[uvi].texcoords[v]
        
        
        bm.to_mesh(me)
        
        # attach to object, place in scene
        ob = bpy.data.objects.new(info.MeshName, me)
        bpy.context.scene.objects.link(ob)
        bpy.context.scene.objects.active = ob
            
        # move hidden objects to second layer
        if info.Attributes & 0x00001000:
            # move vis objects way over there
            if info.Attributes & 0x00000040:
                ob.layers[10] = True
                ob.layers[0] = False
            else:
                ob.layers[1] = True
                ob.layers[0] = False
        
        # materials
        for mat in m.Materials:
            bpy.ops.object.material_slot_add()
            ob.material_slots[ob.material_slots.__len__() - 1].material = mat['BlenderMaterial']
        
        # assign textures to uv map
        if tids != None and len(tids) > 0 and len(tex) > 0:
            for uvlay in me.uv_textures:
                i = 0
                for foo in uvlay.data:
                    try:
                        foo.image = bpy.data.images[tex[tids[i]].name]
                    except:
                        pass
                    if i < len(tids) - 1:
                        i += 1
        
        # add to list for hierarchy
        meshlist[info.ContainerName + '.' + info.MeshName] = (ob, m)
    
    return meshlist
        
def load_images(root, paths):
    # get every image
    filenames = root.findRec('texture_name')
    
    # load images. Blender can figure out duplicates
    for fn in filenames:
        img = None
        for path in paths:
            try:
                img = bpy.data.images.load(os.path.join(path, fn.name))
            except:
                # if it failed, try again with .dds
                try:
                    ddsname = os.path.splitext(fn.name)[0] + '.dds'
                    img = bpy.data.images.load(os.path.join(path, ddsname))
                    fn.name = ddsname
                except:
                    pass
            
            if img != None:
                break
        
        if img == None:
            print('image not loaded: ' + fn.name)
            
# blender stuff
def read_some_data(context, filepath, ignore_lightmap):
    print("running read_some_data...")
    
    # source directories
    current_path = os.path.dirname(filepath)
    paths = [
        current_path,
        os.path.join(current_path, '../textures/'),
    ]
    
    file = open(filepath, 'rb')
    root = w3d_struct.node()
    try:
        root.children = w3d_struct.parse_nodes(file)
    finally:
        file.close()
    
    # create scene
    load_images(root, paths)
    materials = mat_reduce.mat_reduce(root, ignore_lightmap)
    gen_mats(materials)
    meshes = make_meshes(root)
    hierarchy = make_hierarchy(root, meshes, paths)
    
    #bpy.context.scene.game_settings.material_mode = 'GLSL'
    for scrn in bpy.data.screens:
        if scrn.name == 'Default':
            bpy.context.window.screen = scrn
            for area in scrn.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.viewport_shade = 'TEXTURED'
    
    print('done')
    return {'FINISHED'}

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportWestwood3D(Operator, ImportHelper):
    '''This appears in the tooltip of the operator and in the generated docs'''
    bl_idname = "import.westwood3d"
    bl_label = "Import Westwood3D"

    # ImportHelper mixin class uses this
    filename_ext = ".w3d"

    filter_glob = StringProperty(
            default="*.w3d",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    ignore_lightmap = BoolProperty(
            name="Don't import lightmaps",
            description="Lightmap data increases material count",
            default=True,
            )
    
    def execute(self, context):
        return read_some_data(context, self.filepath, self.ignore_lightmap)
        
# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportWestwood3D.bl_idname, text="Westwood3D (.w3d)")