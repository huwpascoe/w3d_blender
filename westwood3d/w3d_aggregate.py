import os
from . import w3d_struct

def aggregate(root, paths):
    nodes = {}
    ag_rec(root, paths, nodes)
    return nodes
    
def ag_rec(root, paths, nodes):
    files = {}
    concats = {}
    
    # explicit aggregate
    ag = root.get('aggregate')
    if ag is not None:
        ainfo = ag.get('aggregate_info')
        if s[ainfo.BaseModelName] not in nodes:
            files[ainfo.BaseModelName] = True
        for s in ainfo.Subobjects:
            if s['SubobjectName'] not in nodes:
                files[s['SubobjectName']] = True
    
    # hlod
    hlod = root.get('hlod')
    if hlod is not None:
        
        # hierarchy
        hinfo = hlod.get('hlod_header')
        hierarchy = root.get('hierarchy')
        if (hierarchy is None or
            hinfo.HierarchyName != hierarchy.get('hierarchy_header').Name):
            concats[hinfo.HierarchyName] = True
            
        # object containers
        m = root.getRec('mesh_header3')
        ctr = m.ContainerName if m is not None else None
        
        for lod in hlod.find('hlod_lod_array'):
            for h in lod.find('hlod_sub_object'):
                s = h.Name.split('.')
                if len(s) > 1 and ctr != s[0]:
                    concats[s[0]] = True
        
        for lod in hlod.find('hlod_aggregate_array'):
            for h in lod.find('hlod_sub_object'):
                if h.Name not in nodes:
                    files[h.Name] = True
    
    # concats
    for f in concats.keys():
        n = ag_load(f, paths)
        if n is not None:
            # Remove hlod from concat aggregates, just incase
            ch = n.get('hlod')
            if ch is not None:
                n.children.remove(ch)
            
            # concat to current root, it can't load recursively
            root.children += n.children
        
    # load files
    children = []
    for f in files.keys():
        n = ag_load(f, paths)
        if n is not None:
            nodes[f] = n # prevent duplicate loading
            children.append(n)
    
    # load aggregates recursively
    for n in children:
        ag_rec(n, paths, nodes)

def ag_load(files, paths):
    root = None
    for file in files:
        load = False
        for path in paths:
            filename = os.path.join(path, file.lower() + '.w3d')
            try:
                root = w3d_struct.load(filename)
                load = True
                break
            except:
                pass
        if load == False:
            print('MISSING: ' + file.lower() + '.w3d')
    
    return root