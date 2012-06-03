import struct

w3d_keys = {
    0x00000000: 'MESH',
    0x00000002: 'VERTICES',
    0x00000003: 'VERTEX_NORMALS',
    0x0000000C: 'MESH_USER_TEXT',
    0x0000000E: 'VERTEX_INFLUENCES',
    0x0000001F: 'MESH_HEADER3',
    0x00000020: 'TRIANGLES',
    0x00000022: 'VERTEX_SHADE_INDICES',
                       
    0x00000023: 'PRELIT_UNLIT',
    0x00000024: 'PRELIT_VERTEX',
    0x00000025: 'PRELIT_LIGHTMAP_MULTI_PASS',
    0x00000026: 'PRELIT_LIGHTMAP_MULTI_TEXTURE',
                   
    0x00000028: 'MATERIAL_INFO',
                   
    0x00000029: 'SHADERS',
                           
    0x0000002A: 'VERTEX_MATERIALS',
    0x0000002B: 'VERTEX_MATERIAL',                           
    0x0000002C: 'VERTEX_MATERIAL_NAME',
    0x0000002D: 'VERTEX_MATERIAL_INFO',
    0x0000002E: 'VERTEX_MAPPER_ARGS0',
    0x0000002F: 'VERTEX_MAPPER_ARGS1',
                   
    0x00000030: 'TEXTURES',
    0x00000031: 'TEXTURE',
    0x00000032: 'TEXTURE_NAME',
    0x00000033: 'TEXTURE_INFO',
                           
    0x00000038: 'MATERIAL_PASS',
    0x00000039: 'VERTEX_MATERIAL_IDS',
    0x0000003A: 'SHADER_IDS',
    0x0000003B: 'DCG',
    0x0000003C: 'DIG',
    0x0000003E: 'SCG',
                   
    0x00000048: 'TEXTURE_STAGE',
    0x00000049: 'TEXTURE_IDS',
    0x0000004A: 'STAGE_TEXCOORDS',
    0x0000004B: 'PER_FACE_TEXCOORD_IDS',
                   
                   
    0x00000058: 'DEFORM',
    0x00000059: 'DEFORM_SET',
    0x0000005A: 'DEFORM_KEYFRAME',
    0x0000005B: 'DEFORM_DATA',
                   
    0x00000080: 'PS2_SHADERS',
                       
    0x00000090: 'AABTREE',
    0x00000091: 'AABTREE_HEADER',
    0x00000092: 'AABTREE_POLYINDICES',
    0x00000093: 'AABTREE_NODES',
                   
    0x00000100: 'HIERARCHY',
    0x00000101: 'HIERARCHY_HEADER',                          
    0x00000102: 'PIVOTS',                                    
    0x00000103: 'PIVOT_FIXUPS',
                   
    0x00000200: 'ANIMATION',
    0x00000201: 'ANIMATION_HEADER',                          
    0x00000202: 'ANIMATION_CHANNEL',
    0x00000203: 'BIT_CHANNEL',
                   
    0x00000280: 'COMPRESSED_ANIMATION',
    0x00000281: 'COMPRESSED_ANIMATION_HEADER',
    0x00000282: 'COMPRESSED_ANIMATION_CHANNEL',
    0x00000283: 'COMPRESSED_BIT_CHANNEL',
                   
    0x000002C0: 'MORPH_ANIMATION',
    0x000002C1: 'MORPHANIM_HEADER',
    0x000002C2: 'MORPHANIM_CHANNEL',
    0x000002C3: 'MORPHANIM_POSENAME',
    0x000002C4: 'MORPHANIM_KEYDATA',
    0x000002C5: 'MORPHANIM_PIVOTCHANNELDATA',
                   
    0x00000300: 'HMODEL',
    0x00000301: 'HMODEL_HEADER',
    0x00000302: 'NODE',
    0x00000303: 'COLLISION_NODE',
    0x00000304: 'SKIN_NODE',
    0x00000305: 'OBSOLETE_W3D_CHUNK_HMODEL_AUX_DATA',
    0x00000306: 'OBSOLETE_W3D_CHUNK_SHADOW_NODE',
                   
    0x00000400: 'LODMODEL',
    0x00000401: 'LODMODEL_HEADER',
    0x00000402: 'LOD',
                   
    0x00000420: 'COLLECTION',
    0x00000421: 'COLLECTION_HEADER',
    0x00000422: 'COLLECTION_OBJ_NAME',
    0x00000423: 'PLACEHOLDER',
    0x00000424: 'TRANSFORM_NODE',
                   
    0x00000440: 'POINTS',
                   
    0x00000460: 'LIGHT',
    0x00000461: 'LIGHT_INFO',
    0x00000462: 'SPOT_LIGHT_INFO',
    0x00000463: 'NEAR_ATTENUATION',
    0x00000464: 'FAR_ATTENUATION',
                   
    0x00000500: 'EMITTER',
    0x00000501: 'EMITTER_HEADER',
    0x00000502: 'EMITTER_USER_DATA',
    0x00000503: 'EMITTER_INFO',
    0x00000504: 'EMITTER_INFOV2',
    0x00000505: 'EMITTER_PROPS',
    0x00000506: 'OBSOLETE_W3D_CHUNK_EMITTER_COLOR_KEYFRAME',
    0x00000507: 'OBSOLETE_W3D_CHUNK_EMITTER_OPACITY_KEYFRAME',
    0x00000508: 'OBSOLETE_W3D_CHUNK_EMITTER_SIZE_KEYFRAME',
    0x00000509: 'EMITTER_LINE_PROPERTIES',
    0x0000050A: 'EMITTER_ROTATION_KEYFRAMES',
    0x0000050B: 'EMITTER_FRAME_KEYFRAMES',
    0x0000050C: 'EMITTER_BLUR_TIME_KEYFRAMES',
                   
    0x00000600: 'AGGREGATE',
    0x00000601: 'AGGREGATE_HEADER',
    0x00000602: 'AGGREGATE_INFO',
    0x00000603: 'TEXTURE_REPLACER_INFO',
    0x00000604: 'AGGREGATE_CLASS_INFO',
                   
    0x00000700: 'HLOD',
    0x00000701: 'HLOD_HEADER',
    0x00000702: 'HLOD_LOD_ARRAY',
    0x00000703: 'HLOD_SUB_OBJECT_ARRAY_HEADER',
    0x00000704: 'HLOD_SUB_OBJECT',
    0x00000705: 'HLOD_AGGREGATE_ARRAY',
    0x00000706: 'HLOD_PROXY_ARRAY',
                   
    0x00000740: 'BOX',
    0x00000741: 'SPHERE',                                    
    0x00000742: 'RING',                                      
                   
    0x00000750: 'NULL_OBJECT',
                   
    0x00000800: 'LIGHTSCAPE',
    0x00000801: 'LIGHTSCAPE_LIGHT',
    0x00000802: 'LIGHT_TRANSFORM',
                   
    0x00000900: 'DAZZLE',
    0x00000901: 'DAZZLE_NAME',
    0x00000902: 'DAZZLE_TYPENAME',
                   
    0x00000A00: 'SOUNDROBJ',
    0x00000A01: 'SOUNDROBJ_HEADER',
    0x00000A02: 'SOUNDROBJ_DEFINITION',
}

class node:
    children = []
    
    def read(self, file, size):
        file.read(size)
    def write(self, file):
        pass
        
    def log(self, max, indent=0):
        print(('\t'*indent) + self.__class__.__name__[5:])
        
        indent += 1
        
        for key, value in self.__dict__.items():
            if key != 'children':
                print(('\t'*indent) + key + ' = ' + str(value))
        
        if indent < max:
            for n in self.children:
                n.log(max, indent)
        
    def get(self, name):
        for i in self.children:
            if i.__class__.__name__[5:] == name:
                return i
        return None
    def getRec(self, name):
        for i in self.children:
            if i.__class__.__name__[5:] == name:
                return i
            res = i.getRec(name)
            if res != None:
                return res
        return None
    def find(self, name):
        all = []
        for i in self.children:
            if i.__class__.__name__[5:] == name:
                all.append(i)
        return all
    def findRec(self, name, all=None):
        if all == None:
            all = []
        for i in self.children:
            if i.__class__.__name__[5:] == name:
                all.append(i)
            i.findRec(name, all)
        return all

class node_mesh(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_mesh_header3(node):
    def read(self, file, size):
        data = read_struct(file, 'LL16s16sLLLLlLLLL3f3f3ff')
        self.Version = data[0]
        self.Attributes = data[1]
        self.MeshName = data[2].split(b'\0')[0].decode('utf-8')
        self.ContainerName = data[3].split(b'\0')[0].decode('utf-8')
        self.NumTris = data[4]
        self.NumVertices = data[5]
        self.NumMaterials = data[6]
        self.NumDamageStages = data[7]
        self.SortLevel = data[8]
        self.PrelitVersion = data[9]
        self.FutureCounts = data[10]
        self.VertexChannels = data[11]
        self.FaceChannels = data[12]
        self.Min = (data[13], data[14], data[15])
        self.Max = (data[16], data[17], data[18])
        self.SphCenter = (data[19], data[20], data[21])
        self.SphRadius = data[22]
    def write(self, file):
        pass
class node_vertices(node):
    def read(self, file, size):
        self.vertices = []
        while size > 0:
            data = read_struct(file, '3f')
            self.vertices.append((data[0], data[1], data[2]))
            size -= struct.calcsize('3f')
    def write(self, file):
        pass
class node_vertex_normals(node):
    def read(self, file, size):
        self.normals = []
        while size > 0:
            data = read_struct(file, '3f')
            self.normals.append((data[0], data[1], data[2]))
            size -= struct.calcsize('3f')
    def write(self, file):
        pass
class node_triangles(node):
    def read(self, file, size):
        self.triangles = []
        while size > 0:
            data = read_struct(file, '3LL3ff')
            self.triangles.append({
                'Vindex': (data[0], data[1], data[2]),
                'Attributes': data[3],
                'Normal': (data[4],data[5],data[6]),
                'Dist': data[7],
            })
            size -= struct.calcsize('3LL3ff')
    def write(self, file):
        pass
class node_vertex_materials(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_vertex_material(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_vertex_material_name(node):
    def read(self, file, size):
        self.name = file.read(size).split(b'\0')[0].decode('utf-8')
    def write(self, file):
        pass
class node_vertex_material_info(node):
    def read(self, file, size):
        data = read_struct(file, 'L4B4B4B4Bfff')
        self.Attributes = data[0]
        self.Ambient = (data[1], data[2], data[3])
        self.Diffuse = (data[5], data[6], data[7])
        self.Specular = (data[9], data[10], data[11])
        self.Emissive = (data[13], data[14], data[15])
        self.Shininess = data[17]
        self.Opacity = data[18]
        self.Translucency = data[19]
    def write(self, file):
        pass
class node_dcg(node):
    def read(self, file, size):
        self.dcg = []
        while size > 0:
            data = read_struct(file, '4B')
            self.dcg.append((data[0], data[1], data[2], data[3]))
            size -= struct.calcsize('4B')
    def write(self, file):
        pass
class node_prelit_lightmap_multi_pass(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_material_info(node):
    def read(self, file, size):
        data = read_struct(file, 'LLLL')
        self.PassCount = data[0]
        self.VertexMaterialCount = data[1]
        self.ShaderCount = data[2]
        self.TextureCount = data[3]
    def write(self, file):
        pass
class node_material_pass(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_vertex_material_ids(node):
    def read(self, file, size):
        self.ids = []
        while size > 0:
            data = read_struct(file, 'L')
            self.ids.append(data[0])
            size -= struct.calcsize('L')
    def write(self, file):
        pass
class node_shader_ids(node):
    def read(self, file, size):
        self.ids = []
        while size > 0:
            data = read_struct(file, 'L')
            self.ids.append(data[0])
            size -= struct.calcsize('L')
    def write(self, file):
        pass
class node_texture_stage(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_texture_ids(node):
    def read(self, file, size):
        self.ids = []
        while size > 0:
            data = read_struct(file, 'L')
            self.ids.append(data[0])
            size -= struct.calcsize('L')
    def write(self, file):
        pass
class node_stage_texcoords(node):
    def read(self, file, size):
        self.texcoords = []
        while size > 0:
            data = read_struct(file, '2f')
            self.texcoords.append((data[0], data[1]))
            size -= struct.calcsize('2f')
    def write(self, file):
        pass
class node_texture_texcoords(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_textures(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_texture(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_hierarchy(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_texture_name(node):
    def read(self, file, size):
        self.name = file.read(size).split(b'\0')[0].decode('utf-8')
    def write(self, file):
        pass
class node_hierarchy_header(node):
    def read(self, file, size):
        data = read_struct(file, 'L16sL3f')
        self.Version = data[0]
        self.Name = data[1].split(b'\0')[0].decode('utf-8')
        self.NumPivots = data[2]
        self.Center = (data[3], data[4], data[5])
    def write(self, file):
        pass
class node_pivots(node):
    def read(self, file, size):
        self.pivots = []
        while size > 0:
            data = read_struct(file, '16sL3f3f4f')
            self.pivots.append({
                'Name': data[0].split(b'\0')[0].decode('utf-8'),
                'ParentIdx': data[1],
                'Translation': (data[2],data[3],data[4]),
                'Eulerangles': (data[5],data[6],data[7]),
                'Rotation': (data[8],data[9],data[10],data[11])
            })
            size -= struct.calcsize('16sL3f3f4f')
    def write(self, file):
        pass
class node_hlod(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_hlod_lod_array(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_hlod_proxy_array(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
class node_hlod_sub_object(node):
    def read(self, file, size):
        data = read_struct(file, 'L32s')
        self.BoneIndex = data[0]
        self.Name = data[1].split(b'\0')[0].decode('utf-8')
    def write(self, file):
        pass
class node_(node):
    def read(self, file, size):
        self.children = parse_nodes(file, size)
    def write(self, file):
        pass
        
# loading algorithm

def read_struct(file, fmt):
    binary = file.read(struct.calcsize(fmt))
    
    if binary == b'':
        return None
    
    data = struct.unpack(fmt, binary)
    return data
    
def read_header(file):
    data = read_struct(file, 'LL')
    
    if data == None:
        return None
    
    try:
        type = w3d_keys[data[0]]
    except KeyError:
        type = 'ERROR'
    
    size = data[1] & 0x7FFFFFFF
    
    return (type, size)
    
def parse_nodes(file, size=0x7FFFFFFF):
    nodes = []
    
    while size > 0:
        ci = read_header(file)
        if ci == None:
            break;
        
        # instantiate and load node
        try:
            the_node = globals()['node_' + ci[0].lower()]()
        except KeyError:
            the_node = node()
            the_node.unknown = ci[0]
        
        the_node.read(file, ci[1])
        nodes.append(the_node)
        
        # limit size for nested chunks
        size -= 8 + ci[1] # header size + chunk size
        
    return nodes